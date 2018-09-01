from data_mapping import DataMappingCollection

class UnitParser:

    def __init__(self, list_of_monster):

        self.unit_dict = {}
        self.duplicate_unit_dict = {}
        self.parse_units(list_of_monster)

    def parse_units(self, list_of_monster):

        for mons in list_of_monster:

            unit_id = UnitParser.get_monster_id(mons)
            unit_name = UnitParser.get_monster_name(mons)

            self.track_unit_duplicates(unit_name)
            self.set_unit_name_id_mapping(unit_name, unit_id)

    @staticmethod
    def get_monster_id(monster):
        return monster['unit_id']

    @staticmethod
    def get_monster_name(monster):

        monster_id = monster['unit_master_id']
        return DataMappingCollection.get_monster_name(monster_id)

    def track_unit_duplicates(self, unit_name):

        if unit_name not in self.duplicate_unit_dict:
            self.duplicate_unit_dict[unit_name] = 1
        else:
            self.duplicate_unit_dict[unit_name] += 1

    def set_unit_name_id_mapping(self, unit_name, unit_id):
        
        if self.duplicate_unit_dict[unit_name] == 1:
            self.unit_dict[unit_id] = unit_name
        else:
            self.unit_dict[unit_id] = unit_name + " " + str(self.duplicate_unit_dict[unit_name])


