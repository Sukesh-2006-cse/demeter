
import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# MongoDB connection
MONGO_URI = "mongodb+srv://sukesh_2006:tYOWAm7Tbhk2SV7s@cluster0.lg2htpb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['demeter']  # Use your DB name
users_col = db['user_info']


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    phone: str = None
    email: str = None
    pin: str

@app.post("/register")
def register_user(user: User):
    # Check if user exists by phone or email
    if user.phone:
        if users_col.find_one({"phone": user.phone}):
            raise HTTPException(status_code=400, detail="Phone already registered.")
    if user.email:
        if users_col.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered.")
    # Insert user
    users_col.insert_one(user.dict())
    return {"message": "User registered successfully."}

@app.post("/login")
def login_user(user: User):
    query = {}
    if user.phone:
        query["phone"] = user.phone
    if user.email:
        query["email"] = user.email
    query["pin"] = user.pin
    found = users_col.find_one(query)
    if not found:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"message": "Login successful."}
