# Imports
import asyncio
import tkinter as tk
from tkinter import Toplevel, messagebox as msgbox
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import aiohttp
from tkinter.ttk import *
# Variables
root=tk.Tk()
options = {
    "Select a Stock": None,
    'United States': "IBM", 
    "UK - London Stock Exchange": "TSCO.LON", 
    "Canada - Toronto Stock Exchange": "SHOP.TRT", 
    "Canada - Toronto Venture Exchange": "GPV.TRV", 
    "Germany - XETRA": "MBG.DEX", 
    "India - BSE": "RELIANCE.BSE", 
    "China - Shanghai Stock Exchange": "600104.SHH", 
    "China - Shenzhen Stock Exchange": "000002.SHZ"
           }
names = list(options.keys())
value_inside = tk.StringVar(root) 
value_inside.set("Select a Stock")
data = 0
height, width = 300, 350

# Functions

def plotter(x, y, colour, xlabel, ylabel, title, file):
    plt.plot(x, y, marker="o", color=colour)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f'Plot - {file}.png', bbox_inches="tight")

async def fetch(x):
    if x==None:
        print('OPTION NOT SELECTED')
        return 1;
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://jsonplaceholder.typicode.com/todos/1") as response:
                data = await response.json()
                print(data)
                return data
        '''async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={x}&apikey=UCUN7GQUJERVREJK") as response:
                data = await response.json()
                print(data)
                return data'''
    except Exception as e:
        print("NETWORK CONNECTION ERROR")
        print(e)
        return 0;

async def valuefetch():
    print(f"{value_inside.get()}")
    submit.config(text="Fetching...", state=tk.DISABLED)
    raw = await fetch(options[value_inside.get()])
    if raw==0:
        submit.config(text="Fetch Data", state=tk.NORMAL)
        msgbox.showerror("ERROR", "INTERNET CONNECTION ERROR")
    if raw==1:
        submit.config(text="Fetch Data", state=tk.NORMAL)
        msgbox.showerror("ERROR", "PLEASE SELECT SOMETHING")
    else:
        submit.config(text="Fetch Data", state=tk.NORMAL)
        msgbox.showinfo("COMPLETED", "Stock market data has been anaylized")
        raw = raw["Time Series (Daily)"]
        print(raw)
        date, high, open, close, volume, low = [], [], [], [], [], []
        for i in raw:
            x = raw[i]
            date = list(raw.keys())
            high.append(x["2. high"])
            low.append(x["3. low"])
            open.append(x["1. open"])
            close.append(x["4. close"])
            volume.append(x["5. volume"])

        plotter(date, high, "#32a852", "Date", "High", "Changes in High", "date-high")
        plotter(date, low, "#32a852", "Date", "Low", "Changes in Low", "date-low")
        plotter(date, open, "#32a852", "Date", "Open", "Changes in High", "date-high")
        # New window
        newWindow = Toplevel(root)
        newWindow.title("Analysis")
        #newWindow.geometry("500x400")
    return None
def valuefetcher():
    asyncio.run(valuefetch())
# GUI
root.geometry(f"{width}x{height}")
root.title("Stock Market Analyzer")

question_menu = tk.OptionMenu(root, value_inside, *names) 
question_menu.grid(row=0, column=1)

submit=tk.Button(root, text="Fetch Data", command=valuefetcher)
submit.grid(row=1,column=1)

raw = {
  "Meta Data": {
    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
    "2. Symbol": "IBM",
    "3. Last Refreshed": "2024-08-22",
    "4. Output Size": "Compact",
    "5. Time Zone": "US/Eastern"
  },
  "Time Series (Daily)": {
    "2024-08-22": {
      "1. open": "197.2500",
      "2. high": "197.9200",
      "3. low": "195.5700",
      "4. close": "195.9600",
      "5. volume": "1969496"
    },
    "2024-08-21": {
      "1. open": "195.9700",
      "2. high": "197.3300",
      "3. low": "194.1150",
      "4. close": "197.2100",
      "5. volume": "2579343"
    },
    "2024-08-20": {
      "1. open": "194.5900",
      "2. high": "196.2100",
      "3. low": "193.7500",
      "4. close": "196.0300",
      "5. volume": "1790371"
    },
  }
}
raw = raw["Time Series (Daily)"]
date, high, open, close, volume, low = [], [], [], [], [], []
for i in raw:
    x = raw[i]
    date = list(raw.keys())

    high.append(x["2. high"])
    low.append(x["3. low"])
    open.append(x["1. open"])
    close.append(x["4. close"])
    volume.append(x["5. volume"])

print(date, high, open, close, volume, low)
'''
plotter(date, high, "#32a852", "Date", "High", "Changes in High", "date-high")
plotter(date, low, "#32a852", "Date", "Low", "Changes in Low", "date-low")
plotter(date, open, "#32a852", "Date", "Open", "Changes in Open", "date-open")
'''
#root.mainloop()