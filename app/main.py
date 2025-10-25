from fastapi import FastAPI

app = FastAPI(title="Clients & Orders")

@app.get("/health")
def health():
    return {"status": "ok"}