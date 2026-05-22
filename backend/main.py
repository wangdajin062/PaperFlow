from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.execution import router as execution_router
from api.models import router as models_router
from api.workflows import router as workflows_router
from services.vscode import open_file, open_folder
from storage.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="PaperFlow API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8765"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflows_router)
app.include_router(execution_router)
app.include_router(models_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


class VSCodeOpenRequest(BaseModel):
    file_path: str | None = None
    folder_path: str | None = None


@app.post("/api/vscode/open")
async def vscode_open(req: VSCodeOpenRequest):
    if req.folder_path:
        return open_folder(req.folder_path)
    if req.file_path:
        return open_file(req.file_path)
    return {"success": False, "error": "file_path or folder_path required"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8765, reload=True)
