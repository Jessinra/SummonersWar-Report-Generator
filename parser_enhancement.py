from parser_rune import Rune

class Enhancement():
    
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
        self.set_min_value()
        self.set_max_value()

    def set_enhancement_type(self, craft_type):

        if craft_type == 1 or craft_type == 3 :
            self.type = "Enchant"
        else:
            self.type = "Grind"

    def set_enhancement_sets(self):

        self.set = Rune.get_rune_type(int(self.type_id[0:-4]))

    def set_enhancement_stat(self):

        self.stat = Rune.get_sub_type(int(self.type_id[-4:-2]))

    def set_enhancement_grade(self):
        
        self.grade_int = int(self.type_id[-1])
        self.grade = Rune.get_rune_grade(self.grade_int, shorten=False)

    def set_min_value(self):

        self.min_value = enhancement_map[self.type][self.stat][self.grade]['min']

    def set_max_value(self):

        self.max_value = enhancement_map[self.type][self.stat][self.grade]['max']

    def show_detail(self):
        
        print("{} {} {} {} ({} - {})\n".format(self.type, self.grade, self.set, self.stat, self.min_value, self.max_value))

    def __eq__(self, other):
        
        return self.type_id == other.type_id
    


enhancement_map = {

    'Grind': {
        "SPD": { "Unknown": { "min": 1, "max": 2 }, "Magic": { "min": 1, "max": 2 }, "Rare": { "min": 2, "max": 3 }, "Hero": { "min": 3, "max": 4 }, "Legend": { "min": 4, "max": 5 } },
        "ATK%": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 5 }, "Rare": { "min": 3, "max": 6 }, "Hero": { "min": 4, "max": 7 }, "Legend": { "min": 5, "max": 10 } },
        "ATK flat": { "Unknown": { "min": 4, "max": 8 }, "Magic": { "min": 6, "max": 12 }, "Rare": { "min": 10, "max": 18 }, "Hero": { "min": 12, "max": 22 }, "Legend": { "min": 18, "max": 30 } },
        "HP%": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 5 }, "Rare": { "min": 3, "max": 6 }, "Hero": { "min": 4, "max": 7 }, "Legend": { "min": 5, "max": 10 } },
        "HP flat": { "Unknown": { "min": 80, "max": 120 }, "Magic": { "min": 100, "max": 200 }, "Rare": { "min": 180, "max": 250 }, "Hero": { "min": 230, "max": 450 }, "Legend": { "min": 430, "max": 550 } },
        "DEF%": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 5 }, "Rare": { "min": 3, "max": 6 }, "Hero": { "min": 4, "max": 7 }, "Legend": { "min": 5, "max": 10 } },
        "DEF flat": { "Unknown": { "min": 4, "max": 8 }, "Magic": { "min": 6, "max": 12 }, "Rare": { "min": 10, "max": 18 }, "Hero": { "min": 12, "max": 22 }, "Legend": { "min": 18, "max": 30 } }
        # "CRate": { "Unknown": { "min": 1, "max": 2 }, "Magic": { "min": 1, "max": 3 }, "Rare": { "min": 2, "max": 4 }, "Hero": { "min": 3, "max": 5 }, "Legend": { "min": 4, "max": 6 } },
        # "CDmg": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 4 }, "Rare": { "min": 2, "max": 5 }, "Hero": { "min": 3, "max": 5 }, "Legend": { "min": 4, "max": 7 } },
        # "RES": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 4 }, "Rare": { "min": 2, "max": 5 }, "Hero": { "min": 3, "max": 7 }, "Legend": { "min": 4, "max": 8 } },
        # "ACC": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 4 }, "Rare": { "min": 2, "max": 5 }, "Hero": { "min": 3, "max": 7 }, "Legend": { "min": 4, "max": 8 } }
    },
    
    'Enchant': {
        "SPD": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 4 }, "Rare": { "min": 3, "max": 6 }, "Hero": { "min": 5, "max": 8 }, "Legend": { "min": 7, "max": 10 } },
        "ATK%": { "Unknown": { "min": 2, "max": 4 }, "Magic": { "min": 3, "max": 7 }, "Rare": { "min": 5, "max": 9 }, "Hero": { "min": 7, "max": 11 }, "Legend": { "min": 9, "max": 13 } },
        "ATK flat": { "Unknown": { "min": 8, "max": 12 }, "Magic": { "min": 10, "max": 16 }, "Rare": { "min": 15, "max": 23 }, "Hero": { "min": 20, "max": 30 }, "Legend": { "min": 28, "max": 40 } },
        "HP%": { "Unknown": { "min": 2, "max": 4 }, "Magic": { "min": 3, "max": 7 }, "Rare": { "min": 5, "max": 9 }, "Hero": { "min": 7, "max": 11 }, "Legend": { "min": 9, "max": 13 } },
        "HP flat": { "Unknown": { "min": 100, "max": 150 }, "Magic": { "min": 130, "max": 220 }, "Rare": { "min": 200, "max": 310 }, "Hero": { "min": 290, "max": 420 }, "Legend": { "min": 400, "max": 580 } },
        "DEF%": { "Unknown": { "min": 2, "max": 4 }, "Magic": { "min": 3, "max": 7 }, "Rare": { "min": 5, "max": 9 }, "Hero": { "min": 7, "max": 11 }, "Legend": { "min": 9, "max": 13 } },
        "DEF flat": { "Unknown": { "min": 8, "max": 12 }, "Magic": { "min": 10, "max": 16 }, "Rare": { "min": 15, "max": 23 }, "Hero": { "min": 20, "max": 30 }, "Legend": { "min": 28, "max": 40 } },
        "CRate": { "Unknown": { "min": 1, "max": 3 }, "Magic": { "min": 2, "max": 4 }, "Rare": { "min": 3, "max": 5 }, "Hero": { "min": 4, "max": 7 }, "Legend": { "min": 6, "max": 9 } },
        "CDmg": { "Unknown": { "min": 2, "max": 4 }, "Magic": { "min": 3, "max": 5 }, "Rare": { "min": 4, "max": 6 }, "Hero": { "min": 5, "max": 8 }, "Legend": { "min": 7, "max": 10 } },
        "RES": { "Unknown": { "min": 2, "max": 4 }, "Magic": { "min": 3, "max": 6 }, "Rare": { "min": 5, "max": 8 }, "Hero": { "min": 6, "max": 9 }, "Legend": { "min": 8, "max": 11 } },
        "ACC": { "Unknown": { "min": 2, "max": 4 }, "Magic": { "min": 3, "max": 6 }, "Rare": { "min": 5, "max": 8 }, "Hero": { "min": 6, "max": 9 }, "Legend": { "min": 8, "max": 11 } }
    }
}