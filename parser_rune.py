from data_mapping import DataMappingCollection

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

    RUNE_SUBS_UPGRADE_AVG_EFF = 47 / 59  # 6 star sub upgrade min 35 max 59, avg 47...

    def __init__(self, rune):

        # Default initialization
        self.slot = rune['slot_no']
        self.stars = rune['class']
        self.grade = Rune.get_rune_grade(rune['rank'])
        self.base_grade = Rune.get_rune_grade(rune['extra'])
        self.type = Rune.get_rune_set(rune['set_id'])
        self.level = rune['upgrade_curr']
        self.main = Rune.get_rune_stat(rune['pri_eff'])

        self.loc = None
        self.innate = None
        self.substats = None
        self.substats_without_grind = None
        self.dense_substats = None
        self.grind_values = None
        self.enchant_type = None
        self.efficiency = 0
        self.exp_efficiency = 0
        self.efficiency_without_grind = 0
        self.exp_efficiency_without_grind = 0

        self.set_innate(rune['prefix_eff'])
        self.set_substats(rune['sec_eff'])
        self.set_substats(rune['sec_eff'], include_grind=False)
        self.set_dense_substats()
        self.set_grind_values(rune['sec_eff'])
        self.set_enchant_type(rune['sec_eff'])

        self.set_rune_efficiencies()
        self.set_rune_expected_efficiency()

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

    def set_substats(self, rune_substat_raw, include_grind=True):
        """
        Getting sub stats
        """

        substats = []
        for raw_substat in rune_substat_raw:
            substat = Rune.get_rune_stat(raw_substat, include_grind=include_grind)
            substats.append(substat)

        if include_grind:
            self.substats = substats
        else:
            self.substats_without_grind = substats

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

            sub_type = Rune.get_rune_stat_type(stat[0])

            # Skip crate, cdmg, res, acc since they can't be grinded
            if sub_type not in self.grind_values:
                continue

            # Update dictionary's value
            if len(stat) > 2:
                self.grind_values[sub_type] = stat[3]
            else:
                self.grind_values[sub_type] = 0

    def set_enchant_type(self, substats):
        """
        Set rune enchantment type if the rune is enchanted
        :param substats: owned substats
        :type substats: list of str
        """

        for stat in substats:
            if Rune.is_stat_enchanted(stat):
                self.enchant_type = Rune.get_rune_stat_type(stat[0])
                break

    def set_rune_efficiencies(self):
        """
        Set rune's efficiency with and without grind
        """

        self.efficiency = Rune.rune_efficiency(self, include_grind=True)
        self.efficiency_without_grind = Rune.rune_efficiency(self, include_grind=False)

    def set_rune_expected_efficiency(self):
        """
        Set rune's expected efficiency with and without grind
        """

        self.exp_efficiency = Rune.rune_expected_efficiency(self, include_grind=True)
        self.exp_efficiency_without_grind = Rune.rune_expected_efficiency(self, include_grind=False)

    def get_owned_all_stats_type(self):
        """
        Return all stats own by a rune (main, innate, substats)
        """

        owned_stats = [self.main[0]]

        if self.innate is not None:
            owned_stats.append(self.innate[0])

        owned_stats += self._get_owned_substats_type()

        return owned_stats

    def _get_owned_stat_roll_chance(self):
        """
        Count how many times OWNED sub upgrade available
        """

        available_upgrade_chance = 4 - min(self.level // 3, 4)
        return available_upgrade_chance - self._get_new_stat_roll_chance()

    def _get_new_stat_roll_chance(self):
        """
        Count how many times NEW sub available 
        """

        return 4 - min(len(self.substats), 4)

    def _get_owned_substats_type(self):
        """
        :return: owned substats (only the stat type)
        :rtype: list of str
        """

        return [stat[0] for stat in self.substats]

    def _compute_primary_score(self):
        """
        Get partial efficiency score based on primary stat
        """

        return self.main[1] / Rune.max_roll(self.main[0])

    def _forecast_primary_score(self):
        """
        Predict partial efficiency score based on primary stat,
        assumption: normally rune upgraded to +12 at least
        """

        if self.level > 12:
            return 1
        else:
            return 0.75  # around +12

    def _compute_roll_score(self, include_grind):
        """
        Calculate partial rune efficiency based on roll (substat upgrade) results
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: partial rune efficiency
        :rtype: float
        """

        if include_grind:
            substats = self.substats
        else:
            substats = self.substats_without_grind

        substats_roll_score = 0
        for substat in substats:
            substats_roll_score += substat[1] / Rune.max_roll_substats(substat[0])

        return substats_roll_score

    def _compute_innate_score(self):
        """
        Get partial efficiency score based on innate stat
        """

        if self.innate is not None:
            return self.innate[1] / Rune.max_roll_substats(self.innate[0])
        else:
            return 0

    def _forecast_owned_stat_upgrade_score(self):

        def count_owned_good_bad_substats(available_sub):
            """
            Count how many good substats and bad substats that already owned by a rune
            """

            # List of good and bad stats
            good_substat = ["HP%", "ATK%", "DEF%", "SPD", "CRate", "CDmg", "RES", "ACC"]
            bad_substat = ["HP flat", "ATK flat", "DEF flat"]

            # Count good and bad stats owned by rune
            owned_good = len([x for x in available_sub if x in good_substat])
            owned_bad = len([x for x in available_sub if x in bad_substat])

            return owned_good, owned_bad

        def probability_owned_stat(available_sub):
            """
            Calculate probability to roll into good stat for owned stats
            :param available_sub: available stats of runes
            :type available_sub: list
            """

            count_good, count_bad = count_owned_good_bad_substats(available_sub)
            return count_good / (count_good + count_bad)

        roll_chance = self._get_owned_stat_roll_chance()
        owned_substats = self._get_owned_substats_type()

        roll_to_good_probability = probability_owned_stat(owned_substats)
        return roll_chance * roll_to_good_probability * Rune.RUNE_SUBS_UPGRADE_AVG_EFF * 0.2

    def _forecast_new_stat_upgrade_score(self):

        def count_available_good_bad_substats(available_sub, rune_slot):
            """
            Count how many good substats and bad substats that can be acuired as new stat
            """

            # List of good and bad stats
            good_substat = ["HP%", "ATK%", "DEF%", "SPD", "CRate", "CDmg", "RES", "ACC"]
            bad_substat = ["HP flat", "ATK flat", "DEF flat"]

            # Count available good and bad stats for rolling
            available_good = len([x for x in good_substat if x not in available_sub])
            available_bad = len([x for x in bad_substat if x not in available_sub])

            # Special condition of slot 1 (no def% and def+) and 3 (no atk% and atk+)
            if rune_slot == 1 or rune_slot == 3:
                available_good -= 1  # atk% or def%
                available_bad -= 1  # atk+ or def+

            # Special assumption that slot 2 4 6 has 'good' primary stat (percents), and 1 3 5 has 'bad' primary stat (flats)
            if rune_slot % 2 == 0:
                available_good -= 1  # definitely single type of good stat is used already for primary
            else:
                available_bad -= 1  # definitely single type of bad stat is used already for primary

            return available_good, available_bad

        def probability_new_roll(available_sub, available_rolls, rune_slot):
            """
            Calculate probability of rolling into a new good stat
            :param available_sub: subs owned by rune
            :type available_sub: list
            :param available_rolls: how many roll still available
            :type available_rolls: int
            :param rune_slot: rune's slot (slot 1 and 3 has special condition)
            :type rune_slot: int
            """

            def expectation(available_good_substat, available_bad_substat, avail_rolls):
                """
                Calculate of how many roll into 'good' stat  (hyper geometry dist mean (n * k/N)
                """

                return avail_rolls * (available_good_substat / (available_good_substat + available_bad_substat))

            # If rune is already at +12, no possible new roll, therefor zero probability
            if available_rolls <= 0:
                return 0

            # Count number of good and bad stats
            available_good_substat, available_bad_substat = count_available_good_bad_substats(available_sub, rune_slot)

            # Statistic
            expected_roll_into_good = expectation(available_good_substat, available_bad_substat, available_rolls)
            prob_getting_good = expected_roll_into_good / available_rolls

            return prob_getting_good

        roll_chance = self._get_new_stat_roll_chance()
        owned_substats = self._get_owned_substats_type()

        # Take innate stat into consideration when predicting NEW stats
        if self.innate is not None:
            owned_substats += [self.innate]

        roll_to_good_probability = probability_new_roll(owned_substats, roll_chance, rune_slot=self.slot)
        return roll_chance * roll_to_good_probability * Rune.RUNE_SUBS_UPGRADE_AVG_EFF * 0.2

    """ ====================================================================
                                Static Methods
    ==================================================================== """

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
    def get_rune_stat(stats, include_grind=True):
        """
        :param stats: raw data of sub stats
        :type stats: list
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: tuple of sub type and value
        :rtype: tuple
        """

        sub_type = Rune.get_rune_stat_type(stats[0])
        value = stats[1]
        grindable = len(stats) > 2

        if grindable and include_grind:
            grind = stats[3]
        else:
            grind = 0

        return sub_type, (value + grind)

    @staticmethod
    def max_roll(primary_stat):
        return DataMappingCollection.get_rune_primary_stat_max_value(primary_stat)

    @staticmethod
    def max_roll_substats(sub_stat):
        return DataMappingCollection.get_rune_sub_stat_max_value(sub_stat)

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
    def rune_efficiency(rune, include_grind):
        """
        Finding rune's current efficiency
        :param rune: instance of Rune which's efficiency gonna be calculated
        :type rune: Rune
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: rune's efficiency
        :rtype: float
        """

        primary_score = rune._compute_primary_score()
        innate_score = rune._compute_innate_score()
        substats_roll_score = rune._compute_roll_score(include_grind)

        # Sum all score
        return Rune._compute_final_score(primary_score, innate_score, substats_roll_score)

    @staticmethod
    def rune_expected_efficiency(rune, include_grind):
        """
        Finding rune's expected efficiency at +12 (4 times roll)
        :param rune: instance of Rune which's efficiency gonna be calculated
        :type rune: Rune
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: rune's expected efficiency
        :rtype: float
        """

        primary_score = rune._forecast_primary_score()
        innate_score = rune._compute_innate_score()
        substats_roll_score = rune._compute_roll_score(include_grind)
        owned_stat_upgrade_score = rune._forecast_owned_stat_upgrade_score()
        new_stat_upgrade_score = rune._forecast_new_stat_upgrade_score()

        return Rune._compute_final_score(primary_score, innate_score, substats_roll_score, new_stat_upgrade_score, owned_stat_upgrade_score)

    @staticmethod
    def _compute_final_score(*args):
        """
        Compute rune efficiency score (2.8 is from  1 main stat + (9 times roll x 0.2 max efficiency))
        :param args: list of score
        :type args: float
        :return: final efficiency score
        :rtype: float
        """

        score = 0
        for x in args:
            score += x

        return score / 2.8
