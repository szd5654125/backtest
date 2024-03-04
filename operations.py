



def marketpreis_buy(close, commission, initial_cash, cash):
        cash -= initial_cash * commission
        position_new = 1
        buy_price = close
        return cash, position_new, buy_price

def marketpreis_sell(buy_prise, close, commission, initial_cash, cash):
        cash += initial_cash * (close - buy_prise) / buy_prise - initial_cash * commission
        position_new = 0
        return cash, position_new