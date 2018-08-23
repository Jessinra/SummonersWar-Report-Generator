import json
import os
import sys
from parser_mons import generate_monsters

# insert your wizard code as string here ex : "123452"
default_wizard_id = None

def get_wizard_id():
    """
    Handle input and validating user input if necessary, returning wizard id 
    """

    # prompt user id if not given default one
    if default_wizard_id is None:
        try:
            with open("default_id.txt", encoding="utf-8") as f:
                
                for line in f:
                    wizard_id = line.strip()
                    break

            create_file = False
                    
        except:
            wizard_id = input("<this will be stored into default_id.txt>\nInput your id (example 101222 or visit-110200) : ")
            create_file = True

    else:
        wizard_id = default_wizard_id
        create_file = False

    # validating default id
    try:
        int(wizard_id)

    except Exception as e:
        if "visit-" in wizard_id:
            pass
        else:
            print("wrong input:", e)
            os.system("pause")
            sys.exit(0)

    # Store default id for later use
    if create_file:
        f = open("default_id.txt", "w")
        f.write(wizard_id)

    return wizard_id


def parse_file(wizard_id):

    try:
        with open("{}.json".format(wizard_id), encoding="utf-8") as f:
            json_data = json.load(f)
    except:
        raise

    # storage runes
    try:
        rune_list = json_data["runes"]

    except:
        rune_list = []

    try:
        grind_enchant_list = json_data["rune_craft_item_list"]
    
    except:
        grind_enchant_list = []

    # equipped runes
    try:
        monsters = json_data["unit_list"]

    except:
        monsters = json_data["friend"]["unit_list"]

    for mons in monsters:
        monster_runes = mons["runes"]
        if len(monster_runes) > 0:
            for rune in monster_runes:

                # there are 2 different format (?)
                if len(rune) <= 2:
                    rune = monster_runes[rune]
                    rune_list.append(rune)
                else:
                    rune_list.append(rune)

    monster_list = generate_monsters(monsters)

    return rune_list, monster_list, grind_enchant_list

