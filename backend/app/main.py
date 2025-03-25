from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
import joblib # type: ignore
from datetime import datetime
from dotenv import load_dotenv # type: ignore
import os

# Get the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env
load_dotenv(os.path.join(BASE_DIR, '.env'))
MONGO_URI = os.getenv("MONGO_URI")  # e.g., "mongodb+srv://..."

# FastAPI app
app = FastAPI()

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URI)
db = client["your_database"]

# Load model and vectorizer
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'vectorizer.pkl'))

class Message(BaseModel):
    message: str

@app.get("/")
async def home():
    return {"message": "Welcome to the Scam/Ham Prediction API"}

@app.post("/predict")
async def predict(message: Message):
    try:
        # Transform and predict
        message_bow = vectorizer.transform([message.message])
        prediction = model.predict(message_bow)[0]
        
        # Store in MongoDB
        result = {
            "message": message.message,
            "prediction": prediction,
            "timestamp": datetime.now().isoformat()
        }
        await db.predictions.insert_one(result)
        
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown():
    client.close()

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)