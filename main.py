import numpy as np 
import pandas as pd
from numpy.random import normal, seed
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from matplotlib import pyplot
import seaborn as sns

from flask import Flask, request, jsonify, render_template
import pickle
from stocks import Stocks

app = Flask(__name__)
#model = pickle.load(open('C:\\Users\\ishah3\\Downloads\\Deployment-flask-master-20240725T045105Z-001\\Deployment-flask-master\\myproject\\test.pkl', 'rb'))
df = pd.read_csv("C:\\Users\\ishah3\\Downloads\\Deployment-flask-master-20240725T045105Z-001\\Deployment-flask-master\\myproject\\merged-csv-files.csv")

df.fillna(value = 0.0, inplace = True)
df['Date'] = pd.to_datetime(df['Date'])

@app.route('/')
def home():
  stocks=['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO',
'BAJAJFINSV', 'BAJFINANCE', 'BHARTIARTL', 'BPCL', 'BRITANNIA',
'CIPLA', 'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM',
'HCLTECH', 'HDFC', 'HDFCBANK', 'HEROMOTOCO', 'HINDALCO',
'HINDUNILVR', 'ICICIBANK', 'INDUSINDBK', 'INFY', 'IOC', 'ITC',
'JSWSTEEL', 'KOTAKBANK', 'LT', 'MARUTI', 'M&M', 'NESTLEIND',
'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBIN', 'SHREECEM',
'SUNPHARMA', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN',
'ULTRACEMCO', 'UPL', 'VEDL', 'WIPRO', 'ZEEL']
  
  return render_template('homepg.html',stocks=stocks)
  #m1=Stocks(inputdf=df,name="TCS")
  #print(m1.get_summary())



@app.route('/handle_stock_selection', methods=['POST'])

def handle_stock_selection():
    selected_stock = request.form.get('stockSelect')
    print(request.data)
    if selected_stock:

        
        m1=Stocks(df=df,name=selected_stock)
        name=m1.name
        summary=m1.get_summary()
        live=m1.live_price()
        predicted_value=m1.predictions()
        img_path=m1.generate_graph()

        stocks=['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO',
'BAJAJFINSV', 'BAJFINANCE', 'BHARTIARTL', 'BPCL', 'BRITANNIA',
'CIPLA', 'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM',
'HCLTECH', 'HDFC', 'HDFCBANK', 'HEROMOTOCO', 'HINDALCO',
'HINDUNILVR', 'ICICIBANK', 'INDUSINDBK', 'INFY', 'IOC', 'ITC',
'JSWSTEEL', 'KOTAKBANK', 'LT', 'MARUTI', 'M&M', 'NESTLEIND',
'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBIN', 'SHREECEM',
'SUNPHARMA', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN',
'ULTRACEMCO', 'UPL', 'VEDL', 'WIPRO', 'ZEEL']
  
        return render_template('display.html',name=name,summary=summary,live=live,predicted_value=predicted_value,img_path=img_path,stocks=stocks)
      
    
    return 'No stock selected'




if __name__ == "__main__":
    app.run(debug=True)