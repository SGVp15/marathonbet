import pickle

from config import matches_pickle


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
        self.win_number = 1

    def get_match_for_excel(self):
        match_list = []

        # self.value_1_col
        # self.value_2_col
        # self.match_total_first_team_1p5_value
        # self.match_total_second_team_1p5_value

        match_list.append([
            '', f'{self.country} {self.championship}',
            self.command_first_name,
            self.command_second_name,
            self.value_1_col,
            f'win_{self.win_number}',
            self.date]
        )

        match_list.append([
            '', f'{self.country} {self.championship}',
            self.command_second_name,
            self.command_first_name,
            self.value_2_col,
            f'win_{self.win_number}',
            self.date]
        )

        match_list.append([
            '', f'{self.country} {self.championship}',
            self.command_first_name,
            self.command_second_name,
            self.match_total_first_team_1p5_value,
            'ИТБ',
            self.date]
        )

        match_list.append([
            '', f'{self.country} {self.championship}',
            self.command_second_name,
            self.command_first_name,
            self.match_total_second_team_1p5_value,
            'ИТБ',
            self.date]
        )
        goal_teams = list(self.goals_dict.keys())
        goal = []
        for goal_team in goal_teams:
            goal.append(self.goals_dict.get(goal_team))
        reverse_goal_teams = goal_teams[::-1]

        for i in range(len(goal_teams)):
            match_list.append([
                '', f'{self.country} {self.championship}',
                goal_teams[i],
                reverse_goal_teams[i],
                goal[i],
                'клиншит',
                self.date]
            )

        return match_list


def set_match_win():
    with open(matches_pickle, 'rb') as handle:
        matches = pickle.load(handle)

    for j in range(len(matches)):
        match: Match = matches[j]
        for i in range(j + 1, len(matches)):
            match_2: Match = matches[i]
            if match.country == match_2.country:
                if match.championship == match_2.championship:
                    if (match.command_first_name == match_2.command_first_name
                            or match.command_second_name == match_2.command_second_name):
                        match_2.win_number += 1

    with open(matches_pickle, 'wb') as handle:
        pickle.dump(matches, handle, protocol=pickle.HIGHEST_PROTOCOL)
