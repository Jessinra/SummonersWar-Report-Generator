
""" ====================================================================
                                    UNUSED
==================================================================== """


def rune_is_equiped(id):

    if id == "1":
        return True
    else:
        return False


def get_rune_user(unit_list, id):

    if id == 0:
        return ""
    else:
        return unit_list[id]

""" ====================================================================
                                Sub function
==================================================================== """


def get_rune_type(id):
    """
    convert rune type to string
    """

    name_map = {
        1: "Energy",
        2: "Guard",
        3: "Swift",
        4: "Blade",
        5: "Rage",
        6: "Focus",
        7: "Endure",
        8: "Fatal",
        10: "Despair",
        11: "Vampire",
        13: "Violent",
        14: "Nemesis",
        15: "Will",
        16: "Shield",
        17: "Revenge",
        18: "Destroy",
        19: "Fight",
        20: "Determination",
        21: "Enhance",
        22: "Accuracy",
        23: "Tolerance",
    }

    return name_map[id]


def get_sub_type(id):
    """
    convert rune sub type to string
    """

    sub_type_map = {
        0: "",
        1: "HP flat",
        2: "HP%",
        3: "ATK flat",
        4: "ATK%",
        5: "DEF flat",
        6: "DEF%",
        8: "SPD",
        9: "CRate",
        10: "CDmg",
        11: "RES",
        12: "ACC",
    }

    return sub_type_map[id]


def get_rune_grade(id):
    """
    return rune grade (Currently)
    """

    rune_class_map = {
        0: 'U',  # unknown
        1: 'C',  # common
        2: 'M',  # magic
        3: 'R',  # rare
        4: 'H',  # hero
        5: 'L',  # legend
    }

    return rune_class_map[id]


def get_attribute(stats):
    """
    :param stats: raw data of sub stats
    :type stats: list
    :return: tuple of sub type and value
    :rtype: tuple
    """

    sub_type = get_sub_type(stats[0])
    value = stats[1]

    if len(stats) > 2:
        grind = stats[3]
    else:
        grind = 0

    return sub_type, (value+grind)


def max_roll(rune_type):
    """
    return max stat of primary stat
    """

    sub_type_max = {

        "HP flat": 2448,
        "HP%": 63,
        "ATK flat": 160,
        "ATK%": 63,
        "DEF flat": 160,
        "DEF%": 63,
        "SPD": 42,
        "CRate": 58,
        "CDmg": 80,
        "RES": 65,
        "ACC": 65,
    }

    return sub_type_max[rune_type]


def max_roll_substats(rune_type):
    """
    return max roll of sub stat
    """

    try:
        sub_type_max = {

            "HP%": 40,
            "ATK%": 40,
            "DEF%": 40,
            "SPD": 30,
            "CRate": 30,
            "CDmg": 35,
            "RES": 40,
            "ACC": 40,
        }
        return sub_type_max[rune_type]

    except:
        return 99999999999

""" ====================================================================
                                Main function
==================================================================== """


def rune_efficiency(rune):
    """
    Finding rune current efficiency
    """

    # Rune primary stats in tuple eg: ("HP flat" , 580)
    rune_primary_stat = get_attribute(rune['pri_eff'])

    # Rune secondary stats (sub stats)
    rune_subs_list_raw = rune['sec_eff']
    rune_subs_list = []
    secondary_score = 0
    for substats in rune_subs_list_raw:
        rune_substats = get_attribute(substats)
        rune_subs_list.append(rune_substats)
        secondary_score += rune_substats[1] / max_roll_substats(rune_substats[0])

    # Rune inate stat
    rune_static_stat = get_attribute(rune['prefix_eff'])
    secondary_score += rune_static_stat[1] / max_roll_substats(rune_static_stat[0])

    # Sum all score
    primary_score = rune_primary_stat[1] / max_roll(rune_primary_stat[0])
    final_score = (primary_score + secondary_score) / 2.8

    return final_score


