from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mindmap_generator import generate_mindmap

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def create_mindmap(request: Request):
    body = await request.json()
    text = body.get("text", "")
    nodes, edges = generate_mindmap(text)
    return {"nodes": nodes, "edges": edges}
