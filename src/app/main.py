"""
    General methods and FastAPI-application object
    of the Web service 'Article Gate'.
"""

from typing import Annotated
from contextlib import asynccontextmanager

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
    AuthorFullSchema,
    ArticleToAuthorFullSchema,
)
from . import app_admin


# General objects: application and DB engine/session maker,
# that are required for the application processing.
db_engine = create_async_engine("sqlite+aiosqlite:///app/article_gate.sqlite3")
new_session = async_sessionmaker(db_engine, expire_on_commit=False)
app = FastAPI()

# Security config for authentification and access cookie
ACCESS_COOKIE_NAME = app_admin.ACCESS_COOKIE
security_config = AuthXConfig()
security_config.JWT_SECRET_KEY = app_admin.APP_ADMIN_SECRET
security_config.JWT_ACCESS_COOKIE_NAME = ACCESS_COOKIE_NAME
security_config.JWT_ACCESS_CSRF_COOKIE_NAME = ACCESS_COOKIE_NAME
security_config.JWT_TOKEN_LOCATION = ["cookies"]
security_config.JWT_CSRF_METHODS = []
security = AuthX(config=security_config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        Prepare DB on application start up
    """
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    return


async def make_new_session():
    """
        Asynchronously get new session to DB.
    """
    async with new_session() as session:
        yield session


# Dependency injection of make_new_session to avoid
# its explicit calls in handlers.
SessionDep = Annotated[AsyncSession, Depends(make_new_session)]

# Security access token dependency
AccessDeps = [Depends(security.access_token_required)]


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

    general_query = sqla.select(ArticleToAuthorModel)\
        .where(ArticleToAuthorModel.doi == data.doi)\
        .order_by(ArticleToAuthorModel.place.asc())

    results = await session.execute(general_query)
    results = results.scalars().all()

    for idx, elem in enumerate(results):
        author_id = elem.author_id
        author_query = sqla.select(AuthorModel).where(AuthorModel.id == author_id)
        author_result = await session.execute(author_query)

        results[idx] = elem.__dict__
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
    resp.set_cookie(ACCESS_COOKIE_NAME, token)
    return {ACCESS_COOKIE_NAME: token}


@app.delete("/delete/org", dependencies=AccessDeps, tags=["delete"])
async def delete_org(data: Annotated[OrganisationIdSchema, Depends()], session: SessionDep):
    """
        Delete organisation handler.
        Failes if any auther is affilated with requested organisation.
    """

    check_query = sqla.select(AuthorModel).where(AuthorModel.affiliation_org_id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        msg = f"Cant delete organisation with ID {data.id}, because of affiliated authors"
        raise HTTPException(status_code=406, detail=msg)

    query = sqla.delete(OrganisationModel).where(OrganisationModel.id == data.id)
    results = await session.execute(query)
    await session.commit()

    if results.rowcount == 0:
        msg = f"Required organisation ID {data.id} was not found"
        raise HTTPException(status_code=404, detail=msg)
    return f"Organisation with ID {data.id} was deleted"


@app.delete("/delete/binding", dependencies=AccessDeps, tags=["delete"])
async def delete_binding(data: Annotated[ArticleAuthorBindingSchema, Depends()], session: SessionDep):
    """
        Delete binding article-author row by article DOI and author place.
    """

    query = sqla.delete(ArticleToAuthorModel)\
        .where((ArticleToAuthorModel.doi == data.doi) & (ArticleToAuthorModel.place == data.place))
    results = await session.execute(query)
    await session.commit()

    if results.rowcount == 0:
        msg = f"Author-binding of article {data.doi} and place {data.place} was not found"
        raise HTTPException(status_code=404, detail=msg)
    return f"Author-binding of article {data.doi} and place {data.place} was deleted"


@app.delete("/delete/author", dependencies=AccessDeps, tags=["delete"])
async def delete_author(data: Annotated[AuthorIdSchema, Depends()], session: SessionDep):
    """
        Delete author handler.
    """

    check_query = sqla.select(ArticleToAuthorModel).where(ArticleToAuthorModel.author_id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        msg = f"Cant delete author with ID {data.id}, because of existing article to author binding"
        raise HTTPException(status_code=406, detail=msg)

    query = sqla.delete(AuthorModel).where(AuthorModel.id == data.id)
    results = await session.execute(query)
    await session.commit()

    if results.rowcount == 0:
        msg = f"Required author with ID {data.id} was not found"
        raise HTTPException(status_code=404, detail=msg)
    return f"Required author with ID {data.id} was deleted"


@app.delete("/delete/article", dependencies=AccessDeps, tags=["delete"])
async def delete_article(data: Annotated[ArticleDOISchema, Depends()], session: SessionDep):
    """
        Delete article handler.
    """

    check_query = sqla.select(ArticleToAuthorModel).where(ArticleToAuthorModel.doi == data.doi)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        msg = "Cant delete article DOI {data.doi}, because of existing article to author binding"
        raise HTTPException(status_code=406, detail=msg)

    query = sqla.delete(ArticleModel).where(ArticleModel.doi == data.doi)
    results = await session.execute(query)
    await session.commit()

    if results.rowcount == 0:
        msg = f"Required article DOI {data.doi} was not found"
        raise HTTPException(status_code=404, detail=msg)
    return f"Required article DOI {data.doi} was deleted"


@app.post("/create/article", dependencies=AccessDeps, tags=["create"])
async def create_article(data: Annotated[ArticleFullSchema, Depends()], session: SessionDep):
    """
        Create new article handler.
    """

    check_query = sqla.select(ArticleModel).where(ArticleModel.doi == data.doi)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        msg = f"Cant create article with existing DOI {data.doi}"
        raise HTTPException(status_code=406, detail=msg)

    new_article = ArticleModel(doi=data.doi, title=data.title, posting_date=data.posting_date)
    session.add(new_article)
    await session.commit()
    return f"Article DOI {data.doi} was added"


@app.post("/create/org", dependencies=AccessDeps, tags=["create"])
async def create_org(data: Annotated[OrganisationFullSchema, Depends()], session: SessionDep):
    """
        Create new organisation handler.
    """

    check_query = sqla.select(OrganisationModel).where(OrganisationModel.id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        msg = f"Cant create organisation with existing ID {data.id}"
        raise HTTPException(status_code=406, detail=msg)

    new_org = OrganisationModel(id=data.id, title=data.title, location=data.location)
    session.add(new_org)
    await session.commit()
    return f"Organisation with ID {data.id} was added"


@app.post("/create/author", dependencies=AccessDeps, tags=["create"])
async def create_author(data: Annotated[AuthorFullSchema, Depends()], session: SessionDep):
    """
        Create new author handler.
    """

    check_query = sqla.select(AuthorModel).where(AuthorModel.id == data.id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) != 0:
        raise HTTPException(status_code=406, detail=f"Cant add author with existing ID {data.id}")

    check_query2 = sqla.select(OrganisationModel)\
        .where(OrganisationModel.id == data.affiliation_org_id)
    check_results = await session.execute(check_query2)
    if len(check_results.scalars().all()) == 0:
        msg = f"Cant add author with not existing affiliation ID {data.affiliation_org_id}"
        raise HTTPException(status_code=406, detail=msg)

    new_author = AuthorModel(id=data.id, name=data.name, affiliation_org_id=data.affiliation_org_id)
    session.add(new_author)
    await session.commit()
    return f"Author with ID {data.id} was added"


@app.post("/create/article_to_author", dependencies=AccessDeps, tags=["create"])
async def create_article_to_author(
    data: Annotated[ArticleToAuthorFullSchema, Depends()],
    session: SessionDep):
    """
        Create new article to author binding handler.
    """

    check_query = sqla.select(AuthorModel).where(AuthorModel.id == data.author_id)
    check_results = await session.execute(check_query)
    if len(check_results.scalars().all()) == 0:
        raise HTTPException(status_code=406, detail=f"Cant find author with ID {data.author_id}")

    check_query2 = sqla.select(ArticleModel).where(ArticleModel.doi == data.doi)
    check_results = await session.execute(check_query2)
    if len(check_results.scalars().all()) == 0:
        raise HTTPException(status_code=406, detail=f"Cant find article with DOI {data.doi}")

    new_binding = AuthorModel(doi=data.doi, author_id=data.author_id, place=data.place)
    session.add(new_binding)
    await session.commit()
    return f"Binding DOI {data.doi} -> author ID {data.author_id} was added"


@app.post("/alter/article", dependencies=AccessDeps, tags=["alter"])
async def alter_article(data: Annotated[ArticleFullSchema, Depends()], session: SessionDep):
    """
        Alter article handler.
    """

    article = await session.get(ArticleModel, data.doi)
    if article is not None:
        article.title = data.title
        article.posting_date = data.posting_date
        await session.commit()
        return f"Article DOI {data.doi} was altered"

    raise HTTPException(status_code=404, detail=f"Article DOI {data.doi} was not found")


@app.post("/alter/author", dependencies=AccessDeps, tags=["alter"])
async def alter_author(data: Annotated[AuthorFullSchema, Depends()], session: SessionDep):
    """
        Alter author handler.
    """

    author = await session.get(AuthorModel, data.id)
    if author is not None:
        author.name = data.name
        author.affiliation_org_id = data.affiliation_org_id
        await session.commit()
        return f"Author ID {data.id} was altered"

    raise HTTPException(status_code=404, detail=f"Author ID {data.id} was not found")


@app.post("/alter/org", dependencies=AccessDeps, tags=["alter"])
async def alter_org(data: Annotated[OrganisationFullSchema, Depends()], session: SessionDep):
    """
        Alter organisation handler.
    """

    org = await session.get(OrganisationModel, data.id)
    if org is not None:
        org.title = data.title
        org.location = data.location
        await session.commit()
        return f"Organisation ID {data.id} was altered"

    raise HTTPException(status_code=404, detail=f"Organisation ID {data.id} was not found")


@app.post("/alter/article_to_author", dependencies=AccessDeps, tags=["alter"])
async def alter_article_to_author(
    data: Annotated[ArticleToAuthorFullSchema, Depends()],
    session: SessionDep):
    """
        Alter article to author binding handler.
    """

    binding = await session.get(ArticleToAuthorModel, (data.doi, data.author_id))
    if binding is not None:
        binding.place = data.place
        await session.commit()
        return f"Binding DOI {data.doi} -> author ID {data.author_id} was altered"

    msg = f"Binding DOI {data.doi} -> author ID {data.author_id} was not found"
    raise HTTPException(status_code=404, detail=msg)