def rune_expected_efficiency(rune):
    """
    Return rune expected efficiency at +12
    """

    def probability_new_roll(avail_sub, roll_count):
        """
        Calculate probability of rolling into a new good stat
        :param avail_sub: subs owned by rune
        :param roll_count: how many roll
        """

        def expectation(fgood, fbad, rc_l):
            """
            Calculate of how many roll into 'good' stat  (hyper geometry dist mean (n * k/N)
            :param fgood: available good stat un rolled
            :param fbad: available good stat un rolled
            :param rc_l: how many roll available
            """

            return rc_l * (fgood / (fgood + fbad))

        prob_getting_good = 0
        if roll_count > 0:

            # List of good and bad stats
            good = ["HP%", "ATK%", "DEF%", "SPD", "CRate", "CDmg", "RES", "ACC"]
            bad = ["HP flat", "ATK flat", "DEF flat"]

            # Count available good and bad stats for rolling
            fgood = len([x for x in good if x not in avail_sub])
            fbad = len([x for x in bad if x not in avail_sub])

            # Statistic
            expected_roll_into_good = expectation(fgood, fbad, roll_count)
            prob_getting_good = expected_roll_into_good / roll_count

        return prob_getting_good

    def probability_avail(avail_sub):
        """
        Calculate probability to roll into good stat for available stats
        :param avail_sub: available stats of runes
        """

        # List of good and bad stats
        good = ["HP%", "ATK%", "DEF%", "SPD", "CRate", "CDmg", "RES", "ACC"]
        bad = ["HP flat", "ATK flat", "DEF flat"]

        # Count good and bad stats owned by rune
        cgood = len([x for x in avail_sub if x in good])
        cbad = len([x for x in avail_sub if x in bad])

        prob_getting_good = cgood / (cgood+cbad)

        return prob_getting_good

    # Get rune sub stats, do current eff count
    rune_subs_list_raw = rune['sec_eff']
    rune_subs_list_type = []
    secondary_score = 0
    for substats in rune_subs_list_raw:
        rune_substats = get_attribute(substats)
        rune_subs_list_type.append(rune_substats[0])
        secondary_score += rune_substats[1] / max_roll_substats(rune_substats[0])

    # Get rune inate stat, do current eff count
    rune_static_stat = get_attribute(rune['prefix_eff'])
    secondary_score += rune_static_stat[1] / max_roll_substats(rune_static_stat[0])

    # ============================================= #
    #                   forecast part               #
    # ============================================= #

    rune_subs_upgrade_avg_eff = 47 / 59     # 6 star sub upgrade min 35 max 59, avg 47...
    rune_level = rune['upgrade_curr']

    # count how many times NEW sub available
    rune_upgrade_new = 4 - min(len(rune_subs_list_type), 4)
    rune_upgrade_new_point = 0

    # calculate point earned by rolling into NEW stats
    rune_subs_list_type.append(rune_static_stat)
    roll_to_good_probability = probability_new_roll(rune_subs_list_type, rune_upgrade_new)
    for _ in range(0, rune_upgrade_new):

        # times avg eff * 0.2 = how much roll into that stat
        rune_upgrade_new_point += (roll_to_good_probability * rune_subs_upgrade_avg_eff * 0.2)

    # count how many times sub upgrade available
    rune_subs_upgrade = 4 - min(rune_level // 3, 4)
    rune_subs_upgrade_avail = rune_subs_upgrade - rune_upgrade_new

    # calculate point earned by rolling into AVAILABLE stats
    rune_upgrade_avail_point = 0
    for _ in range(0, rune_subs_upgrade_avail):
        rune_upgrade_avail_point += (probability_avail(rune_subs_list_type) * rune_subs_upgrade_avg_eff * 0.2)

    # Sum those points
    third_score = rune_upgrade_new_point + rune_upgrade_avail_point

    # Primary point for primary stat
    if rune_level > 12:
        primary_score = 1
    else:
        primary_score = 0.75  # around + 12

    final_score = (primary_score + secondary_score + third_score) / 2.8  # 1 + 9 x 0.2 max roll
    return final_score
