""" ====================================================================
                                    UNUSED
==================================================================== """


def rune_is_equipped(rune_id):
    """
    Check if a rune is equipped
    :param rune_id: part of rune id which determine if it's equipped
    :type rune_id: string
    :return: is rune equipped or not
    :rtype: bool
    """

    return rune_id == "1"


def get_rune_user(unit_list, rune_id):
    """
    Get name of the monster equipped with this rune
    :param unit_list: list of monster own by player
    :type unit_list: list
    :param rune_id: partial id of the rune, which indicate user
    :type rune_id: int
    :return: name of the monster
    :rtype: string
    """

    if rune_id == 0:
        return ""
    else:
        return unit_list[rune_id]


class Rune:

    def __init__(self, rune):

        # Default initialization
        self.slot = rune['slot_no']
        self.stars = rune['class']
        self.grade = Rune.get_rune_grade(rune['rank'])
        self.base_grade = Rune.get_rune_grade(rune['extra'])
        self.type = Rune.get_rune_type(rune['set_id'])
        self.level = rune['upgrade_curr']
        self.main = Rune.get_rune_stat(rune['pri_eff'])

        self.loc = None
        self.innate = None
        self.substats = None
        self.dense_substats = None
        self.grind_values = None
        self.efficiency = 0
        self.exp_efficiency = 0
        self.efficiency_without_grind = 0
        self.exp_efficiency_without_grind = 0

        self.set_innate(rune['prefix_eff'])
        self.set_substats(rune['sec_eff'])
        self.set_dense_substats()
        self.set_grind_values(rune['sec_eff'])

        self.set_rune_efficiency(rune)
        self.set_rune_expected_efficiency(rune)

    def set_loc(self, rune_user):
        """
        Set location of a rune
        """

        self.loc = rune_user

    def set_innate(self, innate):
        """
        Set innate sub stat of a rune
        """

        innate = Rune.get_rune_stat(innate)

        # Remove if it doesn't have innate stat
        if innate[0] is None:
            self.innate = None
        else:
            self.innate = innate

    def set_substats(self, rune_substat_raw):
        """
        Getting sub stats
        """

        self.substats = []
        for substats in rune_substat_raw:
            rune_substats = Rune.get_rune_stat(substats)
            self.substats.append(rune_substats)

    def set_dense_substats(self):
        """
        Densify the matrix of substats
        """

        self.dense_substats = Rune.substats_to_dense(self.substats)

    def set_grind_values(self, substats):
        """
        Set a map containing value of grinds used
        :param substats: list of substat that rune has
        :type substats: list
        """

        self.grind_values = {

            "SPD": None,
            "ATK%": None,
            "HP%": None,
            "DEF%": None,
            # "CRate": None,
            # "CDmg": None,
            # "RES": None,
            # "ACC": None,
            "ATK flat": None,
            "HP flat": None,
            "DEF flat": None,
        }

        for stat in substats:

            sub_type = Rune.get_sub_type(stat[0])

            # Skip crate, cdmg, res, acc since they can't be grinded
            if sub_type not in self.grind_values:
                continue

            if len(stat) > 2:
                self.grind_values[sub_type] = stat[3]
            else:
                self.grind_values[sub_type] = 0

    def set_rune_efficiency(self, rune):
        """
        Set rune's efficiency with/without grind
        :param rune: raw rune data
        :type rune: list
        """

        self.efficiency, self.efficiency_without_grind = Rune.rune_efficiency(rune)

    def set_rune_expected_efficiency(self, rune):
        """
        Set rune's expected efficiency with/without grind
        :param rune: raw rune data
        :type rune: list
        """

        self.exp_efficiency, self.exp_efficiency_without_grind = Rune.rune_expected_efficiency(rune)

    """ ====================================================================
                                Static Methods
    ==================================================================== """

    @staticmethod
    def get_rune_type(rune_id):
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
            99: "Immemorial"
        }

        return name_map[rune_id]

    @staticmethod
    def get_sub_type(rune_id):
        """
        convert rune sub type to string
        """

        sub_type_map = {
            0: None,
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

        return sub_type_map[rune_id]

    @staticmethod
    def get_rune_grade(rune_id, shorten=True):
        """
        return rune grade (Currently)
        """

        if shorten:
            rune_class_map = {
                0: 'U',  # unknown
                1: 'C',  # common
                2: 'M',  # magic
                3: 'R',  # rare
                4: 'H',  # hero
                5: 'L',  # legend
            }

        else:
            rune_class_map = {
                0: 'Unknown',
                1: 'Common',
                2: 'Magic',
                3: 'Rare',
                4: 'Hero',
                5: 'Legend',
            }

        return rune_class_map[rune_id]

    @staticmethod
    def get_rune_stat(stats, include_grind=True):
        """
        :param stats: raw data of sub stats
        :type stats: list
        :param include_grind: options to include grind upgrade or not
        :type include_grind: bool
        :return: tuple of sub type and value
        :rtype: tuple
        """

        sub_type = Rune.get_sub_type(stats[0])
        value = stats[1]

        if len(stats) > 2 and include_grind:
            grind = stats[3]
        else:
            grind = 0

        return sub_type, (value + grind)

    @staticmethod
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

    @staticmethod
    def max_roll_substats(rune_type):
        """
        return max roll of sub stat
        """

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

        if rune_type in sub_type_max:
            return sub_type_max[rune_type]

        # undesired atk flat, hp flat, and def flat
        else:
            return 99999999999

    @staticmethod
    def substats_to_dense(substat_list):
        """
        Convert list of substats to dense form
        :param substat_list:
        :type substat_list:
        :return:
        :rtype:
        """

        template = {

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

        # Update the value
        for substat in substat_list:
            template[substat[0]] = substat[1]

        # Densify
        return tuple([x for x in template.values()])

    @staticmethod
    def rune_efficiency(rune):
        """
        Finding rune current efficiency
        """

        # Rune primary stats in tuple eg: ("HP flat" , 580)
        rune_primary_stat = Rune.get_rune_stat(rune['pri_eff'])

        # Rune secondary stats (sub stats)
        rune_subs_list_raw = rune['sec_eff']

        substats_roll_score = 0
        substats_roll_without_grind_score = 0

        for substat in rune_subs_list_raw:
            rune_substats = Rune.get_rune_stat(substat, include_grind=True)
            rune_substats_without_grind = Rune.get_rune_stat(substat, include_grind=False)

            substats_roll_score += rune_substats[1] / Rune.max_roll_substats(rune_substats[0])
            substats_roll_without_grind_score += rune_substats_without_grind[1] / Rune.max_roll_substats(rune_substats_without_grind[0])

        # Rune innate stat
        rune_static_stat = Rune.get_rune_stat(rune['prefix_eff'], include_grind=True)
        substats_roll_score += rune_static_stat[1] / Rune.max_roll_substats(rune_static_stat[0])
        substats_roll_without_grind_score += rune_static_stat[1] / Rune.max_roll_substats(rune_static_stat[0])  # Inate stat can't be grinded ATM

        # Sum all score
        primary_score = rune_primary_stat[1] / Rune.max_roll(rune_primary_stat[0])
        final_score = (primary_score + substats_roll_score) / 2.8
        final_score_without_grind = (primary_score + substats_roll_without_grind_score) / 2.8

        return final_score, final_score_without_grind

    @staticmethod
    def rune_expected_efficiency(rune):
        """
        Return rune expected efficiency at +12
        """

        def probability_new_roll(avail_sub, roll_count, rune_slot):
            """
            Calculate probability of rolling into a new good stat
            :param avail_sub: subs owned by rune
            :type avail_sub: list
            :param roll_count: how many roll still available
            :type roll_count: int
            :param rune_slot: rune's slot (slot 1 and 3 has special condition)
            :type rune_slot: int
            """

            def expectation(fgood, fbad, rc_l):
                """
                Calculate of how many roll into 'good' stat  (hyper geometry dist mean (n * k/N)
                :param fgood: available good stat un rolled
                :type fgood: int
                :param fbad: available good stat un rolled
                :type fbad: int
                :param rc_l: how many roll available
                :type rc_l: int
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

                # Special condition of slot 1 (no def% and def+) and 3 (no atk% and atk+)
                if rune_slot == 1 or rune_slot == 3:
                    fgood -= 1  # atk% or def%
                    fbad -= 1  # atk+ or def+

                # Special assumption that slot 2 4 6 has 'good' primary stat (percents), and 1 3 5 has 'bad' primary stat (flats)
                if rune_slot % 2 == 0:
                    fgood -= 1  # definitely single type of good stat is used already for primary
                else:
                    fbad -= 1  # definitely single type of bad stat is used already for primary

                # Statistic
                expected_roll_into_good = expectation(fgood, fbad, roll_count)
                prob_getting_good = expected_roll_into_good / roll_count

            return prob_getting_good

        def probability_avail(avail_sub):
            """
            Calculate probability to roll into good stat for available stats
            :param avail_sub: available stats of runes
            :type avail_sub: list
            """

            # List of good and bad stats
            good = ["HP%", "ATK%", "DEF%", "SPD", "CRate", "CDmg", "RES", "ACC"]
            bad = ["HP flat", "ATK flat", "DEF flat"]

            # Count good and bad stats owned by rune
            cgood = len([x for x in avail_sub if x in good])
            cbad = len([x for x in avail_sub if x in bad])

            prob_getting_good = cgood / (cgood + cbad)

            return prob_getting_good

        # Get rune sub stats, do current eff count
        rune_subs_list_raw = rune['sec_eff']
        rune_subs_list_type = []

        substats_roll_score = 0
        substats_roll_without_grind_score = 0

        for substat in rune_subs_list_raw:
            rune_substats = Rune.get_rune_stat(substat, include_grind=True)
            rune_substats_without_grind = Rune.get_rune_stat(substat, include_grind=False)

            rune_subs_list_type.append(rune_substats[0])

            substats_roll_score += rune_substats[1] / Rune.max_roll_substats(rune_substats[0])
            substats_roll_without_grind_score += rune_substats_without_grind[1] / Rune.max_roll_substats(rune_substats_without_grind[0])

        # Get rune innate stat, do current eff count
        rune_static_stat = Rune.get_rune_stat(rune['prefix_eff'], include_grind=True)
        substats_roll_score += rune_static_stat[1] / Rune.max_roll_substats(rune_static_stat[0])
        substats_roll_without_grind_score += rune_static_stat[1] / Rune.max_roll_substats(rune_static_stat[0])  # Inate stat can't be grinded ATM

        # ============================================= #
        #                   forecast part               #
        # ============================================= #

        rune_subs_upgrade_avg_eff = 47 / 59  # 6 star sub upgrade min 35 max 59, avg 47...
        rune_level = rune['upgrade_curr']
        rune_slot = rune['slot_no']

        # count how many times NEW sub available
        rune_new_stat_upgrade_count = 4 - min(len(rune_subs_list_type), 4)

        # calculate point earned by rolling into NEW stats
        rune_subs_list_type.append(rune_static_stat)
        roll_to_good_probability = probability_new_roll(rune_subs_list_type, rune_new_stat_upgrade_count, rune_slot)
        rune_upgrade_new_point = rune_new_stat_upgrade_count * roll_to_good_probability * rune_subs_upgrade_avg_eff * 0.2

        # count how many times sub upgrade available
        rune_upgrade_count = 4 - min(rune_level // 3, 4)
        rune_subs_upgrade_avail = rune_upgrade_count - rune_new_stat_upgrade_count

        # calculate point earned by rolling into AVAILABLE stats
        rune_upgrade_avail_point = rune_subs_upgrade_avail * probability_avail(rune_subs_list_type) * rune_subs_upgrade_avg_eff * 0.2

        # Sum those points
        forecast_score = rune_upgrade_new_point + rune_upgrade_avail_point

        # Primary point for primary stat
        if rune_level > 12:
            primary_score = 1
        else:
            primary_score = 0.75  # around +12

        final_score = (primary_score + substats_roll_score + forecast_score) / 2.8  # 1 + 9 x 0.2 max roll
        final_score_without_grind = (primary_score + substats_roll_without_grind_score + forecast_score) / 2.8  # 1 + 9 x 0.2 max roll

        return final_score, final_score_without_grind
