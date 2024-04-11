import datetime
import pygal

def parse_date_string(date_str):
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date
    except ValueError:
        return None

def is_date_in_range(date_str, start, end):
    date = parse_date_string(date_str)
    return start <= date <= end

def filter_json_data(json_data, start_date, end_date):
    filtered_data = {}
    time_series_keys = [key for key in json_data.keys() if "Time Series" in key]
    if time_series_keys:
        time_series_key = time_series_keys[0]
        for date_str, data in json_data[time_series_key].items():
            if is_date_in_range(date_str, start_date, end_date):
                filtered_data[date_str] = data

        filtered_data_list = list(filtered_data.items())
        try:
            sorted_data_list = sorted(filtered_data_list, key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d"))
        except:
            sorted_data_list = filtered_data_list
        sorted_filtered_data = dict(sorted_data_list)
        return sorted_filtered_data

def generate_chart(filtered_data, chart_type, stock_symbol, start_date, end_date):
    dates = list(filtered_data.keys())
    open_prices = [float(data['1. open']) for data in filtered_data.values()]
    high_prices = [float(data['2. high']) for data in filtered_data.values()]
    low_prices = [float(data['3. low']) for data in filtered_data.values()]
    close_prices = [float(data['4. close']) for data in filtered_data.values()]

    if chart_type == '1':
        chart = pygal.Bar(x_label_rotation=45)
    else:
        chart = pygal.Line(x_label_rotation=45)

    chart.title = f'Stock Data for {stock_symbol.upper()}: {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
    chart.x_labels = dates
    chart.add('Open', open_prices)
    chart.add('High', high_prices)
    chart.add('Low', low_prices)
    chart.add('Close', close_prices)

    return chart