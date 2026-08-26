import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from src.api.routers.bps import bps
from fastapi import FastAPI
from src.api.routers.docker import docker
from src.core.storage.loadStorageManager import loadAll
from src.utils.docsWebsocket import websocket

from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

DOCS_ROOT = Path(__file__).resolve().parents[1] / "docs"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

loadAll()

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _read_docs_page(file_name: str) -> HTMLResponse:
    file_path = DOCS_ROOT / file_name
    file_content = file_path.read_text()
    return HTMLResponse(file_content)


@app.get("/docs2/", response_class=HTMLResponse)
async def docs_switcher():
    return _read_docs_page("project_documentation_switcher.html")


@app.get("/docs2/legacy", response_class=HTMLResponse)
async def docs_legacy():
    return _read_docs_page("project_documentation.html")


@app.get("/docs2/current", response_class=HTMLResponse)
async def docs_current():
    return _read_docs_page("project_documentation_current.html")


app.include_router(bps.router)
app.include_router(docker.router)

    
websocket(api=app)

#generateForFile("test_alpine_shell","/home/lorendos/Projects/DBackup-Server/test_files")
#generateSplitBackups("/home/lorendos/Projects/DBackup-Server/backups/test.tar.gz",45)
