"""
    General methods and FastAPI-application object
    of the Web service 'Article Gate'.
"""

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    """
        Handler for requests to the root URL of the Web-app.
    """

    welcome_msg = "Welcome to ArticleGate Web-app! " + \
                  "Store and retrieve information about scientific articles."
    return {"ServiceInfo": welcome_msg}


@app.get("/author/{author_id}")
async def get_author(author_id: int):
    """
        Handler for author information requests.
    """

    return {"id": author_id, "name": "Alice"}  # TODO: change


@app.get("/article/{doi}")
async def get_article(doi: str):
    """
        Handler for article information requests.
    """

    return {"doi": doi}  # TODO: change


@app.get("/org/{org_id}")
async def get_org(org_id: int):
    """
        Handler for organisation information requests.
    """

    return {"org_id": org_id}  # TODO: change
