import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

def evaluate_factor_with_score(df, factor_col, future_return_col, quantiles=5, weights=None):
    """
    评估因子在比特币历史数据上的有效性，并生成一个综合评分。
    
    参数:
    df: pd.DataFrame, 包含比特币价格、因子值、未来收益率等信息的数据框。
    factor_col: str, 因子值列名。
    future_return_col: str, 未来收益率列名。
    quantiles: int, 分组数量，默认将因子分为5组 (五分位数)。
    weights: dict, 每个指标的权重，默认为等权重。
    
    返回:
    score: float, 综合评价得分，用于遗传规划或模型优化。
    details: dict, 包含每个指标的详细计算结果。
    """
    
    df= df[[factor_col, future_return_col]].replace([np.inf, -np.inf], np.nan).dropna().copy()
    details = {}
    
    # 1. 相关性分析：因子值与未来收益率的相关性
    try:
          corr, p_value = stats.pearsonr(df[factor_col], df[future_return_col])
          details['correlation'] = corr
          details['correlation_p_value'] = p_value
    except:
          details['correlation'] = 0
          details['correlation_p_value'] = 0

    # 2. 分组收益分析：按因子值进行分组，查看每组的未来平均收益率
    try:
            df['factor_quantile'] = pd.qcut(df[factor_col], quantiles, labels=False)
            group_returns = df.groupby('factor_quantile')[future_return_col].mean()
            details['group_returns'] = group_returns
            # 计算分组最大最小收益差
            max_min_diff = group_returns.max() - group_returns.min()
            details['max_min_group_return_diff'] = max_min_diff
    except:
            details['group_returns'] = 0
            details['max_min_group_return_diff'] = 0

    

    # 3. 信息比率：收益差与其标准差的比值
    mean_return = df[future_return_col].mean()
    factor_return = df[factor_col] * mean_return
    residuals = df[future_return_col] - factor_return
    ir = np.mean(residuals) / np.std(residuals)
    details['information_ratio'] = ir

    # 4. 回归分析：因子值对未来收益率的线性回归
    try:
             X = sm.add_constant(df[factor_col])
             y = df[future_return_col]
             model = sm.OLS(y, X).fit()
             details['regression_coef'] = model.params[factor_col]  # 因子回归系数
             details['regression_p_value'] = model.pvalues[factor_col]  # 因子回归的p值
    except:
             details['regression_coef'] = 0
             details['regression_p_value'] = 0

    # 赋予权重：如果没有指定权重，则使用默认的等权重
    if weights is None:
        weights = {
            'correlation': 0.25,
            'max_min_group_return_diff': 0.25,
            'information_ratio': 0.25,
            'regression_coef': 0.25
        }

    # 5. 标准化并计算最终评分
    # 将每个指标归一化并进行加权求和
    corr_score = (details['correlation'] + 1) / 2  # 相关性范围 [-1, 1] 归一化到 [0, 1]
    group_return_score = details['max_min_group_return_diff']  # 直接使用分组收益差
    ir_score = (details['information_ratio'] + 1) / 2  # 信息比率通常较小，调整到 [0, 1]
    reg_coef_score = max(0, details['regression_coef'])  # 只考虑正向的回归系数

    # 综合得分 = 各指标的加权和
    score = (abs(weights['correlation']) * corr_score +
             abs(weights['max_min_group_return_diff'] )* group_return_score +
             abs(weights['information_ratio']) * ir_score +
             abs(weights['regression_coef'] )* reg_coef_score)

    return score, details


