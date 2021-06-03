import json
import os

def get_race_choice_message():
    dirname = os.getcwd()
    print(dirname)
    path = os.path.join(dirname, 'dokipro1/assets/keiba_choice.json')
    print(path)
    data = open(path, mode='r')
    message = json.load(data)
    data.close()
    return message