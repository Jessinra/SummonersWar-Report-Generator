from parser_rune import RuneParser
from parser_file import WizardIdGetter, FileParser, ExcelFile
from rune import Rune
import pandas as pd
import os


class RuneDeletePicker:
    def __init__(self):

        self.wizard_id = None
        self.rune_list = []
        self.monster_list = []
        self.grind_enchant_list = []
        self.parsed_rune_result = []
        self.monster_eff_result = []

    def start(self):

        try:
            self.run_main_function()

        except Exception as e:
            self.handle_error(e)

    @staticmethod
    def handle_error(error):

        print(error)
        os.system("pause")

    def run_main_function(self):

        self.set_wizard_id()
        self.create_file_parser_and_set_variables()

        self.parse_runes_and_monster_eff()
        self.format_parsed_runes()
        self.format_monster_eff()

        excel = self.result_to_excel()
        excel.open_file()

    def set_wizard_id(self):

        wizard_id_getter = WizardIdGetter()
        self.wizard_id = wizard_id_getter.get_wizard_id()

    def create_file_parser_and_set_variables(self):

        file_parser = FileParser(self.wizard_id)

        self.set_rune_list(file_parser)
        self.set_monster_list(file_parser)

    def set_rune_list(self, file_parser):

        self.rune_list = file_parser.get_rune_list()

    def set_monster_list(self, file_parser):

        self.monster_list = file_parser.get_unit_list()

    def parse_runes_and_monster_eff(self):
        """
        Parse runes and calculate monster efficiency
        """

        monster_eff_map = {}
        monster_exp_eff_map = {}

        for rune in self.rune_list:
            current_rune = Rune(rune)
            current_rune.set_loc(RuneParser.get_rune_user(self.monster_list, rune["occupied_id"]))

            self.parsed_rune_result += self.format_rune(current_rune)

            # Can't calculate monster eff if the rune is not equipped on a monster
            if not current_rune.is_equiped():
                continue

            monster_eff_map = self.increment_dict_value(monster_eff_map, current_rune.loc, current_rune.efficiency)
            monster_exp_eff_map = self.increment_dict_value(monster_exp_eff_map, current_rune.loc, current_rune.exp_efficiency_15)

        # Average it
        for monster in monster_eff_map:
            average_real_efficiency = monster_eff_map[monster] / 6
            average_expected_efficiency = monster_exp_eff_map[monster] / 6

            self.monster_eff_result.append((monster, average_real_efficiency, average_expected_efficiency))

    @staticmethod
    def format_rune(current_rune):
        """
        Reshape for printout
        """

        _separator_ = None

        rune_data = (current_rune.rune_set,
                     current_rune.slot,
                     current_rune.grade,
                     current_rune.base_grade,
                     current_rune.stars,
                     current_rune.level,
                     current_rune.main,
                     current_rune.innate,
                     _separator_)
        rune_data += current_rune.dense_substats
        rune_data += (_separator_,
                      current_rune.efficiency,
                      current_rune.exp_efficiency_12,
                      current_rune.exp_efficiency_15,
                      current_rune.efficiency_without_grind,
                      current_rune.exp_efficiency_12_without_grind,
                      current_rune.loc)

        return [rune_data]

    @staticmethod
    def increment_dict_value(dictionary, dict_key, dict_value):

        if dict_key in dictionary:
            dictionary[dict_key] += dict_value
        else:
            dictionary[dict_key] = dict_value

        return dictionary

    def format_parsed_runes(self):
        """
        Convert rune data to pandas data frame
        """

        columns_name = self.get_pd_column_name("Rune")
        parsed_runes_pd = pd.DataFrame(self.parsed_rune_result, columns=columns_name)
        parsed_runes_pd_sorted = parsed_runes_pd.sort_values(by=['Exp eff 15'])

        self.parsed_rune_result = parsed_runes_pd_sorted

    def format_monster_eff(self):
        """
        Convert monster eff data to pandas data frame
        """

        columns_name = self.get_pd_column_name("Monster eff")
        monster_eff_pd = pd.DataFrame(self.monster_eff_result, columns=columns_name)
        monster_eff_sorted = monster_eff_pd.sort_values(by=['avg real eff'], ascending=False)

        self.monster_eff_result = monster_eff_sorted

    @staticmethod
    def get_pd_column_name(data_name):
        """
        :param data_name: type of data contained in the table
        :type data_name: str
        :return: table columns header / columns name
        :rtype: tuple of str
        """

        columns_name = None

        if data_name == "Rune":
            columns_name = ('Type', 'Slot', 'Grade', 'Base', 'Stars', 'Lv', 'Main', 'Innate', '')
            columns_name += ('Spd', 'Atk%', 'Hp%', 'Def%', 'Crate', 'Cdmg', 'Res', 'Acc', 'Atk+', 'Hp+', 'Def+')
            columns_name += ('', 'Eff', 'Exp eff 12', 'Exp eff 15', 'Ori-Eff', 'Ori-Exp eff 12', "Loc")

        elif data_name == "Monster eff":
            columns_name = ('monster', 'avg real eff', 'avg exp eff 15')

        return columns_name

    def result_to_excel(self):

        excel = ExcelFile(filename='{} rune_eff.xlsx'.format(self.wizard_id),
                          dataframes=[self.parsed_rune_result, self.monster_eff_result],
                          sheets_name=['Rune', 'Monster eff'])
        return excel


if __name__ == '__main__':
    app = RuneDeletePicker()
    app.start()
