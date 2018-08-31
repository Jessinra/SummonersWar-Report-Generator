from data_mapping import DataMappingCollection


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

def get_monster_name(monster_id):
    return DataMappingCollection.get_monster_name(monster_id)

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
