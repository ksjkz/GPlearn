from gp.generate import *
from gp.crossover import *
from gp.formulate_coding_AST import ExpressionTree
import copy


def mutation(tree:ExpressionTree, low=1, high=5):
    """
    对表达式树进行变异操作
    """
    # 生成随机深度
    def weighted_random_depth(low, high):
    # 生成从 low 到 high 的候选值列表
         depths = list(range(low, high ))
         # 为每个候选值分配权重，权重为 10 的指数幂
         weights = [2** d for d in depths]
         return random.choices(depths, weights=weights, k=1)[0]
    if low==high:
         formu_str=custom_formula(depth=low)
    else:
         formu_str=custom_formula(depth=weighted_random_depth(low, high))
    root_node=ExpressionTree(input=formu_str).root
    target_node=select_random_subtree(tree.root)
    tree_new=ExpressionTree(replace_subtree(node=tree.root, target_subtree=target_node, new_subtree=root_node))
    return tree_new

def population_mutation(population, mutation_rate=0.05, low=1, high=3):
    """
    随机选择列表中 10% 的元素并进行替换。

    参数:
    lst: list, 需要进行元素替换的列表。
    replacement_function: function, 用于生成替换值的函数。
    
    返回:
    替换后的列表
    """
    # 计算出 10% 要替换的元素数量，至少替换 1 个元素
    num_to_replace = max(1, int(len(population) * mutation_rate))
    
    # 随机选择要替换的元素索引
    indices_to_replace = random.sample(range(len(population)), num_to_replace)
    
    # 对选中的索引进行替换
    for idx in indices_to_replace:
        population[idx] = mutation(population[idx], low=low, high=high)

    return population

