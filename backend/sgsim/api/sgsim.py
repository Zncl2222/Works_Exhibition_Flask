import time

import uc_sgsim as uc
from uc_sgsim.Cov_Model import Gaussian

from utils.utils import array_to_string_encoder


def get_cov_model(model: str) -> object:
    if model == 'Gaussian':
        return SgsimGaussian
    return SgsimGaussian


class SgsimBase:
    def __init__(self, data: dict):
        self.data = data
        self.x = range(self.data['x_size'])
        self.y = range(self.data['y_size'])

    def run_sgsim(self) -> tuple[str, float]:
        start = time.time()

        if self.data['kernel'] == 'Python':
            sgsim = uc.Simulation(
                self.x,
                self.model(1, 35, 17.32, 1),
                self.data['realizations_number'],
                self.data['randomseed'],
            )
            sgsim.compute_async(
                n_process=1,
                randomseed=self.data['randomseed'],
            )
        elif self.data['kernel'] == 'C':
            sgsim = uc.Simulation_byC(
                self.x,
                self.model(1, 35, 17.32, 1),
                self.data['realizations_number'],
                self.data['randomseed'],
            )
            sgsim.compute_by_dll(
                n_process=1,
                randomseed=self.data['randomseed'],
            )

        end = time.time()
        run_time = end - start
        data = array_to_string_encoder(sgsim.random_field)
        return data, run_time


class SgsimGaussian(SgsimBase):
    model = Gaussian