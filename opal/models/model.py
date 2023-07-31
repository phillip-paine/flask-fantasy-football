"""Model base class"""

from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self, fitted_jags_model, num_samples):
        pass
