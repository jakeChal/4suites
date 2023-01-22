import requests
import json
from urllib.parse import urljoin
from enum import Enum


def get_pretty_json_string(value_dict):
    return json.dumps(value_dict, indent=4, sort_keys=True, ensure_ascii=False)


class Doors(Enum):
    MAIN_ENTRANCE = 1
    BIKE_PARKING = 2
    MALL = 3
    METER_CABINETS = 4


class FourSuites:
    base_url = "https://api.4suites.nl/v1/"
    login_url = urljoin(base_url, "auth/login")
    doors_url = urljoin(base_url, "doors/accessible")

    def __init__(self, token: str = None):
        self.token = token
        self.doors = {}

    def authenticate(self, email: str, password: str, save_token: bool = False):
        response = requests.post(FourSuites.login_url, json={"email": email, "password": password})
        if response:
            self.token = response.json()['data']["access_token"]
            # print(self.token)
            if save_token:
                with open("token.txt", "w") as f:
                    f.write(self.token)
        else:
            print("The user credentials were incorrect :(")
            exit(1)

    def get_doors(self):
        response = requests.get(FourSuites.doors_url, headers={"authorization": f"Bearer {self.token}"})
        # print(get_pretty_json_string(response.json()))
        if response:
            doors_data = response.json()["data"]
            for i in range(len(doors_data)):
                self.doors[doors_data[i]["title"]] = str(doors_data[i]["id"])
        else:
            print("Check your token bro...")
            exit(1)

    def open_door(self, door: Doors):
        door_url = f"https://api.4suites.nl/v1/doors/"

        if len(self.doors) == 0:
            raise RuntimeError("You need to call get_doors() to get the door IDs first!")

        if door == Doors.MAIN_ENTRANCE:
            door_url = urljoin(door_url, self.doors["#01 Hoofdingang"])
        elif door == Doors.BIKE_PARKING:
            door_url = urljoin(door_url, self.doors["#09 Fietsenstalling 1e etage"])
        elif door == Doors.MALL:
            door_url = urljoin(door_url, self.doors["#02 Klapdeur 1e etage"])
        elif door == Doors.METER_CABINETS:
            door_url = urljoin(door_url, self.doors["#05 Meterkasten"])

        door_url = urljoin(door_url + "/", "open")
        response = requests.post(door_url, headers={"authorization": f"Bearer {self.token}"})
        print(get_pretty_json_string(response.json()))
