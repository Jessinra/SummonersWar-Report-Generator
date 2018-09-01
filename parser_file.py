from parser_mons import generate_monsters
from parser_format import excel_formatting
import json
import os
import sys
import pandas.io.formats.excel

pandas.io.formats.excel.header_style = None

class WizardIdGetter:

    default_filename = "default_id.txt"

    def __init__(self):

        self.wizard_id = None

        while not self._is_wizard_id_valid():
            self._display_wizard_id_invalid()
            self._set_wizard_id()
        
        self._store_new_wizard_id()

    def _display_wizard_id_invalid(self):

        error_message = "Your current wizard id is invalid, please input a valid one\n"
        print(error_message)

    def _set_wizard_id(self):

        try:
            self.wizard_id = self._read_cached_wizard_id()
        except:
            self.wizard_id = self._ask_user_wizard_id()

    def _read_cached_wizard_id(self):

        filename = WizardIdGetter.default_filename
        first_line = open(filename, encoding="utf-8").readline()
        return first_line.strip()

    def _ask_user_wizard_id(self, ):

        display_text = "<Your wizard id will be stored in this folder>\n\nPlease input your id (example 101222 or visit-110200) : "

        wizard_id = input(display_text)
        return wizard_id

    def _store_new_wizard_id(self):

        filename = WizardIdGetter.default_filename
        with open(filename, "w") as f:
            f.write(self.wizard_id)

    def _is_wizard_id_valid(self):

        if self.wizard_id is None:
            return False    # Not initialized
        else:
            return self.wizard_id.isdigit() or "visit-" in self.wizard_id

    def get_wizard_id(self):   
        return self.wizard_id
            

def parse_file(wizard_id):
    """
    Parse Json file into three separate json (rune, monster, enhancement)
    :return: list of runes, list of monster, list of enhancement
    :rtype: list, list, list
    """

    filename = "{}.json".format(wizard_id)
    json_data = read_json(filename)

    monsters = parse_monster_section(json_data)
    monster_list = generate_monsters(monsters)
    
    storage_runes = parse_runes_in_storage(json_data)
    equiped_runes = parse_runes_equiped(monsters)
    rune_list = storage_runes + equiped_runes

    grind_enchant_list = parse_enhancement_section(json_data)

    return rune_list, monster_list, grind_enchant_list

def read_json(filename):
    
    try:
        return json.load(open(filename, encoding="utf-8"))
    except:
        raise

def parse_monster_section(json_data):

    try:
        return json_data["unit_list"]
    except:
        return json_data["friend"]["unit_list"]

def parse_runes_in_storage(json_data):

    try:
        return json_data["runes"]
    except:
        return []

def parse_runes_equiped(monsters):

    rune_list = []

    for monster in monsters:
        if is_monster_has_rune(monster):
            rune_list += get_runes_from_monster(monster)

    return rune_list

def is_monster_has_rune(monster):
    return len(monster["runes"]) > 0

def get_runes_from_monster(monster):

    monster_runes = monster["runes"]

    # Format : [{rune data}, {rune data}, {rune data}]
    if isinstance(monster_runes, list):
        return get_runes_from_list(monster_runes)

    # Format : {"XX": {rune data}, "XX": {rune data}, "XX": {rune data}}
    elif isinstance(monster_runes, dict):
        return get_runes_from_dict(monster_runes)

    else:
        return []

def get_runes_from_list(monster_runes):

    rune_list = []
    for rune in monster_runes:
        rune_list.append(rune)
    return rune_list

def get_runes_from_dict(monster_runes):

    rune_list = []
    for key in monster_runes:
        rune_list.append(monster_runes[key])
    return rune_list

def parse_enhancement_section(json_data):

    try:
        return json_data["rune_craft_item_list"]
    except:
        return []




class ExcelFile:

    def __init__(self, filename, dataframes, sheets_name):

        self.filename = filename
        self.dataframes = dataframes
        self.sheet_names = sheets_name
        self.writer = None
        self.workbook = None

        self.write_to_excel()

    def write_to_excel(self):

        success = False
        while not success:
            success = self.try_to_construct_excel()

    def try_to_construct_excel(self):

        try:
            self.set_writer()
            self.set_workbook()
            self.dataframes_to_sheet()
            self.save()

            successfully_constructed = True

        except Exception as e:
            self.handle_exception(e)

            successfully_constructed = False

        finally:
            return successfully_constructed

    def set_writer(self):
        self.writer = pandas.ExcelWriter(self.filename, engine='xlsxwriter')

    def set_workbook(self):
        self.workbook = self.writer.book

    def dataframes_to_sheet(self):
        for i in range(0, len(self.dataframes)):
            dataframe_to_sheet(dataframe=self.dataframes[i],
                               sheet_name=self.sheet_names[i], 
                               writer=self.writer, 
                               workbook=self.workbook)

    def save(self):
        self.writer.save()

    def handle_exception(self, exception):
        print(exception)
        os.system("pause")

    def open_file(self):
        os.startfile(self.filename)
    
def dataframe_to_sheet(dataframe, sheet_name, writer, workbook):
    """
    Convert dataframe to excel sheet
    """

    dataframe.to_excel(writer, sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]
    excel_formatting(workbook, worksheet, cond=sheet_name)