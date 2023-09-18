from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# env_file = ".env.development"
env_file = ".env.production"
load_dotenv(dotenv_path=env_file)

from app import routers as api

app = FastAPI(
    title="LangChain",
    description="",
    version="0.0.0",
    redoc_url=None,
)

# CORS settings
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

# add routers
app.include_router(api.router)


@app.get("/healthz")
async def health():
    return {"status": "up"}
