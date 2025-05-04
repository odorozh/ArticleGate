"""
    General methods and FastAPI-application object
    of the Web service 'Article Gate'.
"""

from typing import Annotated

from authx import AuthX, AuthXConfig
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import(
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from .models.base import BaseModel
from .models.article import ArticleModel
from .models.author import AuthorModel
from .models.organisation import OrganisationModel
from .models.article_to_author import ArticleToAuthorModel
from .schemas import (
    AuthorIdSchema,
    ArticleDOISchema,
    OrganisationIdSchema,
    ArticleAuthorBindingSchema,
    ArticleFullSchema,
    OrganisationFullSchema,
)
from . import app_admin


db_engine = create_async_engine("sqlite+aiosqlite:///app/article_gate.sqlite3")
new_session = async_sessionmaker(db_engine, expire_on_commit=False)
app = FastAPI()

access_cookie_name = app_admin.ACCESS_COOKIE
security_config = AuthXConfig()
security_config.JWT_SECRET_KEY = app_admin.APP_ADMIN_SECRET
security_config.JWT_ACCESS_COOKIE_NAME = access_cookie_name
security_config.JWT_ACCESS_CSRF_COOKIE_NAME = access_cookie_name
security_config.JWT_TOKEN_LOCATION = ["cookies"]
security_config.JWT_CSRF_METHODS = []
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
async def get_author(data: Annotated[AuthorIdSchema, Depends()], session: SessionDep):
    """
        Handler for author information requests.
    """

    query = sqla.select(AuthorModel).where(AuthorModel.id == data.id)
    results = await session.execute(query)
    return results.scalar()


@app.get("/article", tags=["retrieve data"])
async def get_article(data: Annotated[ArticleDOISchema, Depends()], session: SessionDep):
    """
        Handler for article information requests.
    """

    query = sqla.select(ArticleModel).where(ArticleModel.doi == data.doi)
    results = await session.execute(query)
    return results.scalar()


@app.get("/articles_by_author", tags=["retrieve data"])
async def get_article_by_author(data: Annotated[AuthorIdSchema, Depends()], session: SessionDep):
    """
        Handler for articles list by author ID.
    """

    query = sqla.select(ArticleToAuthorModel).where(ArticleToAuthorModel.author_id == data.id)
    results = await session.execute(query)
    return results.scalars().all()


@app.get("/authors_of_article", tags=["retrieve data"])
async def get_authors_of_article(data: Annotated[ArticleDOISchema, Depends()], session: SessionDep):
    """
        Handler for authors list by article DOI.
    """

    general_query = sqla.select(ArticleToAuthorModel).where(ArticleToAuthorModel.doi == data.doi).order_by(ArticleToAuthorModel.place.asc())
    results = await session.execute(general_query)
    results = results.scalars().all()

    for idx in range(len(results)):
        author_id = results[idx].author_id
        author_query = sqla.select(AuthorModel).where(AuthorModel.id == author_id)
        author_result = await session.execute(author_query)

        results[idx] = results[idx].__dict__
        results[idx]["author_info"] = author_result.scalar_one_or_none()

    return results


@app.get("/org", tags=["retrieve data"])
async def get_org(data: Annotated[OrganisationIdSchema, Depends()], session: SessionDep):
    """
        Handler for organisation information requests.
    """

    query = sqla.select(OrganisationModel).where(OrganisationModel.id == data.id)
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


@app.delete("/delete/org", dependencies=[Depends(security.access_token_required)], tags=["delete"])
async def delete_org(data: Annotated[OrganisationIdSchema, Depends()], session: SessionDep):
    """
        Delete organisation handler.
        Failes if any auther is affilated with requested organisation.
    """

    check_query = sqla.select(AuthorModel).where(AuthorModel.affiliation_org_id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        raise HTTPException(status_code=406, detail="Cant delete organisation with ID {}, because it is used in existing author rows".format(data.id))

    query = sqla.delete(OrganisationModel).where(OrganisationModel.id == data.id)
    results = await session.execute(query)

    if results.rowcount == 0:
        raise HTTPException(status_code=404, detail="Required organisation ID {} was not found".format(data.id))
    return "Organisation with ID {} was deleted".format(data.id)


@app.delete("/delete/binding", dependencies=[Depends(security.access_token_required)], tags=["delete"])
async def delete_binding(data: Annotated[ArticleAuthorBindingSchema, Depends()], session: SessionDep):
    """
        Delete binding article-author row by article DOI and author place.
    """

    query = sqla.delete(ArticleToAuthorModel).where((ArticleToAuthorModel.doi == data.doi) & (ArticleToAuthorModel.place == data.place))
    results = await session.execute(query)

    if results.rowcount == 0:
        raise HTTPException(status_code=404, detail="Author-binding of article {} and place {} was not found".format(data.doi, data.place))
    return "Author-binding of article {} and place {} was deleted".format(data.doi, data.place)


@app.delete("/delete/author", dependencies=[Depends(security.access_token_required)], tags=["delete"])
async def delete_author(data: Annotated[AuthorIdSchema, Depends()], session: SessionDep):
    """
        Delete author handler.
    """

    check_query = sqla.select(ArticleToAuthorModel).where(ArticleToAuthorModel.author_id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        raise HTTPException(status_code=406, detail="Cant delete author with ID {}, because it is used in existing article to author binding".format(data.id))
    
    query = sqla.delete(AuthorModel).where(AuthorModel.id == data.id)
    results = await session.execute(query)

    if results.rowcount == 0:
        raise HTTPException(status_code=404, detail="Required author with ID {} was not found".format(data.id))
    return "Required author with ID {} was deleted".format(data.id)


@app.delete("/delete/article", dependencies=[Depends(security.access_token_required)], tags=["delete"])
async def delete_article(data: Annotated[ArticleDOISchema, Depends()], session: SessionDep):
    """
        Delete article handler.
    """

    check_query = sqla.select(ArticleToAuthorModel).where(ArticleToAuthorModel.doi == data.doi)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        raise HTTPException(status_code=406, detail="Cant delete article DOI {}, because it is used in existing article to author binding".format(data.doi))
    
    query = sqla.delete(ArticleModel).where(ArticleModel.doi == data.doi)
    results = await session.execute(query)

    if results.rowcount == 0:
        raise HTTPException(status_code=404, detail="Required article DOI {} was not found".format(data.doi))
    return "Required article DOI {} was deleted".format(data.doi)


@app.post("/create/article", dependencies=[Depends(security.access_token_required)], tags=["create"])
async def create_article(data: Annotated[ArticleFullSchema, Depends()], session: SessionDep):
    """
        Create new article handler.
    """
    
    check_query = sqla.select(ArticleModel).where(ArticleModel.doi == data.doi)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        raise HTTPException(status_code=406, detail="Cant create article with existing DOI {}".format(data.doi))
    
    new_article = ArticleModel(doi=data.doi, title=data.title, posting_date=data.posting_date)
    session.add(new_article)
    await session.commit()
    return "Article DOI {} was added".format(data.doi)


@app.post("/create/org", dependencies=[Depends(security.access_token_required)], tags=["create"])
async def create_author(data: Annotated[OrganisationFullSchema, Depends()], session: SessionDep):
    """
        Create new organisation handler.
    """
    
    check_query = sqla.select(OrganisationModel).where(OrganisationModel.id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        raise HTTPException(status_code=406, detail="Cant create organisation with existing ID {}".format(data.id))
    
    new_org = OrganisationModel(id=data.doi, title=data.title, location=data.location)
    session.add(new_org)
    await session.commit()
    return "Organisation with ID {} was added".format(data.id)
