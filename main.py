"""
ATS MatchProof — Main Application Entrypoint.
Re-exports FastAPI app from src.app for seamless uvicorn compatibility.
"""

import uvicorn

from src.app import app

__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
