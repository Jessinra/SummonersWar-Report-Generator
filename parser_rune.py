from data_mapping import DataMappingCollection


class RuneParser:
    @staticmethod
    def get_rune_user(unit_list, rune_owner_id):

        if rune_owner_id == 0:
            return ""  # Inventory
        else:
            return unit_list[rune_owner_id]

    @staticmethod
    def is_stat_enchanted(substat):
        return substat[2] == 1

    @staticmethod
    def get_rune_set(set_id):
        return DataMappingCollection.get_rune_set(set_id)

    @staticmethod
    def get_rune_stars(stars):
        return int(str(stars)[-1])

    @staticmethod
    def get_rune_grade_shorten(class_id):
        return DataMappingCollection.get_rune_class_shorten(class_id)

    @staticmethod
    def get_rune_stat(stat):

        rune_stat_type, value = RuneParser.get_rune_stat_without_grind(stat)
        grind = RuneParser.get_rune_grind_value(stat)

        return rune_stat_type, (value + grind)

    @staticmethod
    def get_rune_stat_without_grind(stat):

        rune_stat_type = RuneParser.get_rune_stat_type(stat)
        value = RuneParser.get_rune_stat_value(stat)

        return rune_stat_type, value

    @staticmethod
    def get_rune_stat_value(stat):
        return stat[1]

    @staticmethod
    def get_rune_stat_type(stat):

        type_id = stat[0]
        return DataMappingCollection.get_rune_stat_type(type_id)

    @staticmethod
    def get_rune_grind_value(stat):

        if RuneParser.is_grindable(stat):
            return stat[3]
        else:
            return 0

    @staticmethod
    def is_grindable(stats):
        return len(stats) > 2

    @staticmethod
    def max_roll(primary_stat):
        return DataMappingCollection.get_rune_primary_stat_max_value(primary_stat)

    @staticmethod
    def max_roll_substats(substat):
        return DataMappingCollection.get_rune_sub_stat_max_value(substat)

    @staticmethod
    def substats_to_dense_form(substat_list):

        empty_substats_map = RuneParser.create_substats_map()
        substats_map = RuneParser.update_substats_map(empty_substats_map, substat_list)
        dense_tuples = RuneParser.dict_to_dense(substats_map)
        return dense_tuples

    @staticmethod
    def create_substats_map(default=None):

        substats_map = {

            "SPD": default,
            "ATK%": default,
            "HP%": default,
            "DEF%": default,
            "CRate": default,
            "CDmg": default,
            "RES": default,
            "ACC": default,
            "ATK flat": default,
            "HP flat": default,
            "DEF flat": default,
        }

        return substats_map

    @staticmethod
    def update_substats_map(substats_map, substat_list):

        for substat in substat_list:
            substats_map[substat[0]] = RuneParser.get_rune_stat_value(substat)  # Asign value to corresponding stat in substats map

        return substats_map

    @staticmethod
    def dict_to_dense(dictionary):
        return tuple([x for x in dictionary.values()])
