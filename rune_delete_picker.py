from parser_rune import *
from parser_format import *
from parser_mons import *
import pandas as pd
import json
import os
import sys


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
                    
        except Exception as e:
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

    return rune_list, monster_list


try:
    if __name__ == '__main__':

        wizard_id = get_wizard_id()

        try:
            rune_list, monster_list = parse_file(wizard_id)

        except Exception as e:
            print("cannot open file:", e)
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

            # Getting rune main information
            rune_slot = rune['slot_no']
            rune_stars = rune['class']
            rune_grade = get_rune_grade(rune['rank'])
            rune_base_grade = get_rune_grade(rune['extra'])
            rune_type = get_rune_type(rune['set_id'])
            rune_level = rune['upgrade_curr']
            rune_main = get_attribute(rune['pri_eff'])
            rune_inate = get_attribute(rune['prefix_eff'])
            rune_loc = get_rune_user(monster_list, rune["occupied_id"])

            # Getting sub stats
            rune_subs_list_raw = rune['sec_eff']
            rune_subs_list = []
            for substats in rune_subs_list_raw:
                rune_substats = get_attribute(substats)
                rune_subs_list.append(rune_substats)

            # Calculate eff
            rune_eff = rune_efficiency(rune)
            rune_exp_eff = rune_expected_efficiency(rune)

            # Reshape and append
            rune_data = (rune_type, rune_slot, rune_grade, rune_base_grade, rune_stars, rune_level,
                        rune_main, rune_inate, rune_subs_list, rune_eff, rune_exp_eff, rune_loc)
            whole_rune.append(rune_data)

            """ ===================================================
                        MONSTER EFF SECTION
            ===================================================="""
            store_monster_eff(monster_eff, rune_loc, rune_eff)
            store_monster_eff(monster_exp_eff, rune_loc, rune_exp_eff)

        # Convert rune data to pandas dataframe
        whole_rune_index = ('Type', 'Slot', 'Grade', 'Base', 'Stars', 'Lv', 'Main', 'Innate', 'Subs', 'Eff', 'Exp eff', "Loc")
        whole_rune_pd = pd.DataFrame(whole_rune, columns=whole_rune_index)
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