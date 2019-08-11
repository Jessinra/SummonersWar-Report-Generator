from data_mapping import DataMappingCollection


class UnitParser:
    def __init__(self):

        self._unit_dict = {}
        self._duplicate_unit_dict = {}

    def parse_units(self, list_of_monster):

        for mons in list_of_monster:
            unit_id = UnitParser._get_monster_id(mons)
            unit_name = UnitParser._get_monster_name(mons)

            self._track_unit_duplicates(unit_name)
            self._pair_unit_name_and_unit_id(unit_name, unit_id)

    @staticmethod
    def _get_monster_id(monster):
        return monster['unit_id']

    @staticmethod
    def _get_monster_name(monster):

        monster_id = monster['unit_master_id']
        return DataMappingCollection.get_monster_name(monster_id)

    def _track_unit_duplicates(self, unit_name):

        if unit_name not in self._duplicate_unit_dict:
            self._duplicate_unit_dict[unit_name] = 1
        else:
            self._duplicate_unit_dict[unit_name] += 1

    def _pair_unit_name_and_unit_id(self, unit_name, unit_id):

        if self._duplicate_unit_dict[unit_name] == 1:
            self._unit_dict[unit_id] = unit_name
        else:
            self._unit_dict[unit_id] = unit_name + " " + str(self._duplicate_unit_dict[unit_name])

    def get_unit_dict(self):
        return self._unit_dict
