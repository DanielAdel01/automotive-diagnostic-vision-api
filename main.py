from fastapi import FastAPI
from routers import diagnostics, vision

app = FastAPI()
app.include_router(diagnostics.router)
app.include_router(vision.router)

@app.get("/")
def root():
    return {"message": "Automotive Diagnostic API is running"}
