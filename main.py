from fastapi import FastAPI
import uvicorn


app = FastAPI()

# Root route
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

# Example route with parameter
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.post("/chat")
async def chat(query:str):
    return {"message": "Thank You."}

# Run the app directly with python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
