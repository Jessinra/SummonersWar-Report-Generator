from parser_file import get_wizard_id, parse_file, write_to_excel, datafame_to_sheet
from parser_enhancement import Enhancement
from parser_rune import Rune, get_rune_user
from parser_format import excel_formatting
import os
import operator
import pandas as pd


def parse_enhancement(enhancement_list):

    # Parse the grindstones and enchantstones
    inventory = {
        "Grind": {},
        "Enchant": {}
    }

    for enhancement in enhancement_list:
        current_enhancement = Enhancement(enhancement)

        # Group each enhancement according to it's set
        if current_enhancement.set in inventory[current_enhancement.type]:
            inventory[current_enhancement.type][current_enhancement.set].append(current_enhancement)
        else:
            inventory[current_enhancement.type][current_enhancement.set] = [current_enhancement]

    return inventory

def apply_grindstones(grindstones, runes):
    """
    :param grindstones: usable grindstones
    :type grindstones: list
    :param runes: usable runes
    :type runes: list
    :return: list of runes and corresponding grindstones
    :rtype: list
    """

    def grind_applicable(grindstone, rune, eff_threshold=0.75):
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

        # Do several condition checking for decision making
        if substat_to_be_grinded is None:
            return False
            
        elif substat_to_be_grinded == "Applied":
            return False

        elif grindstone.stat == "SPD":

            if grindstone.grade == "Hero" or grindstone.grade == "Legend":
                return substat_to_be_grinded < grindstone.max_value - 1
            else:
                return substat_to_be_grinded < grindstone.max_value

        elif "flat" in grindstone.stat:
            return substat_to_be_grinded < grindstone.max_value * 0.85

        else:

            if grindstone.grade == "Hero" or grindstone.grade == "Legend":
                return substat_to_be_grinded < grindstone.max_value - 2
            else:
                return substat_to_be_grinded < grindstone.max_value - 1

    def virtually_apply_grind(grindstone, rune):
        """
        Remove that substat virtually so it won't get upgraded again
        :param grindstone: which grindstone to be used
        :type grindstone: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        """

        rune.grind_values[grindstone.stat] = "Applied"

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

        return rune_data + grind_data

    # Sort the grindstones by grade and stat (grade is most sorted), and sort the runes by efficiency
    grindstones.sort(key=operator.attrgetter('stat'))
    grindstones.sort(key=operator.attrgetter('grade_int'), reverse=True)
    runes.sort(key=operator.attrgetter('efficiency_without_grind'), reverse=True)

    applied = []
    checked_and_failed = {

        "SPD": False,
        "ATK%": False,
        "HP%": False,
        "DEF%": False,
        # "CRate": False,
        # "CDmg": False,
        # "RES": False,
        # "ACC": False,
        "ATK flat": False,
        "HP flat": False,
        "DEF flat": False,
    }

    for grindstone in grindstones:

        # Flag to mark if certain grind is successfully used or not
        applicable = False

        # By pass if the subs checked and failed
        if checked_and_failed[grindstone.stat]:
            continue

        for rune in runes:

            if grind_applicable(grindstone, rune):

                # If it's applicable, format and append the result
                formatted_result = format_applying_grind(grindstone, rune)
                applied.append(formatted_result)

                # Make sure same substat from a rune won't get grind using two different grind
                virtually_apply_grind(grindstone, rune)

                applicable = True

                # Continue to next grindstone
                break

        # If this kind of rune is unusable, skip those which has same stats, and is same or even lower grade
        if not applicable:
            checked_and_failed[grindstone.stat] = True

    return applied


