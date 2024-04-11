from flask import Flask, render_template, request
from API_Functions import api_call
from Graphing_functions import filter_json_data, generate_chart, parse_date_string
import csv

app = Flask(__name__)

def get_stock_symbols():
    with open('stocks.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return [row[0] for row in reader]

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_symbols = get_stock_symbols()
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        chart_type = request.form['chart_type']
        time_series_function = request.form['time_series_function']
        start_date = parse_date_string(request.form['start_date'])
        end_date = parse_date_string(request.form['end_date'])
        
        json_data = api_call(stock_symbol, time_series_function, start_date)
        if json_data:
            filtered_data = filter_json_data(json_data, start_date, end_date)
            if filtered_data:
                chart = generate_chart(filtered_data, chart_type, stock_symbol, start_date, end_date)
                chart.render_to_file('static/chart.svg')
                return render_template('index.html', chart=True, stock_symbols=stock_symbols)
            else:
                return render_template('index.html', error='No data found within the specified date range.', stock_symbols=stock_symbols)
        else:
            return render_template('index.html', error='Error retrieving data from the API.', stock_symbols=stock_symbols)
    
    return render_template('index.html', stock_symbols=stock_symbols)

if __name__ == '__main__':
    app.run(debug=True)