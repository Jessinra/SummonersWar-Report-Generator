from data_mapping import DataMappingCollection
from parser_rune import RuneParser


class Rune:
    SUBS_UPGRADE_AVG_EFF = 47 / 59  # 6 star sub upgrade min 35 max 59, avg 47...
    SUBS_MAX_EFFICIENCY = 2.8  # 2.8 is from 1 main stat + (9 times roll x 0.2 max efficiency)

    def __init__(self, rune):

        self.slot = rune['slot_no']
        self.stars = RuneParser.get_rune_stars(rune['class'])
        self.level = rune['upgrade_curr']
        self.grade = RuneParser.get_rune_grade_shorten(rune['rank'])
        self.base_grade = RuneParser.get_rune_grade_shorten(rune['extra'])
        self.rune_set = RuneParser.get_rune_set(rune['set_id'])
        self.main = RuneParser.get_rune_stat(rune['pri_eff'])

        self.loc = None
        self.innate = None
        self.substats = []
        self.substats_without_grind = []
        self.dense_substats = None
        self.grind_values = None
        self.enchant_type = None
        self.enchant_value = 0
        self.efficiency = 0
        self.exp_efficiency_12 = 0
        self.exp_efficiency_15 = 0
        self.efficiency_without_grind = 0
        self.exp_efficiency_12_without_grind = 0
        self.exp_efficiency_15_without_grind = 0
        self.enhance_coeficient = 0

        self._set_innate_if_available(rune['prefix_eff'])
        self._set_substats_with_grind(rune['sec_eff'])
        self._set_substats_without_grind(rune['sec_eff'])
        self._set_dense_substats()
        self._set_grind_values(rune['sec_eff'])
        self._set_enchanted_stat_type(rune['sec_eff'])

        self._set_rune_efficiencies()
        self._set_rune_expected_efficiency()
        self._set_rune_enhance_coeficient()

    def _set_innate_if_available(self, innate):

        self.innate = RuneParser.get_rune_stat(innate)
        self._remove_innate_if_none()

    def _remove_innate_if_none(self):

        if self.innate[0] is None:
            self.innate = None

    def _set_substats_with_grind(self, rune_substat_raw):

        for raw_substat in rune_substat_raw:
            substat = RuneParser.get_rune_stat(raw_substat)
            self.substats.append(substat)

    def _set_substats_without_grind(self, rune_substat_raw):

        for raw_substat in rune_substat_raw:
            substat = RuneParser.get_rune_stat_without_grind(raw_substat)
            self.substats_without_grind.append(substat)

    def _set_dense_substats(self):

        self.dense_substats = RuneParser.substats_to_dense_form(self.substats)

    def _set_grind_values(self, substats):

        self.grind_values = RuneParser.create_substats_map()
        for stat in substats:
            self._set_grind_value(stat)

    def _set_grind_value(self, stat):

        sub_type = RuneParser.get_rune_stat_type(stat)
        if DataMappingCollection.is_substat_grindable(sub_type):
            self.grind_values[sub_type] = RuneParser.get_rune_grind_value(stat)

    def _set_enchanted_stat_type(self, substats):
        """
        Set rune enchantment type if the rune is enchanted
        """

        for stat in substats:
            if RuneParser.is_stat_enchanted(stat):
                self.enchant_type, self.enchant_value = RuneParser.get_rune_stat(stat)
                break

    def _set_rune_efficiencies(self):
        """
        Set rune's efficiency with and without grind
        """

        self.efficiency = self._rune_efficiency(include_grind=True)
        self.efficiency_without_grind = self._rune_efficiency(include_grind=False)

    def _rune_efficiency(self, include_grind):
        """
        Finding rune's current efficiency
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: rune's efficiency
        :rtype: float
        """

        primary_score = self._compute_primary_score()
        innate_score = self._compute_innate_score()
        substats_roll_score = self._compute_roll_score(include_grind)

        return Rune._compute_final_score(primary_score, innate_score, substats_roll_score)

    def _compute_primary_score(self):
        """
        Get partial efficiency score based on primary stat
        """

        return self.main[1] / RuneParser.max_roll(self.main[0])

    def _compute_innate_score(self):
        """
        Get partial efficiency score based on innate stat
        """

        if self.innate is not None:
            return self.innate[1] / RuneParser.max_roll_substats(self.innate[0])
        else:
            return 0

    def _compute_roll_score(self, include_grind):
        """
        Calculate partial rune efficiency based on roll (substat upgrade) results
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: partial rune efficiency
        :rtype: float
        """

        substats_roll_score = 0
        substats = self._select_substats_according_to(include_grind)

        for substat in substats:
            substats_roll_score += substat[1] / RuneParser.max_roll_substats(substat[0])

        return substats_roll_score

    def _select_substats_according_to(self, include_grind):

        if include_grind:
            return self.substats
        else:
            return self.substats_without_grind

    @staticmethod
    def _compute_final_score(*args):
        """
        Compute rune efficiency score )
        :param args: list of score
        :type args: float
        :return: final efficiency score
        :rtype: float
        """

        score = 0
        for x in args:
            score += x

        return score / Rune.SUBS_MAX_EFFICIENCY

    def _set_rune_expected_efficiency(self):
        """
        Set rune's expected efficiency with and without grind
        """

        self.exp_efficiency_12, self.exp_efficiency_15 = self._rune_expected_efficiency(include_grind=True)
        self.exp_efficiency_12_without_grind, self.exp_efficiency_15_without_grind = self._rune_expected_efficiency(include_grind=False)

    def _rune_expected_efficiency(self, include_grind):
        """
        Finding rune's expected efficiency at +12 (4 times roll)
        :param include_grind: if set True, applied grind will be counted in efficiency
        :type include_grind: bool
        :return: rune's expected efficiency
        :rtype: float
        """

        primary_score_12 = self._forecast_primary_score(exp_level=12)
        primary_score_15 = self._forecast_primary_score(exp_level=15)
        innate_score = self._compute_innate_score()
        substats_roll_score = self._compute_roll_score(include_grind)
        owned_stat_upgrade_score = self._forecast_owned_stat_upgrade_score()
        new_stat_upgrade_score = self._forecast_new_stat_upgrade_score()

        exp_eff_at_12 = Rune._compute_final_score(primary_score_12, innate_score, substats_roll_score, new_stat_upgrade_score, owned_stat_upgrade_score)
        exp_eff_at_15 = Rune._compute_final_score(primary_score_15, innate_score, substats_roll_score, new_stat_upgrade_score, owned_stat_upgrade_score)

        return exp_eff_at_12, exp_eff_at_15

    def _forecast_primary_score(self, exp_level):
        """
        Predict partial efficiency score based on primary stat,
        assumption: normally rune upgraded to +12 at least
        """
        star_coefficient = self.stars / 6

        if exp_level > 12:
            return 1 * star_coefficient
        else:
            return 0.75 * star_coefficient # expected at +12

    def _forecast_owned_stat_upgrade_score(self):

        roll_chance = self._get_owned_stat_roll_chance()
        roll_to_good_probability = self._probability_owned_stat()

        return roll_chance * roll_to_good_probability * Rune.SUBS_UPGRADE_AVG_EFF * 0.2

    def _get_owned_stat_roll_chance(self):
        """
        Count how many times OWNED sub upgrade available
        """

        available_upgrade_chance = 4 - min(self.level // 3, 4)

        return available_upgrade_chance - self._get_new_stat_roll_chance()

    def _probability_owned_stat(self):
        """
        Calculate probability to roll into good stat for owned stats
        """

        count_good = self._count_owned_good_substats()
        count_bad = self._count_owned_bad_substats()

        return count_good / (count_good + count_bad)

    def _count_owned_good_substats(self):
        """
        Count how many good substats that already owned by a rune
        """

        available_sub = self._get_owned_substats_type()
        good_substat = DataMappingCollection.get_good_substats()
        owned_good = len([x for x in available_sub if x in good_substat])
        return owned_good

    def _count_owned_bad_substats(self):
        """
        Count how many bad substats that already owned by a rune
        """

        available_sub = self._get_owned_substats_type()
        bad_substat = DataMappingCollection.get_bad_substats()
        owned_bad = len([x for x in available_sub if x in bad_substat])
        return owned_bad

    def _get_owned_substats_type(self):
        """
        :return: owned substats (only the stat type)
        :rtype: list of str
        """

        return [stat[0] for stat in self.substats]

    def _forecast_new_stat_upgrade_score(self):

        roll_chance = self._get_new_stat_roll_chance()
        roll_to_good_probability = self._probability_new_roll(roll_chance)

        return roll_chance * roll_to_good_probability * Rune.SUBS_UPGRADE_AVG_EFF * 0.2

    def _get_new_stat_roll_chance(self):
        """
        Count how many times NEW sub available 
        """
        return 4 - min(len(self.substats), 4)

    def _probability_new_roll(self, available_rolls):
        """
        Calculate probability of rolling into a new good stat
        """

        # If rune is already at +12, no possible new roll, therefore zero probability
        if available_rolls <= 0:
            return 0

        # Count number of good and bad stats
        expected_roll_into_good = self.calculate_expectation_into_good_roll(available_rolls)
        prob_getting_good = expected_roll_into_good / available_rolls
        return prob_getting_good

    def calculate_expectation_into_good_roll(self, available_rolls):

        available_good_substat = self._count_available_good_substats()
        available_bad_substat = self._count_available_bad_substats()

        expected_roll_into_good = Rune._expectation(available_good_substat, available_bad_substat, available_rolls)
        return expected_roll_into_good

    def _count_available_good_substats(self):
        """
        Count how many good substats that can be acuired as new stat
        """

        owned_substats = self._get_owned_substats_include_innate()  # Take innate stat into consideration when predicting NEW stats

        good_substat = DataMappingCollection.get_good_substats()
        available_good = len([x for x in good_substat if x not in owned_substats])
        available_good += self._additional_good_point_reduction()
        return available_good

    def _additional_good_point_reduction(self):

        additional_cutoff = 0

        # Special condition of slot 1 (no def%) and 3 (no atk%)
        if self.slot == 1 or self.slot == 3:
            additional_cutoff -= 1

        # Special assumption that slot 2 4 6 has 'good' primary stat (percents)
        if self.slot % 2 == 0:
            additional_cutoff -= 1  # definitely single type of good stat is used already for primary

        return additional_cutoff

    def _count_available_bad_substats(self):
        """
        Count how many bad substats that can be acuired as new stat
        """

        owned_substats = self._get_owned_substats_include_innate()  # Take innate stat into consideration when predicting NEW stats

        bad_substat = DataMappingCollection.get_bad_substats()
        available_bad = len([x for x in bad_substat if x not in owned_substats])
        available_bad += self._additional_bad_point_reduction()
        return available_bad

    def _additional_bad_point_reduction(self):

        additional_cutoff = 0

        # Special condition of slot 1 (no def+) and 3 (no atk+)
        if self.slot == 1 or self.slot == 3:
            additional_cutoff -= 1

        # Special assumption that slot 1 3 5 has 'bad' primary stat (flats)
        if self.slot % 2 != 0:
            additional_cutoff -= 1  # definitely single type of bad stat is used already for primary

        return additional_cutoff

    def _get_owned_substats_include_innate(self):

        owned_substats = self._get_owned_substats_type()
        if self.innate is not None:
            owned_substats += [self.innate[0]]

        return owned_substats

    @staticmethod
    def _expectation(available_good_substat, available_bad_substat, avail_rolls):
        """
        Calculate of how many roll into 'good' stat  (hyper geometry dist mean (n * k/N)
        """

        return avail_rolls * (available_good_substat / (available_good_substat + available_bad_substat))

    def get_owned_all_stats_type(self):
        """
        Return all stats own by a rune (main, innate, substats) : used in apply grind
        """

        owned_stats = [self.main[0]]
        owned_stats += self._get_owned_substats_include_innate()
        return owned_stats

    def _set_rune_enhance_coeficient(self):
        self.enhance_coeficient = 0.5 * self.efficiency_without_grind + 0.25 * self.exp_efficiency_12 + 0.25 * self.efficiency

    def set_loc(self, rune_user):

        self.loc = rune_user

    def get_rune_set(self):
        """ getter used as 'polymorphsm' with enhancement object """

        return self.rune_set

    def is_equiped(self):

        return self.loc != "" and self.loc is not None

    def display_rune_detail(self):
        print("========================")
        print("slot", self.slot)
        print("stars", self.stars)
        print("level", self.level)
        print("grade", self.grade)
        print("base_grade", self.base_grade)
        print("rune_set", self.rune_set)
        print("main", self.main)
        print("loc", self.loc)
        print("innate", self.innate)
        print("substats", self.substats)
        print("substats_without_grind", self.substats_without_grind)
        print("dense_substats", self.dense_substats)
        print("grind_values", self.grind_values)
        print("enchant_type", self.enchant_type)
        print("enchant_value", self.enchant_value)
        print("efficiency", self.efficiency)
        print("exp_efficiency +12", self.exp_efficiency_12)
        print("exp_efficiency +15", self.exp_efficiency_15)
        print("efficiency_without_grind", self.efficiency_without_grind)
        print("exp_efficiency_12_without_grind", self.exp_efficiency_12_without_grind)
        print("enhance_coeficient", self.enhance_coeficient)
        print("========================")
