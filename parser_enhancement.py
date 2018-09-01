from data_mapping import DataMappingCollection

class Enhancement:

    def __init__(self, enhancement):

        self.type_id = str(enhancement['craft_type_id'])
        self.id = str(enhancement['craft_item_id'])

        self.type = None
        self.set = None
        self.stat = None
        self.grade = None
        self.grade_int = 0
        self.min_value = 0
        self.max_value = 0

        self.set_enhancement_type(enhancement['craft_type'])
        self.set_enhancement_sets()
        self.set_enhancement_stat()
        self.set_enhancement_grade()
        self.set_enhance_values()

    def set_enhancement_type(self, craft_type):

        if craft_type == 1 or craft_type == 3:
            self.type = "Enchant"
            
        else:
            self.type = "Grind"

    def set_enhancement_sets(self):

        set_id = int(self.type_id[0:-4])
        self.set = DataMappingCollection.get_rune_set(set_id)

    def set_enhancement_stat(self):

        type_id = int(self.type_id[-4:-2])
        self.stat = DataMappingCollection.get_rune_stat_type(type_id)

    def set_enhancement_grade(self):

        self.grade_int = int(self.type_id[-1])
        self.grade = DataMappingCollection.get_rune_class(self.grade_int)

    def set_enhance_values(self):

        if self.type == "Grind":
            self.set_grindstone_values()

        elif self.type == "Enchant":
            self.set_enchantgem_values()

    def set_grindstone_values(self):

        self.min_value = DataMappingCollection.get_grindstone_value_min(self.stat, self.grade)
        self.max_value = DataMappingCollection.get_grindstone_value_max(self.stat, self.grade)
    
    def set_enchantgem_values(self):
        
        self.min_value = DataMappingCollection.get_enchantgem_value_min(self.stat, self.grade)
        self.max_value = DataMappingCollection.get_enchantgem_value_max(self.stat, self.grade)

    def show_detail(self):

        # Example: Grind Legend Violent Spd (4 - 5)
        print("{} {} {} {} ({} - {})\n".format(self.type, self.grade, self.set, self.stat, self.min_value, self.max_value))

    def __eq__(self, other):
        return self.type_id == other.type_id



