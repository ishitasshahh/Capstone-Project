from jugaad_data.nse import NSELive
import pandas as pd
import requests
from prophet import Prophet
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Stocks:
    
    def __init__(self,name,df):
        self.name=name
        self.filter_df=df.query(f'Symbol == "{self.name}"')
        print(self.filter_df)
        self.make_model()
        print(self.name)

        #print(filter_df)
        
               


    def get_summary(self):
        # get statsitcally computed data for the stock
        summary={}
        stockmean=self.filter_df['Open'].mean().round(2)
        highmean=self.filter_df['High'].mean().round(2)
        lowmean=self.filter_df['Low'].mean()
        maxturnover=self.filter_df['Turnover'].max()
        totalvolume=self.filter_df['Volume'].sum()
        minpercentdeliverable=self.filter_df['%Deliverble'].min()
        maxpercentdeliverable=self.filter_df['%Deliverble'].max()

        summary['Stock_Mean'] = stockmean
        summary['High_Mean'] = highmean
        summary['Low_Mean'] = lowmean
        summary['Max_Turnover'] = maxturnover
        summary['Total_Volume'] = totalvolume
        summary['Min_Deliverable'] = minpercentdeliverable
        summary['Max_Deliverable'] = maxpercentdeliverable

        return summary
        
    def live_price(self):
       
        n=NSELive()
        try:
            a=n.stock_quote(self.name)['priceInfo']['lastPrice']
            #print(n.stock_quote(self.name))
        except Exception as e:
            print(e)
            a=0

        return a
    
    def make_model(self):
       
        mdf=pd.DataFrame(self.filter_df)
        mdf['Close'] = mdf['Close'].astype(float)
        mdf['Date'] = pd.to_datetime(mdf['Date'])
        mdf.sort_values('Date', inplace=True)
        mdf=mdf[['Date', 'Close']]
        mdf.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
  
        model = Prophet()
        model.fit(mdf)
        pickle.dump(model, open('prediction_model.pkl','wb'))

    def predictions(self):
        model = pickle.load(open('prediction_model.pkl','rb'))
        future = model.make_future_dataframe(periods=1)

        forecast = model.predict(future)
        predicted_close = forecast['yhat'].iloc[-1]

        return predicted_close.round(2)
    
        
    def generate_graph(self):
        tempdf=self.filter_df.tail(7)
        plt.figure(figsize=(10, 5))

        plt.plot(tempdf['Date'], tempdf['Open'], label='Date vs Open')

        plt.plot(tempdf['Date'], tempdf['Close'], label='Date vs Close')

        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title('Open and CLose vs Time')
        plt.legend()
        plt.grid(True)
        img_path = 'C:\\Users\\ishah3\\Downloads\\Deployment-flask-master-20240725T045105Z-001\\Deployment-flask-master\\myproject\\static\\images\\stock_chart.png'
        plt.savefig(img_path)
        plt.close()
        return img_path

        


            
        
        

    
    
