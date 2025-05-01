"""
    General methods and FastAPI-application object
    of the Web service 'Article Gate'.
"""

from typing import Annotated

from authx import AuthX, AuthXConfig
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import(
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from .models.base import BaseModel
from .models.article import ArticleModel
from .models.author import AuthorModel
from .models.organisation import OrganisationModel
from .schemas import (
    AuthorGetSchema,
    ArticleGetSchema,
    OrganisationGetSchema,
)
from . import app_admin


db_engine = create_async_engine("sqlite+aiosqlite:///app/article_gate.sqlite3")
new_session = async_sessionmaker(db_engine, expire_on_commit=False)
app = FastAPI()

access_cookie_name = app_admin.ACCESS_COOKIE
security_config = AuthXConfig()
security_config.JWT_SECRET_KEY = app_admin.APP_ADMIN_SECRET
security_config.JWT_ACCESS_COOKIE_NAME = access_cookie_name
security_config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=security_config)


@app.on_event("startup")
async def setup_models():
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def make_new_session():
    """
        Asynchronously get new session to DB.
    """
    async with new_session() as session:
        yield session


# Dependency injection of make_new_session to avoid
# its explicit calls in handlers.
SessionDep = Annotated[AsyncSession, Depends(make_new_session)]


@app.get("/", tags=["welcome page"])
async def root():
    """
        Handler for requests to the root URL of the Web-app.
    """

    welcome_msg = "Welcome to ArticleGate Web-app! " + \
                  "Store and retrieve information about scientific articles."
    return {"ServiceInfo": welcome_msg}


@app.get("/author", tags=["retrieve data"])
async def get_author(data: Annotated[AuthorGetSchema, Depends()], session: SessionDep):
    """
        Handler for author information requests.
    """

    query = select(AuthorModel).where(AuthorModel.id == data.id)
    results = await session.execute(query)
    return results.scalar()


@app.get("/article", tags=["retrieve data"])
async def get_article(data: Annotated[ArticleGetSchema, Depends()], session: SessionDep):
    """
        Handler for article information requests.
    """

    query = select(ArticleModel).where(ArticleModel.doi == data.doi)
    results = await session.execute(query)
    return results.scalar()


@app.get("/org", tags=["retrieve data"])
async def get_org(data: Annotated[OrganisationGetSchema, Depends()], session: SessionDep):
    """
        Handler for organisation information requests.
    """

    query = select(OrganisationModel).where(OrganisationModel.id == data.id)
    results = await session.execute(query)
    return results.scalar()


@app.post("/auth", tags=["auth"])
async def admin_auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], resp: Response):
    """
        Authentificate and save access-token cookie.
    """

    auth_exception = HTTPException(status_code=401, detail="Incorrect username or password")
    if form_data.username != app_admin.APP_ADMIN_LOGIN:
        raise auth_exception
    if form_data.password != app_admin.APP_ADMIN_PASSWORD:
        raise auth_exception
    
    token = security.create_access_token(uid="admin")
    resp.set_cookie(access_cookie_name, token)
    return {access_cookie_name: token}
