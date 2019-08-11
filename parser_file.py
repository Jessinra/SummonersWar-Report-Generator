from parser_mons import UnitParser
from parser_format import ExcelFormatter
import json
import os
import pandas.io.formats.excel

pandas.io.formats.excel.header_style = None


class WizardIdGetter:
    default_filename = "default_id.txt"

    def __init__(self):

        self.wizard_id = None

        self._set_wizard_id()
        self._make_sure_wizard_id_valid()
        self._store_new_wizard_id()

    def _set_wizard_id(self):

        try:
            self.wizard_id = self._read_cached_wizard_id()
        except:
            self.wizard_id = self._ask_user_wizard_id()

    @staticmethod
    def _read_cached_wizard_id():

        filename = WizardIdGetter.default_filename
        first_line = open(filename, encoding="utf-8").readline().strip()
        return first_line

    @staticmethod
    def _ask_user_wizard_id():

        display_text = "<Your wizard id will be stored in this folder>\n\nPlease input your id (example 101222 or visit-110200) : "
        wizard_id = input(display_text)
        return wizard_id

    def _make_sure_wizard_id_valid(self):

        while not self._is_wizard_id_valid():
            self._display_wizard_id_invalid()
            self._set_wizard_id()

    def _is_wizard_id_valid(self):

        if self.wizard_id is None:
            return False  # Not initialized
        else:
            return self.wizard_id.isdigit() or "visit-" in self.wizard_id

    @staticmethod
    def _display_wizard_id_invalid():

        error_message = "Your current wizard id is invalid, please input a valid one\n"
        print(error_message)

    def _store_new_wizard_id(self):

        filename = WizardIdGetter.default_filename
        with open(filename, "w") as f:
            f.write(self.wizard_id)

    def get_wizard_id(self):

        return self.wizard_id


class FileParser:
    def __init__(self, wizard_id):

        self.json_data = None
        self.monster_list = None
        self.unit_list = None
        self.rune_list = None
        self.grind_enchant_list = None

        self._parse_file(wizard_id)

    def _parse_file(self, wizard_id):

        filename = "{}.json".format(wizard_id)
        self._set_json_data(filename)
        self._set_monster_list()
        self._set_unit_list()
        self._set_rune_list()
        self._set_grind_enchant_list()

    def _set_json_data(self, filename):

        self.json_data = json.load(open(filename, encoding="utf-8"))

    def _set_monster_list(self):

        self.monster_list = self._parse_monster_section()

    def _set_unit_list(self):

        unit_parser = UnitParser()
        unit_parser.parse_units(self.monster_list)
        self.unit_list = unit_parser.get_unit_dict()

    def _parse_monster_section(self):

        try:
            return self.json_data["unit_list"]
        except:
            return self.json_data["friend"]["unit_list"]

    def _set_rune_list(self):

        storage_runes = self._parse_runes_in_storage()
        equipped_runes = self._parse_runes_equiped()
        self.rune_list = storage_runes + equipped_runes

    def _parse_runes_in_storage(self):

        try:
            return self.json_data["runes"]
        except:
            return []

    def _parse_runes_equiped(self):

        rune_list = []
        for monster in self.monster_list:
            rune_list += FileParser._get_runes_from_monster(monster)

        return rune_list

    @staticmethod
    def _get_runes_from_monster(monster):

        if FileParser._is_monster_has_rune(monster):
            monster_runes = monster["runes"]
            return FileParser._get_runes_from_list_or_dict(monster_runes)
        else:
            return []

    @staticmethod
    def _is_monster_has_rune(monster):

        return len(monster["runes"]) > 0

    @staticmethod
    def _get_runes_from_list_or_dict(monster_runes):

        # Format : [{rune data}, {rune data}, {rune data}]
        if isinstance(monster_runes, list):
            return FileParser._get_runes_from_list(monster_runes)

        # Format : {"XX": {rune data}, "XX": {rune data}, "XX": {rune data}}
        elif isinstance(monster_runes, dict):
            return FileParser._get_runes_from_dict(monster_runes)
        else:
            return []

    @staticmethod
    def _get_runes_from_list(monster_runes):

        rune_list = []
        for rune in monster_runes:
            rune_list.append(rune)
        return rune_list

    @staticmethod
    def _get_runes_from_dict(monster_runes):

        rune_list = []
        for key in monster_runes:
            rune_list.append(monster_runes[key])
        return rune_list

    def _set_grind_enchant_list(self):

        try:
            self.grind_enchant_list = self.json_data["rune_craft_item_list"]
        except:
            self.grind_enchant_list = []

    def get_rune_list(self):
        return self.rune_list

    def get_unit_list(self):
        return self.unit_list

    def get_grind_enchant_list(self):
        return self.grind_enchant_list


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

        successfully_constructed = False

        try:
            self.set_writer()
            self.set_workbook()
            self.dataframes_to_sheet()
            self.save()
            successfully_constructed = True

        except Exception as e:
            self.handle_exception(e)

        finally:
            return successfully_constructed

    def set_writer(self):
        self.writer = pandas.ExcelWriter(self.filename, engine='xlsxwriter')

    def set_workbook(self):
        self.workbook = self.writer.book

    def dataframes_to_sheet(self):
        for i in range(0, len(self.dataframes)):
            self.dataframe_to_sheet(dataframe=self.dataframes[i],
                                    sheet_name=self.sheet_names[i])

    def dataframe_to_sheet(self, dataframe, sheet_name):
        """
        Convert dataframe to excel sheet
        """

        dataframe.to_excel(self.writer, sheet_name=sheet_name)
        worksheet = self.writer.sheets[sheet_name]
        ExcelFormatter(self.workbook, worksheet, format_type=sheet_name)

    def save(self):
        self.writer.save()

    @staticmethod
    def handle_exception(exception):
        print(exception)
        os.system("pause")

    def open_file(self):
        os.startfile(self.filename)
