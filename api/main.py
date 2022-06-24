from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv
from mangum import Mangum
import mysql.connector
from fastapi.responses import FileResponse
import base64

import googlemaps

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

GOOGLE_PLACES_API_KEY = "AIzaSyC5jO39cyFb2vMOvm-TWFvmT393Eu5b0P4"

cursor = maxdb.cursor()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_reference(x):
    return x["photo_reference"]

@app.get("/random")
async def get_random():
    cursor.execute("SELECT * FROM place ORDER BY RAND() LIMIT 1;")
    result = cursor.fetchone()
    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    geocode_result = gmaps.place(place_id=result[0], language="zh-TW")

    result_dict = geocode_result["result"]
    return {
            "photo_references": list(map(get_reference, result_dict["photos"])),
            "address": result_dict["formatted_address"] if "formatted_address" in result_dict else "",
            "phone": result_dict["formatted_phone_number"] if "formatted_phone_number" in result_dict else "",
            "name": result_dict["name"] if "name" in result_dict else "",
            "price_level": result_dict["price_level"] if "price_level" in result_dict else "",
            "rating": result_dict["rating"] if "rating" in result_dict else "",
            "website": result_dict["website"] if "website" in result_dict else ""
            }

@app.get("/random/place_photo/{reference}")
def get_place_photo(reference: str):

    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    geocode_result = gmaps.places_photo(
        photo_reference=reference,
        max_width=200)

    img = list(geocode_result)
    bytes_img = b''.join(img)

    return base64.b64encode(bytes_img).decode('utf-8')


@app.get("/users")
async def get_users():
    return {"message": "Get Users!"}

# app.include_router(api_router, prefix="/api/v1")
handler = Mangum(app)
