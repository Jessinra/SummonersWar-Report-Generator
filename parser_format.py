class ExcelFormatter:
    def __init__(self, workbook, worksheet, format_type):

        self.workbook = workbook
        self.worksheet = worksheet
        self.apply_format(format_type)

    def apply_format(self, format_type):
        """
        Get excel formatting for displaying output
        """

        if format_type == "Rune":
            self._apply_rune_format()

        elif format_type == "Monster eff":
            self._apply_monster_eff_format()

        elif format_type == "Grinds":
            self._apply_grind_format()

        elif format_type == "Enchant":
            self._apply_enchant_format()

    def _apply_rune_format(self):

        format_5star = self.workbook.add_format({'bg_color': '#632d17', 'font_color': '#eadbd5'})

        format_legend = self.workbook.add_format({'bg_color': '#f9e7a9', 'font_color': '#2B2925'})
        format_hero = self.workbook.add_format({'bg_color': '#f4d9f9', 'font_color': '#2B2925'})
        format_rare = self.workbook.add_format({'bg_color': '#d5f0f2', 'font_color': '#2B2925'})

        format_del_candidate = self.workbook.add_format({'bg_color': '#58595b', 'font_color': '#ffaaaa'})
        format_header = self.workbook.add_format({'bg_color': '#30305e', 'font_color': '#FFFFFF', 'rotation': '45',
                                                  'valign': 'vcenter', 'align': 'center', 'bold': True})

        format_border = self.workbook.add_format({'bg_color': '#030930', 'font_color': '#ef4a4a'})

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        format_left_with_indent = self.workbook.add_format({'indent': 1})

        self.worksheet.conditional_format('F1:F1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': '5',
                                                       'format': format_5star})

        self.worksheet.conditional_format('D1:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'L',
                                                       'format': format_legend})
        self.worksheet.conditional_format('D1:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'H',
                                                       'format': format_hero})
        self.worksheet.conditional_format('D2:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'R',
                                                       'format': format_rare})

        self.worksheet.conditional_format('G1:G1600', {'type': '3_color_scale'})

        # Color scale for substats
        self.worksheet.conditional_format('K1:R1600', {'type': '3_color_scale',
                                                       'min_color': '#e5eeff',
                                                       'mid_color': '#96aedd',
                                                       'max_color': '#3e74dd'})

        self.worksheet.conditional_format('S1:S1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})
        self.worksheet.conditional_format('T1:T1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})
        self.worksheet.conditional_format('U1:U1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})

        # Color scale for efficiency
        self.worksheet.conditional_format('X1:X1600', {'type': 'bottom',
                                                       'criteria': '%',
                                                       'value': '20',
                                                       'format': format_del_candidate})

        self.worksheet.conditional_format('Y1:Y1600', {'type': 'bottom',
                                                       'criteria': '%',
                                                       'value': '20',
                                                       'format': format_del_candidate})

        self.worksheet.conditional_format('AA1:AA1600', {'type': 'bottom',
                                                       'criteria': '%',
                                                       'value': '20',
                                                       'format': format_del_candidate})
                                                       
        self.worksheet.conditional_format('W1:AA1600', {'type': '3_color_scale'})

        # Rune Informations
        self.worksheet.set_column('A:G', None, format_center)
        self.worksheet.set_column('K:AC', None, format_center)
        self.worksheet.set_column('A:A', 5)
        self.worksheet.set_column('B:B', 13.5)
        self.worksheet.set_column('C:C', 5)
        self.worksheet.set_column('D:D', 4.2)
        self.worksheet.set_column('E:E', 4.2)
        self.worksheet.set_column('F:F', 4.33)
        self.worksheet.set_column('G:G', 4.33)
        self.worksheet.set_column('H:H', 18.6, format_left_with_indent)
        self.worksheet.set_column('I:I', 15, format_left_with_indent)

        self.worksheet.set_column('J:J', 0.3, format_border)  # border
        
        # Substats
        self.worksheet.set_column('K:K', 6)
        self.worksheet.set_column('L:L', 6)
        self.worksheet.set_column('M:M', 6)
        self.worksheet.set_column('N:N', 6)
        self.worksheet.set_column('O:O', 6)
        self.worksheet.set_column('P:P', 6)
        self.worksheet.set_column('Q:Q', 6)
        self.worksheet.set_column('R:R', 6)
        self.worksheet.set_column('S:S', 6)
        self.worksheet.set_column('T:T', 6)
        self.worksheet.set_column('U:U', 6)

        self.worksheet.set_column('V:V', 0.3, format_border)
        
        # Efficiencies
        self.worksheet.set_column('W:W', 7.2)
        self.worksheet.set_column('X:X', 7.2)
        self.worksheet.set_column('Y:Y', 7.2)
        self.worksheet.set_column('Z:Z', 7.2)
        self.worksheet.set_column('AA:AA', 7.2)

        self.worksheet.set_column('AB:AB', 15)

        self.worksheet.autofilter('A1:AB1600')
        self.worksheet.set_row(0, 58, format_header)
        self.worksheet.freeze_panes(1, 0)

    def _apply_monster_eff_format(self):

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        format_header = self.workbook.add_format({'bg_color': '#30305e', 'font_color': '#FFFFFF', 'valign': 'vcenter', 'align': 'center', 'bold': True})
        self.worksheet.conditional_format('C1:C600', {'type': '3_color_scale'})
        self.worksheet.conditional_format('D1:D600', {'type': '3_color_scale'})

        self.worksheet.set_column('A:D', None, format_center)
        self.worksheet.set_column('A:A', 4)
        self.worksheet.set_column('B:B', 15)
        self.worksheet.set_column('C:C', 13.2)
        self.worksheet.set_column('D:D', 13.2)

        self.worksheet.set_row(0, 58, format_header)
        self.worksheet.freeze_panes(1, 0)

    def _apply_grind_format(self):

        format_5star = self.workbook.add_format({'bg_color': '#632d17', 'font_color': '#eadbd5'})

        format_legend = self.workbook.add_format({'bg_color': '#f9e7a9', 'font_color': '#2B2925'})
        format_hero = self.workbook.add_format({'bg_color': '#f4d9f9', 'font_color': '#2B2925'})
        format_rare = self.workbook.add_format({'bg_color': '#d5f0f2', 'font_color': '#2B2925'})
        format_flat = self.workbook.add_format({'bg_color': '#dfdee2', 'font_color': '#0d0133'})
        format_border = self.workbook.add_format({'bg_color': '#030930', 'font_color': '#030930'})

        format_header_grind = self.workbook.add_format({'bg_color': '#3e135b', 'font_color': '#FFFFFF', 'rotation': '45',
                                                        'valign': 'vcenter', 'align': 'center', 'bold': True})

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        format_left_with_indent = self.workbook.add_format({'indent': 1})

        self.worksheet.conditional_format('F1:F1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': '5',
                                                       'format': format_5star})

        self.worksheet.conditional_format('D1:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'L',
                                                       'format': format_legend})
        self.worksheet.conditional_format('D1:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'H',
                                                       'format': format_hero})
        self.worksheet.conditional_format('D2:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'R',
                                                       'format': format_rare})
        self.worksheet.conditional_format('G1:G1600', {'type': '3_color_scale'})
        
        # Color scale for substats
        self.worksheet.conditional_format('K1:R1600', {'type': '3_color_scale',
                                                       'min_color': '#e5eeff',
                                                       'mid_color': '#96aedd',
                                                       'max_color': '#3e74dd'})

        self.worksheet.conditional_format('S1:S1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})
        self.worksheet.conditional_format('T1:T1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})
        self.worksheet.conditional_format('U1:U1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})

        # Color scale for efficiency
        self.worksheet.conditional_format('W1:AA1600', {'type': '3_color_scale'})



        self.worksheet.conditional_format('AE1:AE1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'Legend',
                                                       'format': format_legend})

        self.worksheet.conditional_format('AE1:AE1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'Hero',
                                                       'format': format_hero})
        self.worksheet.conditional_format('AE2:AE1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'Rare',
                                                       'format': format_rare})

        # Rune Informations
        self.worksheet.set_column('A:G', None, format_center)
        self.worksheet.set_column('K:AF', None, format_center)
        self.worksheet.set_column('A:A', 5)
        self.worksheet.set_column('B:B', 13.5)
        self.worksheet.set_column('C:C', 5)
        self.worksheet.set_column('D:D', 4.2)
        self.worksheet.set_column('E:E', 4.2)
        self.worksheet.set_column('F:F', 4.33)
        self.worksheet.set_column('G:G', 4.33)
        self.worksheet.set_column('H:H', 18.6, format_left_with_indent)
        self.worksheet.set_column('I:I', 15, format_left_with_indent)
        
        self.worksheet.set_column('J:J', 0.3, format_border)  # border

        # Substats
        self.worksheet.set_column('K:K', 6)
        self.worksheet.set_column('L:L', 6)
        self.worksheet.set_column('M:M', 6)
        self.worksheet.set_column('N:N', 6)
        self.worksheet.set_column('O:O', 6)
        self.worksheet.set_column('P:P', 6)
        self.worksheet.set_column('Q:Q', 6)
        self.worksheet.set_column('R:R', 6)
        self.worksheet.set_column('S:S', 6)
        self.worksheet.set_column('T:T', 6)
        self.worksheet.set_column('U:U', 6)

        self.worksheet.set_column('V:V', 0.3, format_border)

        # Efficiencies
        self.worksheet.set_column('W:W', 7.2)
        self.worksheet.set_column('X:X', 7.2)
        self.worksheet.set_column('Y:Y', 7.2)
        self.worksheet.set_column('Z:Z', 7.2)
        self.worksheet.set_column('AA:AA', 7.2)

        self.worksheet.set_column('AB:AB', 15)

        self.worksheet.set_column('AC:AC', 0.3, format_border)

        # Grind section
        self.worksheet.set_column('AD:AD', 13.5)
        self.worksheet.set_column('AE:AE', 8)
        self.worksheet.set_column('AF:AF', 9.2)

        self.worksheet.autofilter('A1:AF1600')
        self.worksheet.set_row(0, 58, format_header_grind)
        self.worksheet.freeze_panes(1, 0)

    def _apply_enchant_format(self):

        format_5star = self.workbook.add_format({'bg_color': '#632d17', 'font_color': '#eadbd5'})

        format_legend = self.workbook.add_format({'bg_color': '#f9e7a9', 'font_color': '#2B2925'})
        format_hero = self.workbook.add_format({'bg_color': '#f4d9f9', 'font_color': '#2B2925'})
        format_rare = self.workbook.add_format({'bg_color': '#d5f0f2', 'font_color': '#2B2925'})
        format_flat = self.workbook.add_format({'bg_color': '#dfdee2', 'font_color': '#0d0133'})
        format_border = self.workbook.add_format({'bg_color': '#030930', 'font_color': '#030930'})

        format_header_grind = self.workbook.add_format({'bg_color': '#3e135b', 'font_color': '#FFFFFF', 'rotation': '45',
                                                        'valign': 'vcenter', 'align': 'center', 'bold': True})

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        format_left_with_indent = self.workbook.add_format({'indent': 1})

        self.worksheet.conditional_format('F1:F1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': '5',
                                                       'format': format_5star})

        self.worksheet.conditional_format('D1:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'L',
                                                       'format': format_legend})
        self.worksheet.conditional_format('D1:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'H',
                                                       'format': format_hero})
        self.worksheet.conditional_format('D2:E1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'R',
                                                       'format': format_rare})
        self.worksheet.conditional_format('G1:G1600', {'type': '3_color_scale'})
        
        # Color scale for substats
        self.worksheet.conditional_format('K1:R1600', {'type': '3_color_scale',
                                                       'min_color': '#e5eeff',
                                                       'mid_color': '#96aedd',
                                                       'max_color': '#3e74dd'})

        self.worksheet.conditional_format('S1:S1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})
        self.worksheet.conditional_format('T1:T1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})
        self.worksheet.conditional_format('U1:U1600', {'type': '3_color_scale',
                                                       'min_color': '#f9e3f5',
                                                       'mid_color': '#fca9ec',
                                                       'max_color': '#ff7ce5'})

        # Color scale for efficiency
        self.worksheet.conditional_format('W1:AA1600', {'type': '3_color_scale'})



        self.worksheet.conditional_format('AE1:AE1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'Legend',
                                                       'format': format_legend})

        self.worksheet.conditional_format('AE1:AE1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'Hero',
                                                       'format': format_hero})
        self.worksheet.conditional_format('AE2:AE1600', {'type': 'text',
                                                       'criteria': 'containing',
                                                       'value': 'Rare',
                                                       'format': format_rare})

        # Rune Informations
        self.worksheet.set_column('A:G', None, format_center)
        self.worksheet.set_column('K:AF', None, format_center)
        self.worksheet.set_column('A:A', 5)
        self.worksheet.set_column('B:B', 13.5)
        self.worksheet.set_column('C:C', 5)
        self.worksheet.set_column('D:D', 4.2)
        self.worksheet.set_column('E:E', 4.2)
        self.worksheet.set_column('F:F', 4.33)
        self.worksheet.set_column('G:G', 4.33)
        self.worksheet.set_column('H:H', 18.6, format_left_with_indent)
        self.worksheet.set_column('I:I', 15, format_left_with_indent)
        
        self.worksheet.set_column('J:J', 0.3, format_border)  # border

        # Substats
        self.worksheet.set_column('K:K', 6)
        self.worksheet.set_column('L:L', 6)
        self.worksheet.set_column('M:M', 6)
        self.worksheet.set_column('N:N', 6)
        self.worksheet.set_column('O:O', 6)
        self.worksheet.set_column('P:P', 6)
        self.worksheet.set_column('Q:Q', 6)
        self.worksheet.set_column('R:R', 6)
        self.worksheet.set_column('S:S', 6)
        self.worksheet.set_column('T:T', 6)
        self.worksheet.set_column('U:U', 6)

        self.worksheet.set_column('V:V', 0.3, format_border)
        
        # Efficiencies
        self.worksheet.set_column('W:W', 7.2)
        self.worksheet.set_column('X:X', 7.2)
        self.worksheet.set_column('Y:Y', 7.2)
        self.worksheet.set_column('Z:Z', 7.2)
        self.worksheet.set_column('AA:AA', 7.2)

        self.worksheet.set_column('AB:AB', 15)

        self.worksheet.set_column('AC:AC', 0.3, format_border)

        # Enchant sections
        self.worksheet.set_column('AD:AD', 13.5)
        self.worksheet.set_column('AE:AE', 8)
        self.worksheet.set_column('AF:AF', 9.2)

        self.worksheet.autofilter('A1:AF1600')
        self.worksheet.set_row(0, 58, format_header_grind)
        self.worksheet.freeze_panes(1, 0)