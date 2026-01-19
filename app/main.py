from fastapi import FastAPI
app=FastAPI( 
title="My FastAPI Application",
version="1.0.0",
description="This is a sample FastAPI application."
)


@app.get("/ping")
def ping():
        return {"message": "pong"}