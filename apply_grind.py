from parser_file import WizardIdGetter, FileParser, ExcelFile
from parser_enhancement import Enhancement
from parser_rune import RuneParser
from data_mapping import DataMappingCollection
from rune import Rune
import os
import operator
import pandas as pd


class ApplyGrind:
    def __init__(self):

        self.wizard_id = None
        self.rune_list = []
        self.monster_list = []
        self.grind_enchant_list = []
        self.enhancement_inventory = {}
        self.rune_inventory = {}

        self.grind_result = []
        self.enchant_result = []

        self.initialize_enhancement_inventory()

    def initialize_enhancement_inventory(self):
        self.enhancement_inventory = {
            "Grind": {},
            "Enchant": {}
        }

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

        self.construct_enhancement_inventory()
        self.construct_rune_inventory()

        self.apply_enhancements()
        self.format_grind_result()
        self.format_enchant_result()

        excel = self.result_to_excel()
        excel.open_file()

    def set_wizard_id(self):

        wizard_id_getter = WizardIdGetter()
        self.wizard_id = wizard_id_getter.get_wizard_id()

    def create_file_parser_and_set_variables(self):

        file_parser = FileParser(self.wizard_id)

        self.set_rune_list(file_parser)
        self.set_monster_list(file_parser)
        self.set_grind_enchant_list(file_parser)

    def set_rune_list(self, file_parser):
        self.rune_list = file_parser.get_rune_list()

    def set_monster_list(self, file_parser):
        self.monster_list = file_parser.get_unit_list()

    def set_grind_enchant_list(self, file_parser):
        self.grind_enchant_list = file_parser.get_grind_enchant_list()

    def construct_enhancement_inventory(self):
        """
        Parse grind and enchant and sort by rune set
        """

        inventory = self.enhancement_inventory
        for enhancement in self.grind_enchant_list:
            current_e = Enhancement(enhancement)
            inventory = self.group_enhancement_by_set(current_e, inventory)

    @staticmethod
    def group_enhancement_by_set(enhancement, inventory):
        """
        Group each enhancement according to it's set
        """

        if enhancement.set in inventory[enhancement.type]:
            inventory[enhancement.type][enhancement.set].append(enhancement)
        else:
            inventory[enhancement.type][enhancement.set] = [enhancement]

        return inventory

    def construct_rune_inventory(self):
        """
        Parse runes and sort by rune set
        """

        inventory = self.rune_inventory
        for rune in self.rune_list:
            current_rune = Rune(rune)
            rune_user = RuneParser.get_rune_user(self.monster_list, rune["occupied_id"])
            current_rune.set_loc(rune_user)
            self.group_rune_by_set(current_rune, inventory)

    @staticmethod
    def group_rune_by_set(current_rune, inventory):
        """
        Group each RUNE according to it's set
        """

        if current_rune.type in inventory:
            inventory[current_rune.type].append(current_rune)
        else:
            inventory[current_rune.type] = [current_rune]

        return inventory

    def apply_enhancements(self):
        """
        Try to apply all grind and enchant stone for all rune
        """

        grindstone_inventory = self.enhancement_inventory["Grind"]
        enchant_inventory = self.enhancement_inventory["Enchant"]
        rune_inventory = self.rune_inventory

        for rune_set in self.rune_inventory:

            # Only check if there's grind and rune that match
            if rune_set in grindstone_inventory:
                self.apply_grindstones(grindstone_inventory[rune_set], rune_inventory[rune_set])

            if rune_set in enchant_inventory:
                self.apply_enchantgems(enchant_inventory[rune_set], rune_inventory[rune_set])

    def apply_grindstones(self, grindstones, runes):
        """
        :param grindstones: usable grindstones
        :type grindstones: list
        :param runes: usable runes
        :type runes: list
        :return: list of runes and corresponding grindstones
        :rtype: list
        """

        self.sort_grindstones_and_runes(grindstones, runes)
        is_checked_and_failed_table = RuneParser.create_substats_map(default=False)

        for grindstone in grindstones:

            is_applicable = False

            # By pass if the subs checked and failed
            if is_checked_and_failed_table[grindstone.stat]:
                continue

            for rune in runes:

                if self.grind_applicable(grindstone, rune):
                    # If it's applicable, format and append the result
                    self.grind_result += self.format_applying_grind(grindstone, rune)

                    # Make sure same substat from a rune won't get grind using two different grind
                    self.virtually_apply_grind(grindstone, rune)
                    is_applicable = True

                    # Continue to next grindstone
                    break

            # If this kind of rune is unusable, skip those which has same stats, and is same or even lower grade
            if not is_applicable:
                is_checked_and_failed_table[grindstone.stat] = True

    @staticmethod
    def sort_grindstones_and_runes(grindstones, runes):
        """
        Sort the grindstones by grade and stat (grade is most sorted), and sort the runes by efficiency
        """

        grindstones.sort(key=operator.attrgetter('stat'))
        grindstones.sort(key=operator.attrgetter('grade_int'), reverse=True)
        runes.sort(key=operator.attrgetter('efficiency_without_grind'), reverse=True)

    @staticmethod
    def grind_applicable(grindstone, rune, eff_threshold=0.73):
        """
        Check whether a grind can be used and passed certain constraints
        :param grindstone: which grindstone to be used
        :type grindstone: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        :param eff_threshold: minimum efficiency-without-grind, for a rune to be consider grinding
        :type eff_threshold: float
        :return: is grind usable
        :rtype: bool
        """

        # Bad rune should not be grinded
        if rune.exp_efficiency_without_grind <= eff_threshold:
            return False

        # Check the rune's substat
        substat_to_be_grinded = rune.grind_values[grindstone.stat]

        # Rune doesn't have grindstone stat
        if substat_to_be_grinded is None:
            return False

        # That substat is already grinded from before
        elif substat_to_be_grinded == "Applied":
            return False

        elif grindstone.stat == "SPD":

            if grindstone.grade == "Hero" or grindstone.grade == "Legend":
                return substat_to_be_grinded < grindstone.max_value - 1  # 2 Point gap
            else:
                return substat_to_be_grinded < grindstone.max_value  # 1 Point gap

        elif "flat" in grindstone.stat:
            return substat_to_be_grinded < grindstone.max_value * 0.85

        else:

            if grindstone.grade == "Legend":
                return substat_to_be_grinded < grindstone.max_value - 3  # 4 Point gap

            elif grindstone.grade == "Hero":
                return substat_to_be_grinded < grindstone.max_value - 2  # 3 Point gap

            else:
                return substat_to_be_grinded < grindstone.max_value - 1 # 2 Point gap

    @staticmethod
    def format_applying_grind(grindstone, rune):
        """
        Reshape for printout
        :param grindstone: grind to be used
        :type grindstone: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        :return: tuples of rune and grind data, for usable grind
        :rtype: tuples
        """
        _separator = None

        rune_data = (rune.type,
                     rune.slot,
                     rune.grade,
                     rune.base_grade,
                     rune.stars,
                     rune.level,
                     rune.main,
                     rune.innate,
                     rune.substats,
                     rune.efficiency,
                     rune.exp_efficiency,
                     rune.efficiency_without_grind,
                     rune.exp_efficiency_without_grind,
                     rune.loc,
                     _separator)

        grind_data = (grindstone.set,
                      grindstone.grade,
                      grindstone.stat)

        return [rune_data + grind_data]

    @staticmethod
    def virtually_apply_grind(grindstone, rune):
        """
        Remove that substat virtually so it won't get upgraded again
        :param grindstone: which grindstone to be used
        :type grindstone: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        """

        rune.grind_values[grindstone.stat] = "Applied"

    def apply_enchantgems(self, enchantgems, runes):
        """
        :param enchantgems: usable enchantgems
        :type enchantgems: list
        :param runes: usable runes
        :type runes: list
        :return: list of runes and corresponding enchantgems
        :rtype: list
        """

        self.sort_enchants(enchantgems)
        checked_and_failed = RuneParser.create_substats_map(default=False)

        for enchantgem in enchantgems:

            is_applicable = False

            # By pass if the subs checked and failed
            if checked_and_failed[enchantgem.stat]:
                continue

            for rune in runes:

                if self.enchant_applicable(enchantgem, rune):
                    # If it's applicable, format and append the result
                    self.enchant_result += self.format_applying_enchant(enchantgem, rune)
                    is_applicable = True

            # If this kind of rune is unusable, skip those which has same stats, and is same or even lower grade
            if not is_applicable:
                checked_and_failed[enchantgem.stat] = True

    @staticmethod
    def sort_enchants(enchantgems):
        """
        Sort the enchantgem by grade and stat (grade is most sorted), and sort the runes by efficiency
        """

        enchantgems.sort(key=operator.attrgetter('stat'))
        enchantgems.sort(key=operator.attrgetter('grade_int'), reverse=True)

    @staticmethod
    def enchant_applicable(enchantgem, rune):
        """
        Check whether a enchantgem can be used
        :param enchantgem: which enchantgem to be used
        :type enchantgem: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        :return: is enchantgem usable
        :rtype: bool
        """

        # If runes is enchanted already (assumption that enchant into good stat)
        if rune.enchant_type is not None:
            return False

        owned_stats = rune.get_owned_all_stats_type()

        # If the stone stat already exist
        if enchantgem.stat in owned_stats:
            return False

        max_roll_flat_atk = DataMappingCollection.get_rune_sub_stat_max_roll('ATK flat')
        max_roll_flat_def = DataMappingCollection.get_rune_sub_stat_max_roll('DEF flat')
        max_roll_flat_hp = DataMappingCollection.get_rune_sub_stat_max_roll('HP flat')

        # If there exist a flat stat without any roll into it (best scenario)
        if rune.grade == 'L':
            for substat in rune.substats:

                if substat[0] == "ATK flat" and substat[1] <= max_roll_flat_atk:
                    return True
                elif substat[0] == "DEF flat" and substat[1] <= max_roll_flat_def:
                    return True
                elif substat[0] == "HP flat" and substat[1] <= max_roll_flat_hp:
                    return True

        # Since it's not legend (hero or below), it's not going to be reap,
        # So might as well enchant the flat stat if it's feasible (no more than 1 roll into flat)
        else:
            for substat in rune.substats:

                if substat[0] == "ATK flat" and substat[1] <= max_roll_flat_atk * 2:
                    return True
                elif substat[0] == "DEF flat" and substat[1] <= max_roll_flat_def * 2:
                    return True
                elif substat[0] == "HP flat" and substat[1] <= max_roll_flat_hp * 2:
                    return True

    @staticmethod
    def format_applying_enchant(enchantgem, rune):
        """
        Reshape for printout
        :param enchantgem: enchantgem to be used
        :type enchantgem: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        :return: tuples of rune and enchant data, for usable enchantgem
        :rtype: tuples
        """
        _separator = None

        rune_data = (rune.type,
                     rune.slot,
                     rune.grade,
                     rune.base_grade,
                     rune.stars,
                     rune.level,
                     rune.main,
                     rune.innate,
                     rune.substats,
                     rune.efficiency,
                     rune.exp_efficiency,
                     rune.efficiency_without_grind,
                     rune.exp_efficiency_without_grind,
                     rune.loc,
                     _separator)

        enchant_data = (enchantgem.set,
                        enchantgem.grade,
                        enchantgem.stat,
                        enchantgem.id)

        return [rune_data + enchant_data]

    def format_grind_result(self):
        """
        Convert grind result data to pandas dataframe
        """

        columns_name = self.get_pd_column_name("Grind")
        grind_result_pd = pd.DataFrame(self.grind_result, columns=columns_name)
        grind_result_pd_sorted = grind_result_pd.sort_values(by=['Type', 'Exp eff'], ascending=[True, False])

        self.grind_result = grind_result_pd_sorted

    def format_enchant_result(self):
        """
        Convert enchant result data to pandas dataframe
        """

        columns_name = self.get_pd_column_name("Enchant")
        enchant_result_pd = pd.DataFrame(self.enchant_result, columns=columns_name)
        enchant_result_pd_sorted = enchant_result_pd.sort_values(by=['Id', 'Exp eff'], ascending=[True, False])

        self.enchant_result = enchant_result_pd_sorted

    @staticmethod
    def get_pd_column_name(data_name):
        """
        :param data_name: type of data contained in the table
        :type data_name: str
        :return: table columns header / columns name
        :rtype: tuple of str
        """

        columns_name = None

        if data_name == "Grind":

            columns_name = ('Type', 'Slot', 'Grade', 'Base', 'Stars', 'Lv', 'Main', 'Innate',
                            'Substats', 'Eff', 'Exp eff', 'Ori-Eff', 'Ori-Exp eff', "Loc", "",
                            'GType', 'Grade', 'Stat')

        elif data_name == "Enchant":

            columns_name = ('Type', 'Slot', 'Grade', 'Base', 'Stars', 'Lv', 'Main', 'Innate',
                            'Substats', 'Eff', 'Exp eff', 'Ori-Eff', 'Ori-Exp eff', "Loc", "",
                            'Type', 'Enchant Grade', 'Stat', 'Id')

        return columns_name

    def result_to_excel(self):

        excel = ExcelFile(filename='{} applying_grinds.xlsx'.format(self.wizard_id),
                          dataframes=[self.grind_result, self.enchant_result],
                          sheets_name=['Grinds', 'Enchant'])

        return excel


if __name__ == '__main__':
    app = ApplyGrind()
    app.start()
