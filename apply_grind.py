from parser_file import get_wizard_id, parse_file
from parser_enhancement import Enhancement
from parser_rune import Rune, get_rune_user
from parser_format import excel_formatting
import os
import sys
import operator
import pandas as pd

_LOGGING = False


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

        # Bad rune should not be grinded
        if rune.exp_efficiency_without_grind <= eff_threshold:
            return False

        substat_to_be_grinded = rune.grind_values[grindstone.stat]

        if substat_to_be_grinded is None:
            return False

        elif substat_to_be_grinded == "Applied":
            return False

        elif substat_to_be_grinded == "SPD":
            return substat_to_be_grinded < grindstone.max_value

        else: 
            return substat_to_be_grinded < grindstone.max_value - 1

    def virtually_apply_grind(grindstone, rune):

        rune.grind_values[grindstone.stat] = "Applied"

    def format_applying_grind(grindstone, rune):
        """
        Reshape for printout
        """
        _separator = None

        rune_data = (rune.type,
                    rune.slot,
                    rune.grade,
                    rune.base_grade,
                    rune.stars,
                    rune.level,
                    rune.main,
                    rune.inate,
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

    grindstones.sort(key=operator.attrgetter('stat'))
    grindstones.sort(key=operator.attrgetter('grade_int'), reverse=True)
    runes.sort(key=operator.attrgetter('efficiency_without_grind'), reverse=True)

    applied = []
    checked_and_failed = {
        "SPD": False,
        "ATK%": False,
        "HP%": False,
        "DEF%": False,
        #"CRate": False,
        #"CDmg": False,
        #"RES": False,
        #"ACC": False,
        "ATK flat": False,
        "HP flat": False,
        "DEF flat": False,
    }

    for grindstone in grindstones:

        applicable = False

        if _LOGGING:
            print("checking : ")
            grindstone.show_detail()

        # By pass if the subs checked and failed
        if checked_and_failed[grindstone.stat]:
            continue

        for rune in runes:
            
            if _LOGGING:
                print(rune.substats)

            if grind_applicable(grindstone, rune):
                
                if _LOGGING:
                    print(">>  APPLICABLE  <<\n\n")

                formatted_result = format_applying_grind(grindstone, rune)
                applied.append(formatted_result)

                virtually_apply_grind(grindstone, rune)
                applicable = True

                # Continue to next grindstone
                break

            else:

                if _LOGGING:
                    print("fail\n\n")

        # At this point, the grindstone of this type can't be used since it fail every runes
        if not applicable:
            checked_and_failed[grindstone.stat] = True

    return applied


if __name__ == '__main__':

    wizard_id = get_wizard_id()

    try:
        rune_list, monster_list, enhancement_list = parse_file(wizard_id)

        # Parse the grindstones
        grindstone_inventory = {}
        for enhancement in enhancement_list:

            current_enhancement = Enhancement(enhancement)

            # Skip enchantment gem
            if current_enhancement.type == "Enchant":
                continue

            # Group each enhancement according to it's set
            if current_enhancement.set in grindstone_inventory:
                grindstone_inventory[current_enhancement.set].append(current_enhancement)

            else:
                grindstone_inventory[current_enhancement.set] = [current_enhancement]

            if _LOGGING:
                current_enhancement.show_detail()

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

        if _LOGGING:
            for k in rune_inventory:
                print(k, len(rune_inventory[k]))


        grind_result = []
        for rune_set in grindstone_inventory:

            # Only check if there's grind and rune that match
            if rune_set in rune_inventory:

                if _LOGGING:
                    print("\n\nCHECKING RUNE SET : ", rune_set)

                grind_result += apply_grindstones(grindstones=grindstone_inventory[rune_set], runes=rune_inventory[rune_set]) 

        
        # Setup dataframe index
        columns_name = ('Type', 'Slot', 'Grade', 'Base', 'Stars', 'Lv', 'Main', 'Innate',
                        'Substats', 'Eff', 'Exp eff', 'Ori-Eff', 'Ori-Exp eff', "Loc", "",
                        'Type', 'Grade', 'Stat')

        # Convert grind result data to pandas dataframe
        grind_result_pd = pd.DataFrame(grind_result, columns=columns_name)
        grind_result_pd_sorted = grind_result_pd.sort_values(by=['Exp eff'], ascending=False)

        # enable header formatting
        import pandas.io.formats.excel
        pd.io.formats.excel.header_style = None

        success = False
        while not success:
            
            try:
                # Send to excel
                filename = '{} applying_grinds.xlsx'.format(wizard_id)
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                workbook = writer.book

                grind_result_pd_sorted.to_excel(writer, sheet_name="Applying grinds")
                worksheet = writer.sheets['Applying grinds']
                excel_formatting(workbook, worksheet, cond="grinds")

                writer.save()
                os.startfile(filename)
                success = True

            except Exception as e:
                print("File is open, close it first:", e)
                os.system("pause")
                raise e

    except Exception as e:
        print(e)
        print("aborting.....")
        raise e