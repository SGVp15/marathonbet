class Match:
    def __init__(self,
                 country: str = '',
                 championship: str = '',
                 command_first_name: str = '',
                 command_second_name: str = '',
                 value_1_col: float = 0.0,
                 value_2_col: float = 0.0,
                 match_total_first_team_1p5_value: float = 0.0,
                 match_total_second_team_1p5_value: float = 0.0,
                 goals_dict: dict = {}
                 ):
        self.country: str = country
        self.championship: str = championship
        self.command_first_name: str = command_first_name
        self.command_second_name: str = command_second_name
        self.value_1_col: float = value_1_col
        self.value_2_col: float = value_2_col
        self.match_total_first_team_1p5_value: float = match_total_first_team_1p5_value
        self.match_total_second_team_1p5_value: float = match_total_second_team_1p5_value
        self.goals_dict: dict = goals_dict
