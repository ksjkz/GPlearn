
import random

operators = {
    # Element-wise Operators
    'add': 20,
    'sub': 20,
    'mul': 30,
    'div': 30,
    'square':3,
    'sqrt': 3,
    'log': 2,
    'abs': 3,
    'neg': 2,
    'inv': 2,
    'max': 2,
    'min': 2,
    
    # Time Series Operators
    #ts函数 第一个为列,第二个为period 如 ts_sum(ADJ_D_CLOSE, 10)
    'ts_pct_change': 10,  #计算涨跌幅,pd.pct_change 遇到缺失值不填充,第二个参数为1就有意义
    'ts_sum': 6, #正常有关rolling的第二个参数至少为2
    'ts_prod': 1,
    'ts_covariance': 1,    #ts_covariance(ADJ_D_CLOSE,ADJ_D_OPEN, 10)
    'ts_corr':1,
    'ts_std': 3,
    'ts_mean': 6,
    'ts_timeweighted_mean': 3,
    'ts_rank': 6,
    'ts_max': 2,
    'ts_min': 2,
    'ts_median':2,
    'ts_argmax': 1,
    'ts_argmin': 1,
    'ts_skew': 1, #计算偏度 至少要rolling 3才有意义
    'ts_kurt': 1, #计算峰度 至少要rolling 3才有意义
    
}

# 定义运算符的输入输出规则
operator_rules = {
    'add': ('column', 'column'),  # add(a, b)
    'sub': ('column', 'column'),  # sub(a, b)
    'mul': ('column', 'column'),  # mul(a, b)
    'div': ('column', 'column'),  # div(a, b)
    
    'square': ('column',),  # square(a)
    'sqrt': ('column',),  # sqrt(a)
    'log': ('column',),  # log(a)
    'abs': ('column',),  # abs(a)
    'neg': ('column',),  # neg(a)
    'inv': ('column',),  # inv(a)
    'max': ('column', 'column'),  # max(a, b)
    'min': ('column', 'column'),  # min(a, b)
    

    # Time Series Operators (ts_ functions)
    'ts_pct_change': ('column', 'period'),  # ts_pct_change(a, 1)
    'ts_sum': ('column', 'period'),  # ts_sum(a, 10)
    'ts_prod': ('column', 'period'),  # ts_prod(a, 10)
    'ts_covariance': ('column', 'column', 'period'),  # ts_covariance(a, b, 10)
    'ts_corr': ('column', 'column', 'period'),  # ts_corr(a, b, 10)
    'ts_std': ('column', 'period'),  # ts_std(a, 10)
    'ts_mean': ('column', 'period'),  # ts_mean(a, 10)
    'ts_timeweighted_mean': ('column', 'period'),  # ts_timeweighted_mean(a, 10)
    'ts_rank': ('column', 'period'),  # ts_rank(a, 10)
    'ts_max': ('column', 'period'),  # ts_max(a, 10)
    'ts_min': ('column', 'period'),  # ts_min(a, 10)
    'ts_median': ('column', 'period'),  # ts_median(a, 10)
    'ts_argmax': ('column', 'period'),  # ts_argmax(a, 10)
    'ts_argmin': ('column', 'period'),  # ts_argmin(a, 10)
    'ts_skew': ('column', 'period'),  # ts_skew(a, 3)
    'ts_kurt': ('column', 'period')  # ts_kurt(a, 3)
}

columns={
    'open':20, 
    'high':20, 
    'low':20, 
    'close':20, 
    'volume':30, 
    'quote_asset_volume':10,
    'number_of_trades':10,
    'taker_buy_base_asset_volume':10,
    'taker_buy_quote_asset_volume':10,
    'high_change':5,
    'low_change':5,
    'close_change':5,  
    'volume_change':5,     
    'quote_asset_vol_change':5,
    'number_of_trades_change':5,
    'taker_buy_base_asset_vol_change':5,
    'taker_buy_q_asset_vol_change':5,
    'open_change':5,
   
}

period=[2,3,4,5,7,12,26,52,100]


# 随机选择一个运算符
def random_operator():
    keys = list(operators.keys())  # 获取所有的运算符
    weights = list(operators.values())  # 获取对应的权重
    # random.choices() 根据权重随机选择一个键
    return random.choices(keys, weights=weights, k=1)[0]
   

# 随机选择一个列名（column）
def random_column():
    keys = list(columns.keys())  # 获取所有的列名
    weights = list(columns.values())  # 获取对应的权重
    # random.choices() 根据权重随机选择一个键
    return random.choices(keys, weights=weights, k=1)[0]

# 生成随机数值 (num)
def random_period():
    return random.choice(period)

# 根据 expected_type 生成公式
def generate_formula(depth=3, expected_type='column'):
    # 当递归深度为0时，返回一个列名或者数值（根据 expected_type）
    if expected_type=='period':
        return random_period()  # 返回数值
    if depth == 0:
      
        return random_column()  # 返回列名
      

    # 选择一个运算符
    arity = random_operator()
    arity_num = len(operator_rules[arity])

    # 单目运算符
    if arity_num == 1:
        # 单目运算符总是返回 column 类型
        return f"{arity}({generate_formula(depth-1, 'column')})"

    # 双目运算符，根据规则生成
    elif arity_num == 2:
        # 获取运算符的输入类型规则
        left_type, right_type = operator_rules[arity]

        # 左侧输入，根据规则生成 column 或 num
        left = generate_formula(depth-1, left_type)

        # 右侧输入，根据规则生成 column 或 num
        right = generate_formula(depth-1, right_type)

        return f"{arity}({left}, {right})"
    elif arity_num == 3:
        # 获取运算符的输入类型规则
        left_type, mid_type, right_type = operator_rules[arity]

        # 左侧输入，根据规则生成 column 或 num
        left = generate_formula(depth-1, left_type)

        # 中间输入，根据规则生成 column 或 num
        mid = generate_formula(depth-1, mid_type)

        # 右侧输入，根据规则生成 column 或 num
        right = generate_formula(depth-1, right_type)

        return f"{arity}({left}, {mid}, {right})"

# 生成自定义的字符公式
def custom_formula(depth=3):
    return generate_formula(depth=depth, expected_type='column')



def generate(low=1, high=5,num=10000):
    data = []
    def weighted_random_depth(low, high):
    # 生成从 low 到 high 的候选值列表
         depths = list(range(low, high ))
         # 为每个候选值分配权重，权重为 10 的指数幂
         weights = [2** d for d in depths]
         return random.choices(depths, weights=weights, k=1)[0]
    for _ in range(num):
        formula = custom_formula(depth=weighted_random_depth(low, high))
        data.append(formula)
    return data