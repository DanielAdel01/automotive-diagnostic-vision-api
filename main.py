from fastapi import FastAPI
from routers import diagnostics, vision, speech, llm, assistant

app = FastAPI()
app.include_router(diagnostics.router)
app.include_router(vision.router)
app.include_router(speech.router)
app.include_router(llm.router)
app.include_router(assistant.router)

@app.get("/")
def root():
    return {"message": "Automotive Diagnostic API is running"}
