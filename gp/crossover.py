from gp.formulate_coding_AST import ExpressionTree,Node
import random
'''
用于crossover的公式树继承于formulate_coding_AST的ExpressionTree,Node
'''


def select_random_subtree(node:Node)->Node:
    """
    随机选择一个子树。通过递归遍历树，随机返回某个节点。
    """
    if not node.children:
        if not isinstance(node.value, int):  #不能替换叶节点上的int
           return node.deepcopy()  # 如果没有子节点，返回自身
        else:
            return None
    # 随机决定是否选择当前节点或递归到子节点
    if random.random() < 0.1 :
        return node.deepcopy()
    else:
        # 在子节点中随机选择一个进行递归
        # 随机选择一个子节点，并确保该子节点不是叶节点
        while True:
            selected_child = random.choice(node.children)
            result = select_random_subtree(selected_child)
            if result is not None:
                return result  # 递归找到了非叶节点，返回它
    

def replace_subtree(node:Node, target_subtree:Node, new_subtree:Node)->Node:
    """
    替换指定的子树。递归遍历节点并替换与 target_subtree 匹配的子树。
    
    参数：
    - node: 当前节点（递归的起点）
    - target_subtree: 要替换的子树（即我们要找到的子树）
    - new_subtree: 用来替换的子树（替换掉 target_subtree 的新子树）

    逻辑：
    - 递归遍历树，找到 `target_subtree`，并将它替换为 `new_subtree`
    """
    # 1. 基本情况：如果当前节点就是我们要替换的那个子树 `target_subtree`
    if node == target_subtree:
        return new_subtree.deepcopy()  # 找到目标子树，返回新的子树，替换掉目标子树
    
    # 2. 如果当前节点不是目标子树，递归处理其子节点
    new_node = Node(node.value) #创建新的防止修改老的节点
    # 递归地处理子节点
    new_node.children = [replace_subtree(child, target_subtree, new_subtree) for child in node.children]
    return new_node.deepcopy()  



def crossover_node(node1:Node, node2:Node):
    """
    对两个表达式树进行交叉操作。随机选择两个子树并交换它们。
    node1,node2都是根节点

    """
    # 从两个树中随机选择子树
    subtree1 = select_random_subtree(node1)
    subtree2 = select_random_subtree(node2)
    # 输出选择的子树值（可选，用于调试）
    # print(f"Selected subtree from tree1: {subtree1.value}")
    # print(f"Selected subtree from tree2: {subtree2.value}")
    # 交换子树
    new_tree1_root = replace_subtree(node1, subtree1, subtree2)
    new_tree2_root = replace_subtree(node2, subtree2, subtree1)
    # 返回新的树
    return new_tree1_root, new_tree2_root


def crossover(tree1:ExpressionTree, tree2:ExpressionTree):
    tree1_root, tree2_root = crossover_node(tree1.root, tree2.root)
    tree1.root = tree1_root
    tree2.root = tree2_root
    return tree1, tree2

def generate_random_pairs(num:int=100000):
    # 创建 0 到 8999 的列表
    numbers = list(range(num))
    # 随机打乱这个列表
    random.shuffle(numbers)
    # 两两配对，转成 (a, b) 的元组列表
    pairs = [(numbers[i], numbers[i + 1]) for i in range(0, len(numbers), 2)]
    
    return pairs
def population_crossover(population:list[ExpressionTree]):
    '''
    population：list
    '''
    pairs = generate_random_pairs(len(population))
    new_population = []
    for pair in pairs:
        tree1, tree2 = crossover(population[pair[0]], population[pair[1]])
        new_population.append(tree1)
        new_population.append(tree2)
    return new_population

