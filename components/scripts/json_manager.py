import json


def save_json(location, json_object:dict) -> None:
    with open(location, "w") as json_out:
        json.dump(json_object, json_out, indent=4)



def open_json(location) -> dict:
    with open(location, "r") as json_in:
        json_object = json.load(json_in)
    
    return json_object