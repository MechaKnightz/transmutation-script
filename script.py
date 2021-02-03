import requests
from bs4 import BeautifulSoup
from string import ascii_uppercase
import os.path
import pickle
import itertools
import urllib.parse as parse
import urllib.request
from urllib.request import urlopen as req_url
import json
import string
import webbrowser
import time

rare_mods_store = "rare_mods"
corrupted_mods_store = "corrupted_mods"
augment_mods_store = "augment_mods"
rare_mods = "https://warframe.fandom.com/wiki/Category:Rare_Mods"
corrupted_mods = "https://warframe.fandom.com/wiki/Category:Corrupted_Mods"
augment_mods = "https://warframe.fandom.com/wiki/Category:Augment_Mods"

def get_average_price(name):
    print(name)
    parsed = ""
    try:
        main_url = req_url('https://api.warframe.market/v1/items/' + name + '/statistics')
        data = main_url.read()
        parsed = json.loads(data)
    except:
        return None
    try:
        parsed_data = parsed['payload']['statistics_closed']['48hours'][-1]['min_price']
    except:
        try:
            parsed_data = parsed['payload']['statistics_closed']['90days'][-1]['min_price']
        except:
            return 0
    #date_time = parsed['payload']['statistics']['48hours'][-1]['datetime']
    return parsed_data

def get_mods_by_link(link):
    contents = []
    for letter in ascii_uppercase:
        page = requests.get(
            link + "?from=" + letter)
        res = page.content
        contents.append(BeautifulSoup(res, 'html.parser'))

    names = []
    for content in contents:
        mod_elements = content.find_all("a", class_="category-page__member-link")
        names += list(map((lambda element: element.get("title")), mod_elements))

    names = set(names)

    names = set(filter((lambda element: ":" not in element), names))

    return names



if(not os.path.isfile(rare_mods_store)): 
    
    names = get_mods_by_link(rare_mods)

    with open(rare_mods_store, 'wb') as f:
        pickle.dump(names, f)

if(not os.path.isfile(corrupted_mods_store)): 
    
    names = get_mods_by_link(corrupted_mods)
    print(names)

    with open(corrupted_mods_store, 'wb') as f:
        pickle.dump(names, f)

if(not os.path.isfile(augment_mods_store)): 
    
    names = get_mods_by_link(augment_mods)
    print(names)

    with open(augment_mods_store, 'wb') as f:
        pickle.dump(names, f)

rare_mods={}
with open(rare_mods_store, 'rb') as f:
    rare_mods = pickle.load(f)

mods = rare_mods

corrupted_mods={}
with open(corrupted_mods_store, 'rb') as f:
    corrupted_mods = pickle.load(f)

augment_mods={}
with open(augment_mods_store, 'rb') as f:
    augment_mods = pickle.load(f)

f = open("blacklist", "r")
lines = f.read().splitlines()

for mod_name in lines:
    mods.discard(mod_name)

for corrupted_mod in corrupted_mods:
    mods.discard(corrupted_mod)

for augment_mod in augment_mods:
    mods.discard(augment_mod)

for i, mod in enumerate(mods):
    temp = mod
    temp = temp.replace(" (Mod)", "")
    temp = temp.replace(" ", "_")
    temp = temp.lower()
    mods.remove(mod)
    mods.add(temp)

result = []
for mod in mods:
    price = get_average_price(mod)
    print(price)
    if price == None:
        continue
    result.append(price)
    time.sleep(1)

print(sum(result) / len(result))
