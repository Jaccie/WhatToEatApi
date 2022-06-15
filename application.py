from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import googlemaps
import random

import os

# .env
GOOGLE_PLACES_API_KEY = "AIzaSyC5jO39cyFb2vMOvm-TWFvmT393Eu5b0P4"
origins = ["*"]

#places
FAV_PLACES = ["ChIJ1ZknGcOrQjQR9tA_7aXt_WQ", "ChIJm3H5hjqqQjQRj5OKx31m7cw", "ChIJec_KyzaqQjQRqvpNC2qFmeI", "ChIJz5YKzDCqQjQR_4KXeLpvQz8", "ChIJQXoy2DaqQjQRArLgDsmBx4U", "ChIJwetj6DCqQjQRQ-fkKnXAnYY",
              "ChIJOQej_jCqQjQRsvgf3NlZPnE", "ChIJec_KyzaqQjQR1Nfja5rK97w", "ChIJA_iHFw-rQjQRaA_nObpM3_I", "ChIJrfDWozaqQjQRiRPNOz42pno", "ChIJ1TYBgsKrQjQRKIqbgiit5Fk", "ChIJcSjKamKrQjQRboZeTqQIDDc",
              "ChIJ9-Hu0jCqQjQR4A95UtrPWzI", "ChIJdasmHs2rQjQRHJ7zliuhgSY", "ChIJI-Z-LDGqQjQRt-_hOGrPpf4", "ChIJ2ePotjeqQjQRyD-Q51Xr0Oc", "ChIJ2ZlUzV6rQjQRGyIFxPBsOuI", "ChIJgcd0b3yrQjQRFpncpfmur6w",
              "ChIJbwko3DaqQjQRfs-77naEJOI", "ChIJcYxfuDCqQjQRs00McwbQqcU", "ChIJz-ZzsjeqQjQRAHc2BAJm6_E", "ChIJr3vnvzaqQjQRw4_aFz_WPwg", "ChIJKbbHuTCqQjQRZS2T6vI1jS0", "ChIJbcOGADGqQjQRfK7bjgaHaEc",
              "ChIJR0nkSUuqQjQRvkeJDaZRQVY", "ChIJWw-AoTaqQjQRV_BodVLuec8", "ChIJ499L49KrQjQRPnng-9bYJLo", "ChIJ7Zfw-C2qQjQR-LkXG37xKD8", "ChIJeyF6BTKqQjQR_ZimXtmid0c", "ChIJm3EnbTKqQjQRKq240g6rfmc",
              "ChIJT1w6Ay6qQjQR3-aM1y8aXYQ", "ChIJwednY4mpQjQRUFPwDKmLxXs", "ChIJYya0hSyqQjQRkEwgQt4-oC8", "ChIJtb609TaqQjQRJwhhIMSLkrc", "ChIJQ7tqMhSrQjQRke0jTexrMe8", "ChIJI9rNyeYBaDQRqD8fhpU8Ix4",
              "ChIJ80YSLNKrQjQRdZU13XCEySk", "ChIJdazBVyyqQjQRDqXaeGyGDdk", "ChIJgQNISIKpQjQRqbCflBogrpw", "ChIJaZFb5DOqQjQRlKpTTglbRsg"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class RandomPara(BaseModel):
    option: str = ""
    choice: str = ""


@app.get("/random/place_photo/{reference}")
def get_place_photo(reference: str):
    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    geocode_result = gmaps.places_photo(
        photo_reference=reference,
        max_width=200)
    file_name = str(reference) + ".png"
    temp = open(file_name, "wb")
    for chunk in geocode_result:
        if chunk:
            temp.write(chunk)
    temp.close()
    return FileResponse(file_name)


def get_reference(x):
    return x["photo_reference"]


@app.post("/random/")
def read_item(para: List[RandomPara]):
    print(para[0].option)
    print(para[0].choice)
    # Client
    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    place_id = random.choice(FAV_PLACES)
    # place_id = FAV_PLACES[-1]
    # geocode_result = gmaps.places_nearby(location=(25.034195, 121.564467), radius=100, type="cafe")
    # aa = gmaps.find_place(input="陸角", input_type="textquery") # 新增使用
    # geocode_result = gmaps.place(place_id="ChIJ1ZknGcOrQjQR9tA_7aXt_WQ", language="zh-TW")
    geocode_result = gmaps.place(place_id=place_id, language="zh-TW")

    # Radar search
    # location = (25.017156, 121.506359)
    # radius = 25000
    # place_type = 'restaurant'
    # places_radar_result = gmaps.places_radar(location, radius, type=place_type)
    print(type(geocode_result["result"]))
    print(hasattr(geocode_result["result"], "formatted_address"))
    # print(aa)
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



