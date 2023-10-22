from __future__ import annotations

import time

import uc_sgsim as uc
from uc_sgsim.cov_model import Exponential, Gaussian, Spherical

from utils.utils import array_to_string_encoder


class Sgsim:
    x: int = 150
    y: int = 0
    realizations_number: int = 10
    cov_model: str = 'Gaussian'
    k_range: float = 17.32
    k_sill: float = 1
    k_nugget: float = 0
    bw_l: int = 35
    bw_s: int = 1
    kernel: str = 'Python'
    z_min: float = -6
    z_max: float = 6
    max_neighbor: int = 8
    randomseed: int = 12345
    cov_model_options: dict = {
        'Gaussian': Gaussian,
        'Spherical': Spherical,
        'Exponential': Exponential,
    }
    kernel_options: dict = {
        'Python': uc.UCSgsim,
        'C': uc.UCSgsimDLL,
    }

    def __init__(self, data: dict[str, str | int | float]):
        self.x = data['x_size']
        self.y = data['y_size']
        self.realizations_number = data['realizations_number']
        self.kernel = data['kernel']
        self.cov_model = self.cov_model_options.get(data['cov_model'], Gaussian)
        self.bw_l = int(data['bandwidth'])
        self.bw_s = int(data['bandwidth_step'])
        self.randomseed = data['randomseed']
        self.k_range = data['krige_range']
        self.k_sill = data['krige_sill']
        self._validate_and_set_default()

    def _validate_and_set_default(self):
        if self.kernel not in ['Python', 'C']:
            self.kernel = 'Python'

    def run_sgsim(self) -> tuple[str, float]:
        start = time.time()
        sgsim = self.kernel_options.get(self.kernel, uc.UCSgsim)

        sgsim = sgsim(
            self.x,
            self.realizations_number,
            self.cov_model(self.bw_l, self.bw_s, self.k_range, self.k_sill),
        )

        sgsim.compute(
            n_process=1,
            randomseed=int(self.randomseed),
        )

        end = time.time()
        run_time = end - start
        data = array_to_string_encoder(sgsim.random_field)
        return data, run_time
