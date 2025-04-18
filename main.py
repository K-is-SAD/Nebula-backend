from fastapi import FastAPI
from fastapi.responses import JSONResponse
from gitingest import ingest_async
from routes import summarise_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/greet/{name}")
def greet(name: str):
    return JSONResponse(content={"message": f"Hello, {name}!"})

@app.get("/api/gitingest")
async def gitingest_fn(github_url):
    try:
        summary, tree, content = await ingest_async(github_url)
        print("----------TREE----------")
        print(tree)
        print("--------------------------")
        if not summary or not tree or not content:
            raise ValueError("Failed to fetch repository details.")
        return {
            "summary" : summary,
            "success" : True
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

app.include_router(summarise_route.router)
