from app.home.finance.stocks_dict import stocks_dict
from app.home.finance.returns import get_optimal_interval
from app.home.finance.load_stock import load_stock

import concurrent.futures

def get_top_gainers(sector, time_frame):
    CONNECTIONS = 100

    optimal_interval = get_optimal_interval(time_frame)

    gainer_data = []

##    for t in stocks_dict[sector]:
##        gainer_data.append(load_stock(t, time_frame, optimal_interval))

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_stocks  = (executor.submit(load_stock, t['name'], t['ticker'], t['currency'], time_frame, optimal_interval) for t in stocks_dict[sector])

        for future in concurrent.futures.as_completed(future_to_stocks):
            try:
                data = future.result()

                if data:
                    gainer_data.append(data)
            except Exception as exc:
                print(str(exc))
                print('Error loading data!')

    sorted_gainers = sorted(gainer_data, key=lambda k: k['change'], reverse=True)

    return sorted_gainers
