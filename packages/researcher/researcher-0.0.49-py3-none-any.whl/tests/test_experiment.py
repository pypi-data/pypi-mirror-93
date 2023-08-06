from researcher.experiment import Experiment
import unittest
import json

import numpy as np
import researcher as rs

from tests.tools import TEST_DATA_PATH

class TestExperiment(unittest.TestCase):
    def setUp(self) -> None:
        self.mse_experiment = {
            "title": "test",
            "description": "this is the first example record",
            "experiment": "linear_reg",
            "data_name": "data/train.csv",
            "folds": 5,
            "pipeline": "noop",
            "metrics": [
                "mse"
            ],
            "x_cols": [
                "building_id"
            ],
            "y_cols": [
                "meter_reading"
            ],
            "timestamp": "2020-07-11_12:48:55",
            "hash": "28hbsb12bns8612vt26867156",
            "observations": {
                "mse": [
                    [
                        18899806900.366104
                    ],
                    [
                        65922637417.14631
                    ],
                    [
                        29483771984.313713
                    ],
                    [
                        73728779.50177501
                    ],
                    [
                        3029002638.4022694
                    ]
                ]
            }
        }

    def test_returns_correct_number_of_folds(self):
        e = Experiment(self.mse_experiment)

        self.assertEqual(e.n_folds(), 5)

        self.mse_experiment["observations"] = {
            "mse": [
                [0.877], 
                [0.877], 
                [0.877],
            ],
            "rmse": [
                [0.877, 0.99],
                [0.877, 0.99],
                [0.877, 0.99],
            ] 
        }
        e = Experiment(self.mse_experiment)
        self.assertEqual(e.n_folds(), 3)

        self.mse_experiment["observations"] = {
            "mse": [
                [0.877], 
                [0.877], 
                [0.877],
            ],
            "rmse": [
                [0.877, 0.99],
                [0.877, 0.99],
                [0.877, 0.99],
            ],
            "final_score": [0.88, 0.88],
            "final_score2": 0.88
        }
        e = Experiment(self.mse_experiment)
        self.assertEqual(e.n_folds(), 3)

    def test_returns_correct_number_of_folds_no_obs(self):
        self.mse_experiment["observations"] = {}
        e = Experiment(self.mse_experiment)

        self.assertEqual(e.n_folds(), 0)


    def test_returns_correct_number_of_folds_non_fold_obs(self):
        self.mse_experiment["observations"] = {
            "final_score": 0.877 
        }
        e = Experiment(self.mse_experiment)
        self.assertEqual(e.n_folds(), 0)

        self.mse_experiment["observations"] = {
            "final_scores": [0.877, 0.987, 0.363] 
        }
        e = Experiment(self.mse_experiment)
        self.assertEqual(e.n_folds(), 0)

    def test_records_observations_correctly(self):


        expected_observations = {
                "mse": [
                    [
                        18899806900.366104
                    ],
                    [
                        65922637417.14631
                    ],
                    [
                        29483771984.313713
                    ],
                    [
                        73728779.50177501
                    ],
                    [
                        3029002638.4022694
                    ]
                ]
            }

        e = Experiment(self.mse_experiment)

        self.assertEqual(e.observations, expected_observations)
