from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.cloud.main import CloudRegistry
import uvicorn

app = FastAPI(title="SecureCloud Vault", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cloud_registry = CloudRegistry()

class StorageRequest(BaseModel):
    block_id: str
    data_object: dict

@app.post("/store")
async def store_data(request: StorageRequest):
    """
    Stores encrypted/signed blocks.
    In production, this would write to S3/DB.
    """
    cloud_registry.store(request.block_id, request.data_object)
    return {"status": "stored", "block_id": request.block_id}

@app.get("/block/{block_id}")
async def retrieve_block(block_id: str):
    data = cloud_registry.retrieve(block_id)
    if not data:
        raise HTTPException(status_code=404, detail="Block not found")
    return data

@app.post("/proof")
async def generate_proof(indices: list[int]):
    """
    Simulates Proof Generation for TPA.
    """
    return cloud_registry.generate_integrity_proof(indices)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
