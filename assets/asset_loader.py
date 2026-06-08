import json
from classes.engine import Engine
from classes.component import Component


fuels = []
engines = []
components = []
loaded = [False, False, False]

# saving fuels to memory
def load_fuels():
    global fuels
    if loaded[0] == False:
        print("Loading fuels into memory...")
        with open('./library/fuels.json', 'r') as f:
            fuels_data = json.load(f)
        fuels.clear()
        fuels.extend(fuels_data)
        loaded[0] = True
        print("Fuels loaded into memory")

def load_engines():
    if loaded[1] == False:
        print("Loading engines into memory...")
        with open('./library/engines.json', 'r') as f:
            f = json.load(f)
            for a in f:
                engines.append(Engine(a['flow_rate'], a['size_scale'], a['name'], a['material'], a['type'], a['exit_area'], a['exhaust_velocity'], a['asset'], a['height'], a['width'], a['side-offset'], a['fuel_capacity'], a['mass'], a['drag-factor']))
        loaded[1] = True
        print("Engines loaded into memory")

def load_components():
    if loaded[2] == False:
        print("Loading components into memory...")
        with open('./library/components.json', 'r') as f:
            f = json.load(f)
            for a in f:
                components.append(Component(a['name'], a['mass'], a['width'], a['height'], a['x-offset'], a['size_scale'], a['asset'], a['type'], a['fuel_capacity'], a['control_surface'], a['stability_offset'], a['drag-factor']))
        loaded[2] = True
        print("Components loaded into memory")

def init_ram():
    load_fuels()
    load_engines()
    load_components()