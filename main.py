from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, users
from app.database.mongodb import connect_to_mongo, close_mongo_connection


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="User Management API for Conversational AI SaaS"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} - API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
    
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
