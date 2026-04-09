from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import libros, notas, sesiones, estadisticas

# STEP 1 — Lifespan: only init_db, no StaticFiles for covers
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# STEP 2 — App init (unchanged)
app = FastAPI(title="Bookish API", version="1.5.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STEP 3 — Routers (unchanged)
app.include_router(libros.router,       prefix="/api/libros",   tags=["Libros"])
app.include_router(notas.router,        prefix="/api",          tags=["Notas"])
app.include_router(sesiones.router,     prefix="/api",          tags=["Sesiones"])
app.include_router(estadisticas.router, prefix="/api",          tags=["Estadisticas"])

if __name__ == "__main__":
    import uvicorn
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="127.0.0.1", port=port)
