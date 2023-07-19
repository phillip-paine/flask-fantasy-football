"""File to handle the data manipulation of data sourced for this project"""
import pandas as pd
from dataclasses import dataclass
from typing import Dict


class TeamData:
    def __init__(self, teams_data: Dict[str, pd.DataFrame]):
        self.team_data_dict = teams_data
        self.seasons = teams_data.keys()

        def create_teams_data(data_dict) -> pd.DataFrame:
            df_combined = pd.DataFrame()
            for s_, df_ in data_dict:
                df_['season'] = s_
                if df_combined.empty:
                    df_combined = df_
                else:
                    df_combined = pd.concat([df_combined, df_])

            return df_combined

        self.df = create_teams_data(teams_data)

    @property
    def team_index(self):
        df_team_index = self.df.sort_values(by=['name'], ascending=True).drop_duplicates().reset_index()
        return df_team_index

    @property
    def fetch_seasons(self):
        return self.seasons

    def merge_coefficients(self, df_team_coefs):
        ti = self.team_index()
        # This needs to be done before passing to here
        # df_coef = pd.DataFrame({'team_index': ti, 'att_coef': att_coef, 'def_coef': def_coef})
        return self.df.merge(df_team_coefs, on=['team_index'])


@dataclass
class TeamStrengthDataModel:
    fixtures: pd.DataFrame
    teamsIndex: TeamData  # FIXME: might need to replace with TeamData class object
    season: str

    @property
    def fetch_season(self):
        return self.season

    @property
    def game_week(self):
        return self.fixtures['event'].max()

    @property
    def home_goals_series(self):
        return self.fixtures.team_h_score

    @property
    def away_goals_series(self):
        return self.fixtures.team_a_score

    @property
    def home_team_index_series(self):
        return self.fixtures['team_h']

    @property
    def away_team_index_series(self):
        return self.fixtures['team_a']

    def add_fixture_coefficients(self):
        return self.fixtures

    def add_fixture_dataframe(self, ):
        return


if __name__ == '__main__':
    pass
