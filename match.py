class Match:
    def __init__(self,
                 country: str = '',
                 championship: str = '',
                 command_first_name: str = '',
                 command_second_name: str = '',
                 value_1_col: str = '',
                 value_2_col: str = '',
                 match_total_first_team_1p5_value: str = '',
                 match_total_second_team_1p5_value: str = '',
                 goals_dict: dict = {},
                 date: str = '',
                 ):
        self.country: str = country
        self.championship: str = championship
        self.command_first_name: str = command_first_name
        self.command_second_name: str = command_second_name
        self.value_1_col: str = value_1_col
        self.value_2_col: str = value_2_col
        self.match_total_first_team_1p5_value: str = match_total_first_team_1p5_value
        self.match_total_second_team_1p5_value: str = match_total_second_team_1p5_value
        self.goals_dict: dict = goals_dict
        self.date: str = date
