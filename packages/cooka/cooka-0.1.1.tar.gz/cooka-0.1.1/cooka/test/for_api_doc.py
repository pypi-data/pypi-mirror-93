# -*- encoding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from hypergbm.hyper_gbm import HyperGBM
from hypergbm.search_space import search_space_general
from hypernets.core.searcher import OptimizeDirection
from hypernets.experiment.general import GeneralExperiment
from hypernets.searchers.mcts_searcher import MCTSSearcher
df = pd.read_csv("./iris.csv")  # 读取数据
X_train, X_test = train_test_split(df, test_size=0.1, random_state=42, shuffle=True)  # 拆分数据
y_train = X_train.pop('Species')
y_test = X_test.pop('Species')
rs = MCTSSearcher(search_space_general, max_node_space=10,
                  optimize_direction=OptimizeDirection.Maximize)  # 使用蒙特卡洛树算法作为搜索器
hk = HyperGBM(rs, task="classification", reward_metric="accuracy")
experiment = GeneralExperiment(hk, X_train, y_train, X_eval=X_test, y_eval=y_test)
estimator = experiment.run(use_cache=True, max_trials=10)