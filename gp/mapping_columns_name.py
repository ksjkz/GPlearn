
"""
这个库本质就是个re映射库,用来统一公式和df的列名
"""
import re


mapping = {

    r'open_change': 'ts_pct_change(open,1)',
    r'high_change': 'ts_pct_change(high,1)',
    r'low_change': 'ts_pct_change(low,1)',
    r'close_change': 'ts_pct_change(close,1)',
    r'volume_change': 'ts_pct_change(volume,1)',
    r'quote_asset_vol_change': 'ts_pct_change(quote_asset_volume,1)',
    r'number_of_trades_change': 'ts_pct_change(number_of_trades,1)',
    r'taker_buy_base_asset_vol_change': 'ts_pct_change(taker_buy_base_asset_volume,1)',
    r'taker_buy_q_asset_vol_change': 'ts_pct_change(taker_buy_quote_asset_volume,1)',
    
    
    
}


def trans_(input:str|list[str],mapping_dict:dict=mapping)->str|list[str]:
     '''
     这个函数根据mapping_dict通过正则表达式替换公式统一公式和df的列名
     输入list[str]或者str
     '''
     if isinstance(input, list):
            a=[]
            for i in input:
                   a.append(trans_(i,mapping_dict))
            return a
    
     elif isinstance(input, str):
        for old, new in mapping_dict.items():
              input = re.sub(old, new, input)
        return  input
     else:
       raise TypeError("变量必须是 list[str] 或者 str")
     




       
    
             

    