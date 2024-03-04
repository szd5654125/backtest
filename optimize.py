import numpy as np
from datetime import datetime
import os
import concurrent.futures
import pandas as pd
from diamond_strategy import Diamond
from trade import backtesting

def single_combination(source, length, dev, close, commission, initial_cash):
    r_line = Diamond(source, length, dev, close)
    cash, position, trade_count, max_drawdown = backtesting(r_line, commission, initial_cash, close)
    final_cash = cash.iloc[-1]
    return length, dev, final_cash, r_line, cash, position, trade_count, max_drawdown


def optimize_parameters(source, commission, initial_cash, length_range, dev_range, close):
    # store every combination
    results = []
    # Initialization
    max_cash = -float('inf')
    best_r_line, best_cash, best_position = None, None, None
    # all combination
    total_combinations = ((length_range[1] - length_range[0]) / length_range[2] + 1) * ((dev_range[1] - dev_range[0]) / dev_range[2] + 1)
    # done
    completed_combinations = 0

    # through all combinations of parameters
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for length in range(length_range[0], length_range[1] + 1, length_range[2]):
            for dev in np.arange(dev_range[0], dev_range[1] + dev_range[2], dev_range[2]):
                futures.append(executor.submit(single_combination, source, length, dev, close, commission, initial_cash))

        for future in concurrent.futures.as_completed(futures):
            completed_combinations += 1
            progress = (completed_combinations / total_combinations) * 100  # 计算完成的百分比
            # print finished percent
            print(f"Progress: {progress:.2f}% completed")
            length, dev, final_cash, r_line, cash, position, trade_count, max_drawdown = future.result()
            results.append((length, dev, final_cash, trade_count, max_drawdown))
            if final_cash > max_cash:
                max_cash = final_cash
                best_r_line, best_cash, best_position = r_line, cash, position

    results_df = pd.DataFrame(results, columns=['length', 'dev', 'final_cash', 'trade_count', 'max_drawdown'])

    current_time = datetime.now().strftime('%Y%m%d%H%M')

    # make sure optimize_result folder exist
    os.makedirs('result', exist_ok=True)

    file_path = os.path.join('result', f'{current_time}_optimize.csv')

    results_df.to_csv(file_path, index=False)
    return best_r_line, best_cash, best_position







