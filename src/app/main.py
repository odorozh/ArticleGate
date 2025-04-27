from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    welcome_msg = "Welcome to ArticleGate Web-app! " + \
                  "Store and retrieve information about scientific articles."
    return {"ServiceInfo" : welcome_msg}
