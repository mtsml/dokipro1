import json


def get_race_choice_message():
    data = open('assets/keiba_choice.json', mode='r')
    message = json.load(data)
    data.close()
    return message