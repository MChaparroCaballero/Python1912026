from fastapi import FastAPI

app = FastAPI(
    title="FerreApp API",
    version="1.0.0",
    description="API REST desacoplada para gestión de productos de ferretería"
)

@app.get("/ping")
def ping():
    return {"message": "pong"}
