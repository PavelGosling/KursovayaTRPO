# run.py
import uvicorn
from backend.endpoints import app

if __name__ == "__main__":
    uvicorn.run("backend.endpoints:app", port=8080, reload=True)
