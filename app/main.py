from fastapi import FastAPI

app = FastAPI(
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hola Mundoo "}


if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)