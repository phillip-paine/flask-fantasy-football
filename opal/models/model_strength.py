"""Model class for team strength model fitting and prediction. This is a proxy for predicting
a match outcome."""

import pandas as pd
import numpy as np

from model import Model
from opal.data_methods.data_manager import TeamStrengthDataModel
import pyjags as pj
from opal.constants import MODEL_COLUMN_TUPLE, FIXTURE_PARAMETERS
from opal.Run.run_arguments import RunArguments
from typing import Dict, Any
import arviz as az


class TeamStrength(Model):
    def __init__(self, data_model: TeamStrengthDataModel,  bugs_model: str, args: RunArguments):
        self.bugs = bugs_model
        self.data_model = data_model
        self.args = args

    def create_data_dict(self) -> Dict[Any, Any]:
        data_dict = {col_name: self.data_model.fixtures[col_name].values for col_name in MODEL_COLUMN_TUPLE}
        data_dict['nteam'] = 20  # can hard-code this for premier league
        data_dict['ngames'] = self.data_model.completed_games
        return data_dict

    def fit(self) -> pj.Model:
        jags_data_dict = self.create_data_dict()
        jags_fixtures_model = pj.Model(file=self.bugs, data=jags_data_dict, adapt=self.args.adaption_iterations)
        # burn-in
        jags_fixtures_model.sample(1000, vars=[])
        return jags_fixtures_model

    def predict(self, fitted_jags_model, num_samples) -> az.from_pyjags():
        prediction_samples = fitted_jags_model.sample(num_samples, vars=FIXTURE_PARAMETERS)
        return az.from_pyjags(prediction_samples)


class JagsModelComponents:
    """Class that takes jags model predictions and returns the useful components, e.g. team strength samples etc"""
    jags_samples: az.from_pyjags()

    @property
    def get_home_advantage(self) -> float:
        return self.jags_samples

    @property
    def get_team_strength(self) -> pd.DataFrame:
        # return the att and def coef for each team
        df_team_str = self.jags_samples
        return df_team_str




