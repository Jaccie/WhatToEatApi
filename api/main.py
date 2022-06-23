from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv
from mangum import Mangum
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

load_dotenv(find_dotenv())

maxdb = mysql.connector.connect(
    host="what-to-eat-database.c7qk1icsj9gs.ap-northeast-2.rds.amazonaws.com",
    user="JessieKao",
    password="Jaccie850315",
    database="foods",
)

cursor = maxdb.cursor()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/random")
async def get_random():
    cursor.execute("SELECT * FROM place ORDER BY RAND() LIMIT 1;")
    result = cursor.fetchone()
    return {"place_id": result[0]}

@app.get("/users")
async def get_users():
    return {"message": "Get Users!"}

# app.include_router(api_router, prefix="/api/v1")
handler = Mangum(app)
