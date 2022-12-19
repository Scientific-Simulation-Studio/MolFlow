from typing import List

import numpy as np
import spu
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import roc_auc_score

import molflow as sf
from molflow.data.base import Partition
from molflow.data.mix import MixDataFrame
from molflow.data.split import train_test_split
from molflow.data.vertical import VDataFrame
from molflow.ml.linear.fl_lr_mix import FlLogisticRegressionMix
from molflow.preprocessing.scaler import StandardScaler
from molflow.security.aggregation import SecureAggregator

from tests.basecase import DeviceTestCaseBase


class TestFlLrMix(DeviceTestCaseBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.num_cpus = 64
        super().setUpClass()

        def heu_config(sk_keeper: str, evaluators: List[str]):
            return {
                'sk_keeper': {'party': sk_keeper},
                'evaluators': [{'party': evaluator} for evaluator in evaluators],
                'mode': 'PHEU',
                'he_parameters': {
                    'schema': 'paillier',
                    'key_pair': {'generate': {'bit_size': 2048}},
                },
            }

        cls.heu0 = sf.HEU(heu_config(
            'alice', ['bob', 'carol']), spu.spu_pb2.FM128)
        cls.heu1 = sf.HEU(heu_config(
            'alice', ['bob', 'davy']), spu.spu_pb2.FM128)
        cls.heu2 = sf.HEU(heu_config(
            'alice', ['bob', 'eric']), spu.spu_pb2.FM128)

        features, label = load_breast_cancer(return_X_y=True, as_frame=True)
        label = label.to_frame()
        feat_list = [
            features.iloc[:, :10],
            features.iloc[:, 10:20],
            features.iloc[:, 20:],
        ]
        x = VDataFrame(
            partitions={
                cls.alice: Partition(cls.alice(lambda: feat_list[0])()),
                cls.bob: Partition(cls.bob(lambda: feat_list[1])()),
                cls.carol: Partition(cls.carol(lambda: feat_list[2])()),
            }
        )
        x = StandardScaler().fit_transform(x)
        y = VDataFrame(
            partitions={cls.alice: Partition(cls.alice(lambda: label)())})
        x1, x = train_test_split(x, train_size=0.35, shuffle=False)
        x2, x3 = train_test_split(x, train_size=0.54, shuffle=False)
        y1, y = train_test_split(y, train_size=0.35, shuffle=False)
        y2, y3 = train_test_split(y, train_size=0.54, shuffle=False)

        # davy holds same x
        x2_davy = x2.partitions[cls.carol].data.to(cls.davy)
        del x2.partitions[cls.carol]
        x2.partitions[cls.davy] = Partition(x2_davy)

        # eric holds some x also.
        x3_eric = x3.partitions[cls.carol].data.to(cls.eric)
        del x3.partitions[cls.carol]
        x3.partitions[cls.eric] = Partition(x3_eric)

        cls.x = MixDataFrame(partitions=[x1, x2, x3])
        cls.y = MixDataFrame(partitions=[y1, y2, y3])
        cls.y_arr = label.values

    def test_model_should_ok_when_fit_dataframe(self):
        # GIVEN
        aggregator0 = SecureAggregator(
            self.alice, [self.alice, self.bob, self.carol])
        aggregator1 = SecureAggregator(
            self.alice, [self.alice, self.bob, self.davy])
        aggregator2 = SecureAggregator(
            self.alice, [self.alice, self.bob, self.eric])

        model = FlLogisticRegressionMix()

        # WHEN
        model.fit(
            self.x,
            self.y,
            epochs=3,
            batch_size=64,
            learning_rate=0.1,
            aggregators=[aggregator0, aggregator1, aggregator2],
            heus=[self.heu0, self.heu1, self.heu2],
        )

        y_pred = np.concatenate(sf.reveal(model.predict(self.x)))

        auc = roc_auc_score(self.y_arr, y_pred)
        acc = np.mean((y_pred > 0.5) == self.y_arr)

        # THEN
        auc = sf.reveal(auc)
        acc = sf.reveal(acc)
        print(f'auc={auc}, acc={acc}')

        self.assertGreater(auc, 0.98)
        self.assertGreater(acc, 0.93)
