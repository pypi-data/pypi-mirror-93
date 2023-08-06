from hypergbm.search_space import search_space_general  # 默认搜索空间
from hypernets.searchers.mcts_searcher import MCTSSearcher
from hypernets.core.searcher import OptimizeDirection
rs = MCTSSearcher(search_space_general, max_node_space=10,
                  optimize_direction=OptimizeDirection.Maximize)
