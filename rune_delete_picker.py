from parser_rune import Rune, get_rune_user
from parser_file import get_wizard_id, parse_file, write_to_excel
from parser_mons import store_monster_eff
import pandas as pd
import os


def format_rune(current_rune):
    """
    Reshape for printout
    """

    _separator_ = None

    rune_data = (current_rune.type,
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
                  current_rune.exp_efficiency,
                  current_rune.efficiency_without_grind,
                  current_rune.exp_efficiency_without_grind,
                  current_rune.loc)

    return rune_data


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
        columns_name += ('', 'Eff', 'Exp eff', 'Ori-Eff', 'Ori-Exp eff', "Loc")

    elif data_name == "Monster eff":
        columns_name = ('monster', 'avg real eff', 'avg exp eff')

    return columns_name


def parse_runes_and_monster_eff(rune_list):
    """
    Parse runes and calculate monster efficiency
    :param rune_list: list of raw rune data
    :type rune_list: list
    :return: parsed runes, monster efficiency
    :rtype: (list, list)
    """

    parsed_runes = []
    monster_eff = {}
    monster_exp_eff = {}

    for rune in rune_list:
        current_rune = Rune(rune)
        current_rune.set_loc(get_rune_user(monster_list, rune["occupied_id"]))

        store_monster_eff(monster_eff, current_rune.loc, current_rune.efficiency)
        store_monster_eff(monster_exp_eff, current_rune.loc, current_rune.exp_efficiency)

        formatted_result = format_rune(current_rune)
        parsed_runes.append(formatted_result)

    # Average it
    monster_eff_avg = []

    for monster in monster_eff:
        avg_real_eff = monster_eff[monster] / 6
        avg_exp_eff = monster_exp_eff[monster] / 6

        monster_eff_avg.append((monster, avg_real_eff, avg_exp_eff))

    return parsed_runes, monster_eff_avg


def format_parsed_runes(parsed_runes):
    """
    :return: formatted parsed runes
    :rtype: pandas.DataFrame
    """

    # Convert rune data to pandas data frame
    columns_name = get_pd_column_name("Rune")
    parsed_runes_pd = pd.DataFrame(parsed_runes, columns=columns_name)
    parsed_runes_pd_sorted = parsed_runes_pd.sort_values(by=['Exp eff'])

    return parsed_runes_pd_sorted


def format_monster_eff(monster_eff_avg):
    """
    :return: formatted monsters efficiency
    :rtype: pandas.DataFrame
    """

    # Convert monster eff data to pandas data frame
    columns_name = get_pd_column_name("Monster eff")
    monster_eff_pd = pd.DataFrame(monster_eff_avg, columns=columns_name)
    monster_eff_sorted = monster_eff_pd.sort_values(by=['avg real eff'], ascending=False)

    return monster_eff_sorted


try:

    if __name__ == '__main__':
        wizard_id = get_wizard_id()
        rune_list, monster_list, grind_enchant_list = parse_file(wizard_id)

        parsed_runes, monster_eff_avg = parse_runes_and_monster_eff(rune_list)

        formatted_parsed_runes = format_parsed_runes(parsed_runes)
        formatted_monster_eff = format_monster_eff(monster_eff_avg)

        filename = '{} rune_eff.xlsx'.format(wizard_id)
        dataframes = [formatted_parsed_runes, formatted_monster_eff]
        sheets_name = ['Rune', 'Monster eff']
        write_to_excel(filename, dataframes, sheets_name)

except Exception as e:
    print(e)
    os.system("pause")
    raise e
