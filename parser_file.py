import json
import os
import sys
from parser_mons import generate_monsters
from parser_format import excel_formatting

 # enable header formatting
import pandas.io.formats.excel
pandas.io.formats.excel.header_style = None


def get_wizard_id(default_wizard_id=None):
    """
    Handle input and validating user input if necessary, returning wizard id 
    """

    wizard_id = None

    # prompt user id if not given default one
    if default_wizard_id is None:

        # Try to open existing file
        try:
            with open("default_id.txt", encoding="utf-8") as f:
                for line in f:
                    wizard_id = line.strip()
                    break

            create_file = False

        # If file doesn't exist yet, prompt user for input and cache input
        except:
            wizard_id = input("<This will be stored into default_id.txt>\nInput your id (example 101222 or visit-110200) : ")
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
    """
    Parse Json file into three separate json (rune, monster, enhancement)
    :return: list of runes, list of monster, list of enhancement
    :rtype: list, list, list
    """
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

    try:
        grind_enchant_list = json_data["rune_craft_item_list"]

    except:
        grind_enchant_list = []

    return rune_list, monster_list, grind_enchant_list


def write_to_excel(filename, dataframes, sheets_name):

   
    success = False
    while not success:

        try:

            writer = pandas.ExcelWriter(filename, engine='xlsxwriter')
            workbook = writer.book

            for i in range(0, len(dataframes)):
                datafame_to_sheet(dataframe=dataframes[i], sheet_name=sheets_name[i], writer=writer, workbook=workbook)

            writer.save()
            os.startfile(filename)
            success = True

        except:
            print("File is open, close it first")
            os.system("pause")


def datafame_to_sheet(dataframe, writer, workbook, sheet_name):

    dataframe.to_excel(writer, sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]
    excel_formatting(workbook, worksheet, cond=sheet_name)
