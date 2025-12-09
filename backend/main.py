from fastapi import FastAPI

app = FastAPI(title="Customer Inquiry Backend")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
