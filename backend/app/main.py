from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import notes, graph, settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zettelkasten Note Taker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)
app.include_router(graph.router)
app.include_router(settings.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
