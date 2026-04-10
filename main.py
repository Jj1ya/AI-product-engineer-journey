from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, AI Product Engineer!"}

@app.get("/health")
def health_check():
    return {"status": "OK"}