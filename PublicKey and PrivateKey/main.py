from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

   # Generate a pair of public and private keys
private_key = Fernet.generate_key()
public_key = Fernet.generate_key()

   # Simulated user database with user-specific private keys
user_db = {
    "user1": "password1",
    "user2": "password2",
}

user_data = {
    "user1": "Some sensitive data for user 1",
    "user2": "Some sensitive data for user 2",
}

api_keys = {
    "user1_api_key": "user1",
    "user2_api_key": "user2",
}


class UserCredentials(BaseModel):
       username: str
       password: str

@app.post("/login")
async def login(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password

    if username in user_db and user_db[username] == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

@app.get("/secure-data")
async def get_secure_data(api_key: str = Query(...)):
    if api_key in api_keys:
        user = api_keys[api_key]
        if user in user_data:
            sensitive_data = user_data[user]
            return {"data": sensitive_data}
    
    # If the API key is invalid or user not found, return a 401 error
    raise HTTPException(status_code=401, detail="Authentication failed")