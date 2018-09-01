from data_mapping import DataMappingCollection


class RuneParser:

    @staticmethod
    def get_rune_user(unit_list, rune_id):

        if rune_id == 0:
            return ""
        else:
            return unit_list[rune_id]

    @staticmethod
    def is_stat_enchanted(substat):
        return substat[2] == 1

    @staticmethod
    def get_rune_set(set_id):
        return DataMappingCollection.get_rune_set(set_id)

    @staticmethod
    def get_rune_stat_type(type_id):
        return DataMappingCollection.get_rune_stat_type(type_id)

    @staticmethod
    def get_rune_grade(class_id, shorten=True):
        
        if shorten:
            return DataMappingCollection.get_rune_class_shorten(class_id)
        else:
            return DataMappingCollection.get_rune_class(class_id)

    @staticmethod
    def get_rune_stat(stats):
        """
        :return: tuple of sub type and value
        :rtype: tuple
        """

        rune_stat_type, value = RuneParser.get_rune_stat_without_grind(stats)
        grind = RuneParser.get_rune_grind_value(stats)

        return rune_stat_type, (value + grind)
    
    @staticmethod
    def get_rune_stat_without_grind(stats):
        """
        :return: tuple of sub type and value
        :rtype: tuple
        """
        rune_stat_type = RuneParser.get_rune_stat_type(stats[0])
        value = stats[1]

        return rune_stat_type, value

    @staticmethod
    def get_rune_grind_value(stats):

        if RuneParser.is_grindable(stats):
            return stats[3]
        else:
            return 0

    @staticmethod
    def is_grindable(stats):
        return len(stats) > 2

    @staticmethod
    def max_roll(primary_stat):
        return DataMappingCollection.get_rune_primary_stat_max_value(primary_stat)

    @staticmethod
    def max_roll_substats(sub_stat):
        return DataMappingCollection.get_rune_sub_stat_max_value(sub_stat)

    @staticmethod
    def substats_to_dense_form(substat_list):

        substats_map = RuneParser.create_empty_substats_map()
        substats_map = RuneParser.update_substats_map(substat_list, substats_map)
        dense_tuples = RuneParser.dict_to_dense(substats_map)

        return dense_tuples

    @staticmethod
    def create_empty_substats_map():
        
        substats_map = {

            "SPD": None,
            "ATK%": None,
            "HP%": None,
            "DEF%": None,
            "CRate": None,
            "CDmg": None,
            "RES": None,
            "ACC": None,
            "ATK flat": None,
            "HP flat": None,
            "DEF flat": None,
        }

        return substats_map

    @staticmethod
    def dict_to_dense(dictionary):
        return tuple([x for x in dictionary.values()])



    @staticmethod
    def update_substats_map(substat_list, substats_map):

        for substat in substat_list:
            substats_map[substat[0]] = substat[1]   # Asign value to corresponding stat in substats map

        return substats_map
    







    





    

    



        









  


    

    