def apply_enchantstones(enchantstones, runes):

    def enchant_applicable(enchantstone, rune):
        
        # If runes is enchanted already (assumtion that enchant into good stat)
        if rune.enchant_type is not None:
            return False

        owned_stats = rune._get_owned_all_stats_type()
        
        # If the stone stat already exist
        if enchantstone.stat in owned_stats:
            return False

        max_roll_flat_atk = 20
        max_roll_flat_def = 20
        max_roll_flat_hp = 375

        # If there exist a flat stat without any roll into it
        if rune.grade == 'L':
            for substat in rune.substats:

                if substat[0] == "ATK flat" and substat[1] <= max_roll_flat_atk:
                    return True
                elif substat[0] == "DEF flat" and substat[1] <= max_roll_flat_def:
                    return True
                elif substat[0] == "HP flat" and substat[1] <= max_roll_flat_hp:
                    return True
        
        # Since it's not legend, it's not going to be reap
        else:
            for substat in rune.substats:

                if substat[0] == "ATK flat" and substat[1] <= max_roll_flat_atk*2:
                    return True
                elif substat[0] == "DEF flat" and substat[1] <= max_roll_flat_def*2:
                    return True
                elif substat[0] == "HP flat" and substat[1] <= max_roll_flat_hp*2:
                    return True

    def format_applying_enchant(enchantstone, rune):
        """
        Reshape for printout
        :param enchantstone: enchantstone to be used
        :type enchantstone: Enhancement
        :param rune: which rune to be checked
        :type rune: Rune
        :return: tuples of rune and enchant data, for usable enchantstone
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

        enchant_data = (enchantstone.set,
                        enchantstone.grade,
                        enchantstone.stat,
                        enchantstone.id)

        return rune_data + enchant_data

    # Sort the enchantstone by grade and stat (grade is most sorted), and sort the runes by efficiency
    enchantstones.sort(key=operator.attrgetter('stat'))
    enchantstones.sort(key=operator.attrgetter('grade_int'), reverse=True)
   
    applied = []
    checked_and_failed = {

        "SPD": False,
        "ATK%": False,
        "HP%": False,
        "DEF%": False,
        "CRate": False,
        "CDmg": False,
        "RES": False,
        "ACC": False,
        "ATK flat": False,
        "HP flat": False,
        "DEF flat": False,
    }

    for enchantstone in enchantstones:

        # Flag to mark if certain enchantstone is successfully used or not
        applicable = False

        # By pass if the subs checked and failed
        if checked_and_failed[enchantstone.stat]:
            continue

        for rune in runes:

            if enchant_applicable(enchantstone, rune):

                # If it's applicable, format and append the result
                formatted_result = format_applying_enchant(enchantstone, rune)
                applied.append(formatted_result)

                applicable = True

        # If this kind of rune is unusable, skip those which has same stats, and is same or even lower grade
        if not applicable:
            checked_and_failed[enchantstone.stat] = True

    return applied


def get_pd_column_name(data_name):

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

def parse_rune(rune_list, monster_list):

    # Parse the runes
    rune_inventory = {}
    for rune in rune_list:

        current_rune = Rune(rune)
        current_rune.set_loc(get_rune_user(monster_list, rune["occupied_id"]))

        # Group each RUNE according to it's set
        if current_rune.type in rune_inventory:
            rune_inventory[current_rune.type].append(current_rune)
        else: 
            rune_inventory[current_rune.type] = [current_rune]

    return rune_inventory


def apply_enhancements(enhancement_inventory, rune_inventory):

    grindstone_inventory = enhancement_inventory["Grind"]
    enchant_inventory = enhancement_inventory["Enchant"]

    grind_result = []
    enchant_result = []

    for rune_set in rune_inventory:

        # Only check if there's grind and rune that match
        if rune_set in grindstone_inventory:
            grind_result += apply_grindstones(grindstones=grindstone_inventory[rune_set], runes=rune_inventory[rune_set])

        if rune_set in enchant_inventory:
            enchant_result += apply_enchantstones(enchantstones=enchant_inventory[rune_set], runes=rune_inventory[rune_set])

    return grind_result, enchant_result



def format_grind_result(grind_result):

    # Convert grind result data to pandas dataframe
    columns_name = get_pd_column_name("Grind")
    grind_result_pd = pd.DataFrame(grind_result, columns=columns_name)
    grind_result_pd_sorted = grind_result_pd.sort_values(by=['Type', 'Exp eff'], ascending=[True, False])
    
    return grind_result_pd_sorted


def format_enchant_result(enchant_result):

    # Convert enchant result data to pandas dataframe
    columns_name = get_pd_column_name("Enchant")
    enchant_result_pd = pd.DataFrame(enchant_result, columns=columns_name)
    enchant_result_pd_sorted = enchant_result_pd.sort_values(by=['Id', 'Exp eff'], ascending=[True, False])

    return enchant_result_pd_sorted

try:

    if __name__ == '__main__':

        wizard_id = get_wizard_id()
        rune_list, monster_list, enhancement_list = parse_file(wizard_id)

        enhancement_inventory = parse_enhancement(enhancement_list)
        rune_inventory = parse_rune(rune_list, monster_list)

        grind_result, enchant_result = apply_enhancements(enhancement_inventory, rune_inventory)

        formated_grind_result = format_grind_result(grind_result)
        formated_enchant_result = format_enchant_result(enchant_result)

        filename = '{} applying_grinds.xlsx'.format(wizard_id)
        dataframes = [formated_grind_result, formated_enchant_result]
        sheets_name = ['Grinds', 'Enchant']
        write_to_excel(filename, dataframes, sheets_name)

except Exception as e:
    print(e)
    os.system("pause")
    raise e
