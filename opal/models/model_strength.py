"""Model class for team strength model fitting and prediction. This is a proxy for predicting
a match outcome."""

import pandas as pd
import numpy as np
from model import Model


class TeamStrength(Model):
    def __init__(self, bugs_model: str):
        self.bugs = bugs_model

    def fit(self):
        pass

    def predict(self):
        pass
