
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
        
        format_legend = self.workbook.add_format({'bg_color': '#f9e7a9', 'font_color': '#2B2925'})
        format_hero = self.workbook.add_format({'bg_color': '#f4d9f9', 'font_color': '#2B2925'})
        format_rare = self.workbook.add_format({'bg_color': '#d5f0f2', 'font_color': '#2B2925'})

        format_del_candidate = self.workbook.add_format({'bg_color': '#261a17', 'font_color': '#f9525d'})
        format_header = self.workbook.add_format({'bg_color': '#30305e', 'font_color': '#FFFFFF', 'rotation': '45',
                                            'valign': 'vcenter', 'align': 'center', 'bold': True})

        format_border = self.workbook.add_format({'bg_color': '#030930', 'font_color': '#030930'})

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})

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

        self.worksheet.conditional_format('X1:X1600', {'type': 'bottom',
                                                'criteria': '%',
                                                'value': '20',
                                                'format': format_del_candidate})

        self.worksheet.conditional_format('Z1:Z1600', {'type': 'bottom',
                                                'criteria': '%',
                                                'value': '20',
                                                'format': format_del_candidate})

        self.worksheet.set_column('A:G', None, format_center)
        self.worksheet.set_column('K:AA', None, format_center)
        self.worksheet.set_column('A:A', 4)
        self.worksheet.set_column('B:B', 9)
        self.worksheet.set_column('C:C', 4)
        self.worksheet.set_column('D:D', 3.2)
        self.worksheet.set_column('E:E', 3.2)
        self.worksheet.set_column('F:F', 3.33)
        self.worksheet.set_column('G:G', 3.33)
        self.worksheet.set_column('H:H', 14.6)
        self.worksheet.set_column('I:I', 12)

        self.worksheet.set_column('J:J', 0.3, format_border)    # border

        self.worksheet.set_column('K:K', 5.2)
        self.worksheet.set_column('L:L', 5.2)
        self.worksheet.set_column('M:M', 5.2)
        self.worksheet.set_column('N:N', 5.2)
        self.worksheet.set_column('O:O', 5.2)
        self.worksheet.set_column('P:P', 5.2)
        self.worksheet.set_column('Q:Q', 5.2)
        self.worksheet.set_column('R:R', 5.2)
        self.worksheet.set_column('S:S', 5.2)
        self.worksheet.set_column('T:T', 5.2)
        self.worksheet.set_column('U:U', 5.2)

        self.worksheet.set_column('V:V', 0.3, format_border) 

        self.worksheet.set_column('W:W', 6.2)
        self.worksheet.set_column('X:X', 6.2)
        self.worksheet.set_column('Y:Y', 6.2)
        self.worksheet.set_column('Z:Z', 6.2)

        self.worksheet.set_column('AA:AA', 9)

        self.worksheet.autofilter('A1:AA1600')
        self.worksheet.set_row(0, 58, format_header)
        self.worksheet.freeze_panes(1, 0)

    def _apply_monster_eff_format(self):

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        format_header = self.workbook.add_format({'bg_color': '#30305e', 'font_color': '#FFFFFF', 'valign': 'vcenter', 'align': 'center', 'bold': True})

        self.worksheet.set_column('A:D', None, format_center)
        self.worksheet.set_column('A:A', 4)
        self.worksheet.set_column('B:B', 13)
        self.worksheet.set_column('C:C', 13.2)
        self.worksheet.set_column('D:D', 13.2)

        self.worksheet.set_row(0, None, format_header)
        self.worksheet.freeze_panes(1, 0)

    def _apply_grind_format(self):

        format_legend = self.workbook.add_format({'bg_color': '#f9e7a9', 'font_color': '#2B2925'})
        format_hero = self.workbook.add_format({'bg_color': '#f4d9f9', 'font_color': '#2B2925'})
        format_rare = self.workbook.add_format({'bg_color': '#d5f0f2', 'font_color': '#2B2925'})
        format_flat = self.workbook.add_format({'bg_color': '#dfdee2', 'font_color': '#0d0133'})
        format_border = self.workbook.add_format({'bg_color': '#030930', 'font_color': '#030930'})

        format_header_grind = self.workbook.add_format({'bg_color': '#3e135b', 'font_color': '#FFFFFF', 'rotation': '45',
                                                'valign': 'vcenter', 'align': 'center', 'bold': True})

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})

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

        self.worksheet.conditional_format('J2:J1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'flat',
                                                'format': format_flat})                                         

        self.worksheet.conditional_format('R1:R1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'Legend',
                                                'format': format_legend})

        self.worksheet.conditional_format('R1:R1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'Hero',
                                                'format': format_hero})
        self.worksheet.conditional_format('R2:R1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'Rare',
                                                'format': format_rare})

        self.worksheet.conditional_format('G1:G1600', {'type': '3_color_scale'})
        self.worksheet.conditional_format('K1:N1600', {'type': '3_color_scale'})

        self.worksheet.set_column('A:G', None, format_center)
        self.worksheet.set_column('K:AA', None, format_center)
        self.worksheet.set_column('A:A', 4)
        self.worksheet.set_column('B:B', 9)
        self.worksheet.set_column('C:C', 4)
        self.worksheet.set_column('D:D', 3.2)
        self.worksheet.set_column('E:E', 3.2)
        self.worksheet.set_column('F:F', 3.33)
        self.worksheet.set_column('G:G', 3.33)
        self.worksheet.set_column('H:H', 14.6)
        self.worksheet.set_column('I:I', 12)
        self.worksheet.set_column('J:J', 42)

        self.worksheet.set_column('K:K', 6.2)
        self.worksheet.set_column('L:L', 6.2)
        self.worksheet.set_column('M:M', 6.2)
        self.worksheet.set_column('N:N', 6.2)
        self.worksheet.set_column('O:O', 9)

        self.worksheet.set_column('P:P', 0.3, format_border) 

        self.worksheet.set_column('Q:Q', 12.5)        
        self.worksheet.set_column('R:R', 7)
        self.worksheet.set_column('S:S', 7.2)

        self.worksheet.autofilter('A1:S1600')
        self.worksheet.set_row(0, 58, format_header_grind)
        self.worksheet.freeze_panes(1, 0)

    def _apply_enchant_format(self):

        format_legend = self.workbook.add_format({'bg_color': '#f9e7a9', 'font_color': '#2B2925'})
        format_hero = self.workbook.add_format({'bg_color': '#f4d9f9', 'font_color': '#2B2925'})
        format_rare = self.workbook.add_format({'bg_color': '#d5f0f2', 'font_color': '#2B2925'})
        format_flat = self.workbook.add_format({'bg_color': '#dfdee2', 'font_color': '#0d0133'})
        format_border = self.workbook.add_format({'bg_color': '#030930', 'font_color': '#030930'})

        format_header_grind = self.workbook.add_format({'bg_color': '#3e135b', 'font_color': '#FFFFFF', 'rotation': '45',
                                                'valign': 'vcenter', 'align': 'center', 'bold': True})

        format_center = self.workbook.add_format({'valign': 'vcenter', 'align': 'center'})

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

        self.worksheet.conditional_format('J2:J1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'flat',
                                                'format': format_flat})                                         

        self.worksheet.conditional_format('R1:R1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'Legend',
                                                'format': format_legend})

        self.worksheet.conditional_format('R1:R1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'Hero',
                                                'format': format_hero})
        self.worksheet.conditional_format('R2:R1600', {'type': 'text',
                                                'criteria': 'containing',
                                                'value': 'Rare',
                                                'format': format_rare})

        self.worksheet.conditional_format('G1:G1600', {'type': '3_color_scale'})
        self.worksheet.conditional_format('K1:N1600', {'type': '3_color_scale'})

        self.worksheet.set_column('A:G', None, format_center)
        self.worksheet.set_column('K:AA', None, format_center)
        self.worksheet.set_column('A:A', 4)
        self.worksheet.set_column('B:B', 9)
        self.worksheet.set_column('C:C', 4)
        self.worksheet.set_column('D:D', 3.2)
        self.worksheet.set_column('E:E', 3.2)
        self.worksheet.set_column('F:F', 3.33)
        self.worksheet.set_column('G:G', 3.33)
        self.worksheet.set_column('H:H', 14.6)
        self.worksheet.set_column('I:I', 12)
        self.worksheet.set_column('J:J', 42)

        self.worksheet.set_column('K:K', 6.2)
        self.worksheet.set_column('L:L', 6.2)
        self.worksheet.set_column('M:M', 6.2)
        self.worksheet.set_column('N:N', 6.2)
        self.worksheet.set_column('O:O', 9)

        self.worksheet.set_column('P:P', 0.3, format_border) 

        self.worksheet.set_column('Q:Q', 12.5)        
        self.worksheet.set_column('R:R', 7)
        self.worksheet.set_column('S:S', 7.2)
        self.worksheet.set_column('T:T', 9.2)

        self.worksheet.autofilter('A1:T1600')
        self.worksheet.set_row(0, 58, format_header_grind)