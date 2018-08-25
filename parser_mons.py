from monsters import monsters_name_map


def get_monster_name(monster_id):
    """
    Return monster name from monster id
    :param monster_id: monsters id
    :type monster_id: int
    :return: monster name
    :rtype: string
    """

    monster_attribute = {
        '1': "Water",
        '2': "Fire",
        '3': "Wind",
        '4': "Light",
        '5': "Dark"
    }

    # Specific name
    if str(monster_id) in monsters_name_map:
        return monsters_name_map[str(monster_id)]

    # Unawakened name
    elif str(monster_id)[0:3] in monsters_name_map:
        return str(monsters_name_map[str(monster_id)[0:3]] + " " + monster_attribute[str(monster_id)[4]])

    else:
        return "unknown " + str(monster_id)


def generate_monsters(list_of_unit):
    """
    convert list of unit to monsters list
    :param list_of_unit: list of raw unit data
    :type list_of_unit: list
    :return: monster list
    :rtype: list
    """

    monster_list = {}
    count_duplicate = {}
    for unit in list_of_unit:
        unit_id = unit['unit_id']
        unit_name = get_monster_name(unit['unit_master_id'])

        if unit_name not in count_duplicate:
            monster_list[unit_id] = unit_name
        else:
            monster_list[unit_id] = unit_name + " " + str(count_duplicate[unit_name] + 1)

        count_duplicate[unit_name] = 1

    return monster_list


def store_monster_eff(monsters_eff, monster_id, rune_eff):
    """
    Update monster efficiency dictionary
    :param monsters_eff: dictionary to keep monsters efficiencies
    :type monsters_eff: dict
    :param monster_id: id representing monster
    :type monster_id: string
    :param rune_eff: rune's efficiency
    :type rune_eff: float
    """

    if len(monster_id) > 2:
        if monster_id in monsters_eff:
            monsters_eff[monster_id] += rune_eff
        else:
            monsters_eff[monster_id] = rune_eff
