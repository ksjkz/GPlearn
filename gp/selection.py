import random

def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    pick = random.uniform(0, total_fitness)    #生成一个0到total_fitness之间的随机数
    current = 0
    for i, individual in enumerate(population):
        current += fitness_scores[i]
        if current > pick:
            return individual
        


def tournament_selection(population:list, fitness_scores:list, num_to_select:int, tournament_size:int=3):

    selected_individuals = []
    for _ in range(num_to_select):
        # 随机选择tournament_size个个体
        tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
        # 选择适应度最高的个体
        winner = max(tournament, key=lambda x: x[1])[0]
        selected_individuals.append(winner)
    
    return selected_individuals

# 示例使用
# population = ['A', 'B', 'C', 'D']
# fitness_scores = [10, 30, 40, 20]  # 各个体的适应度值
# num_to_select = 4  # 保持人口基数不变
# selected_individuals = tournament_selection(population, fitness_scores, num_to_select, tournament_size=2)
# print(f"Selected individuals: {selected_individuals}")


def reserve_top_n_individuals(population:list, fitness_scores:list, num_to_reserve:int)->list:
    '''
    保留最高的几个个体

    '''
    sorted_individuals = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
    return [individual[0] for individual in sorted_individuals[:num_to_reserve]]