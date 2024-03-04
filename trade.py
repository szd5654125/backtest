import numpy as np
import pandas as pd
from operations import marketpreis_buy, marketpreis_sell




def backtesting(indicator,commission, initial_cash, close):
    cash = pd.Series(initial_cash, index=close.index, dtype=float)
    position = pd.Series(np.zeros_like(close), index=close.index)
    buy_price = 0
    trade_count = 0  # 初始化交易次数
    max_cash = initial_cash  # 初始化最大现金余额
    max_drawdown = 0  # 初始化最大回撤金额

    # 遍历每个时间点
    for i in range(1, len(close)):
        # 更新前一次的现金余额到当前，如果前一天已经更新则保持不变
        cash[i] = cash[i - 1]
        # 如果当前持有仓位，则将 position 设置为 1
        if position[i - 1] == 1:
            position[i] = 1

        # 检查买入条件：close向上穿过r_line
        if indicator[i - 1] > close[i - 1] and indicator[i] < close[i]:
            if position[i] == 0:  # 确保当前没有持仓
                # 关于position: 执行操作同时修改position
                cash[i], position[i], buy_price = marketpreis_buy(close[i], commission, initial_cash, cash[i-1])
                trade_count += 1  # 交易次数加一

        # 检查卖出条件：close向下穿过r_line
        elif indicator[i - 1] < close[i - 1] and indicator[i] > close[i]:
            if position[i] == 1:  # 确保当前有持仓
                # 关于position: 执行操作同时修改position
                cash[i], position[i] = marketpreis_sell(buy_price, close[i], commission, initial_cash, cash[i-1])
                buy_price = 0  # 重置买入价格
                max_cash = max(max_cash, cash[i])  # 更新最高现金余额
                max_drawdown = max(max_drawdown, max_cash - cash[i])  # 更新最大回撤金额
                trade_count += 1  # 交易次数加一

        # 循环结束后，检查是否有持仓需要卖出
    if position.iloc[-1] == 1:
        cash.iloc[-1], position.iloc[-1] = marketpreis_sell(buy_price, close.iloc[-1], commission, initial_cash, cash.iloc[-1])
        max_cash = max(max_cash, cash.iloc[-1])
        max_drawdown = max(max_drawdown, max_cash - cash.iloc[-1])
        trade_count += 1  # 交易次数加一
    cash.name = 'cash'
    position.name = 'position'
    # 返回现金数列和持仓数列
    return cash, position, trade_count, max_drawdown



