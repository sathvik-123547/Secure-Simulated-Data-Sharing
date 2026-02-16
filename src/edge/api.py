from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.edge.main import EdgeNode
import uvicorn

app = FastAPI(title="SecureEdge Service", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton Instance
edge_node = EdgeNode()

class IngestRequest(BaseModel):
    id: str
    payload: str  # Encrypted AES
    key: str      # AES Key (Simulated secure channel)

@app.post("/ingest")
async def ingest_telemetry(data: IngestRequest):
    """
    Receives encrypted telemetry from Terminal.
    Performs: Decrypt -> CP-ABE Re-encrypt -> BLS Sign
    """
    try:
        # Convert Pydantic to dict for internal method
        packet = data.dict()
        processed = edge_node.process_ingest(packet)
        return {"status": "success", "processed_data": processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "online", "crypto_engine": "active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
