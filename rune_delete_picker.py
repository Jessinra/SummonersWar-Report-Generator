from parser_rune import Rune, get_rune_user
from parser_format import excel_formatting
from parser_file import *
from parser_mons import store_monster_eff
import pandas as pd
import os
import sys


def format_rune_parser(current_rune):
    """
    Reshape for printout
    """

    _separator_ = None  # separator

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

try:

    if __name__ == '__main__':

        wizard_id = get_wizard_id()

        try:
            rune_list, monster_list, grind_enchant_list = parse_file(wizard_id)

        except Exception as e:
            print("aborting.....")
            os.system("pause")
            sys.exit(0)

        whole_rune = []
        monster_eff = {}
        monster_exp_eff = {}

        for rune in rune_list:

            """ ===================================================
                                RUNE SECTION
            ===================================================="""

            current_rune = Rune(rune)
            current_rune.set_loc(get_rune_user(monster_list, rune["occupied_id"]))

            formatted_result = format_rune_parser(current_rune)
            whole_rune.append(formatted_result)

            """ ===================================================
                        MONSTER EFF SECTION
            ===================================================="""
            store_monster_eff(monster_eff, current_rune.loc, current_rune.efficiency)
            store_monster_eff(monster_exp_eff, current_rune.loc, current_rune.exp_efficiency)

        # Setup dataframe index
        columns_name = ('Type', 'Slot', 'Grade', 'Base', 'Stars', 'Lv', 'Main', 'Innate', '')
        columns_name += ('Spd', 'Atk%', 'Hp%', 'Def%', 'Crate', 'Cdmg', 'Res', 'Acc', 'Atk+', 'Hp+', 'Def+')
        columns_name += ('', 'Eff', 'Exp eff', 'Ori-Eff', 'Ori-Exp eff', "Loc")
        
        # Convert rune data to pandas dataframe
        whole_rune_pd = pd.DataFrame(whole_rune, columns=columns_name)
        whole_rune_pd_sorted = whole_rune_pd.sort_values(by=['Exp eff'])

        # Calculate monster efficiency
        monster_eff_avg = []
        for monster in monster_eff:
            avg_real_eff = monster_eff[monster] / 6
            avg_exp_eff = monster_exp_eff[monster] / 6
            monster_eff_avg.append((monster, avg_real_eff, avg_exp_eff))

        # Convert eff data to pandas data frame
        monster_eff_index = ('monster', 'avg real eff', 'avg exp eff')
        monster_eff_pd = pd.DataFrame(monster_eff_avg, columns=monster_eff_index)
        monster_eff_sorted = monster_eff_pd.sort_values(by=['avg real eff'], ascending=False)

        # enable header formatting
        import pandas.io.formats.excel
        pd.io.formats.excel.header_style = None

        success = False
        while not success:
            
            try:
                # Send to excel
                filename = '{} rune_eff.xlsx'.format(wizard_id)
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                workbook = writer.book

                whole_rune_pd_sorted.to_excel(writer, sheet_name="Rune")
                worksheet = writer.sheets['Rune']
                excel_formatting(workbook, worksheet)

                monster_eff_sorted.to_excel(writer, sheet_name="Mons eff")
                worksheet = writer.sheets['Mons eff']
                excel_formatting(workbook, worksheet, cond="mons")

                writer.save()
                os.startfile(filename)
                success = True

            except Exception as e:
                print("File is open, close it first:", e)
                os.system("pause")

except Exception as e:
    print(e)
    os.system("pause")
    raise e
