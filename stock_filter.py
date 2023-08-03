import yfinance as yf
import pandas as pd

def filter_stocks(price_range, price_weeks, earning_weeks):
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    tickers = sp500.Symbol.to_list()
    filtered_stocks = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=f'{price_weeks}wk')
            price_range_low = hist['Close'].tail(price_weeks*5).min()
            price_range_high = hist['Close'].tail(price_weeks*5).max()
            latest_price = stock.info['regularMarketPreviousClose']
            # earning_date = stock.calendar.iloc[0]['Earnings Date']
            if latest_price <= price_range_low + (price_range / 100) * (price_range_high - price_range_low): # and earning_date <= pd.Timestamp.today() + pd.Timedelta(weeks=earning_weeks):
                filtered_stocks.append({
                    'Ticker': ticker,
                    'Company name': stock.info['longName'],
                    'Latest price': latest_price,
                    f'Price range of last {price_weeks} weeks': f'{price_range_low:.2f} - {price_range_high:.2f}',
                    #'EPS': stock.info['trailingEps'],
                    #'P/E ratio': stock.info['trailingPE']
                })
                print(f"added {ticker}: {latest_price}")
        except KeyError as e:
            # print(f'{str(e)} when processing {ticker}')
            continue
        except:
            # print(f'something wrong when processing {ticker}')
            continue
    return filtered_stocks

if __name__ == '__main__':
    price_range = 10
    price_weeks = 52
    earning_weeks = 2
    filtered_stocks = filter_stocks(price_range, price_weeks, earning_weeks)
    print(filtered_stocks)