from monsters import monsters_name_map


def generate_monsters(list_of_unit):
    """
    convert list of unit to monsters list
    :param list_of_unit: list of raw unit data
    :type list_of_unit: list
    :return: monster list
    :rtype: list
    """

    def get_monster_name(id):
        """
        Return monster name from monster id
        :param id: monsters id
        :type id: int
        :return: monster name
        :rtype: string
        """
        def element(id):

            if id == "1":
                return "water"
            elif id == "2":
                return "fire"
            elif id == "3":
                return "wind"
            elif id == "4":
                return "light"
            elif id == "5":
                return "dark"

        try:
            if str(id) in monsters_name_map:
                name = monsters_name_map[str(id)]
            else:
                name = str(monsters_name_map[str(id)[0:3]] + " " + element(str(id)[4]))

            return name
        except:
            return "unknown "+str(id)

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

    if len(monster_id) > 2:
        try:
            monsters_eff[monster_id] += rune_eff
        except:
            monsters_eff[monster_id] = rune_eff