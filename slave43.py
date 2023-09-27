import requests
import os
import obsws_python as obs
from deepdiff import DeepDiff
from time import sleep
from copy import copy


client = obs.ReqClient(host='localhost', port=4455, password='3H6XZbvhK4deeaQx', timeout=3)

IP = os.environ.get('IP', 'http://localhost')


def main():
    memory = {}
    while True:
        response = requests.get(IP)
        if not response.ok:
            continue
        data = response.json()

        for scene_name in data.keys():
            for item in data[scene_name]:
                if not (memory.get(scene_name) and check_in_memory(memory[scene_name], item)):
                    try:
                        change_item(scene_name, item)
                    except Exception as e:
                        print(e)
                        print('=' * 50, '\n' * 5)
            memory[scene_name] = data[scene_name]


def check_in_memory(memory, item):
    for item_mem in memory:
        if not DeepDiff(item_mem, item):
            return True
    return False


def check_item(scene_name, source_name):
    items = client.get_scene_item_list(scene_name)
    for item in items.scene_items:
        if item['sourceName'] == source_name:
            return True
    return False


def change_item(scene_name, data):
    if not check_item(scene_name, data['sourceName']):
        client.create_scene_item(scene_name, data['sourceName'])
    item_id = client.get_scene_item_id(scene_name, data['sourceName']).scene_item_id
    client.set_scene_item_enabled(scene_name, item_id, data['sceneItemEnabled'])
    client.set_scene_item_locked(scene_name, item_id, data['sceneItemLocked'])
    client.set_scene_item_index(scene_name, item_id, data['sceneItemIndex'])
    client.set_scene_item_blend_mode(scene_name, item_id, data['sceneItemBlendMode'])
    for trans_item in copy(data['sceneItemTransform']).keys():
        if not data['sceneItemTransform'][trans_item]:
            data['sceneItemTransform'].pop(trans_item)
    client.set_scene_item_transform(scene_name, item_id, data['sceneItemTransform']) 
    
main()