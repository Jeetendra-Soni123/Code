# Imports
import subprocess
import asyncio
import tkinter as tk
from tkinter import messagebox as msgbox
import matplotlib.pyplot as plt
import aiohttp
import math as mt
import os
import shutil

# Variables
root=tk.Tk()
options = {
    "Select a Stock": None,
    "United States": "IBM", 
    "UK - London Stock Exchange": "TSCO.LON", 
    "Canada - Toronto Stock Exchange": "SHOP.TRT", 
    "Canada - Toronto Venture Exchange": "GPV.TRV", 
    "Germany - XETRA": "MBG.DEX", 
    "India - BSE": "RELIANCE.BSE",
    "Nifty India Financials ETF": "INDF",
    "FT India Nifty 50 EW ETF":"NFTY",
    "China - Shanghai Stock Exchange": "600104.SHH", 
    "China - Shenzhen Stock Exchange": "000002.SHZ",
    "AMEX Advance Decline Difference": "ADDA",
    "CAD Total Advancing Stocks": "ADVX",
    "AEX General - Netherlands": "AEX",
    "Amsterdam Midkap Index": "AMX",
    "All Ordinaries Index": "AORD",
    "AMEX Declining Stocks": "ASHD",
    "AMEX Advances - Declines": "ASHF",
    "AMEX Advance Decline Ratio": "ASHR",
    "AMEX Advancing Stocks": "ASHU",
    "ATX - Austria": "ATX",
    "Vanguard Small Cap Index": "VB",
    "MSCI US Smallcap Value": "VCV",
    "Vix Index": "VIX",
    "CAC 40 Index": "XAX",
    "NYSE Composite": "XBX",
    "FTSE 100 Index": "XCAX",
    "Xetra Dax": "XDAX",
           }
names = list(options.keys())
value_inside = tk.StringVar(root) 
value_inside.set("Select a Stock")
data = 0
height, width = 300, 350

# Functions
def run_script():
    subprocess.run(["python", "show_graphs.py"], check=True)


def plotter(x, y, colour, xlabel, ylabel, title, file):
    plt.rcParams["figure.figsize"] = [20, 3.5]
    plt.tick_params(labeltop=True, labelright=True)
    plt.xticks(rotation=90)
    plt.plot(x, y, marker="o", color=colour)
    plt.grid()
    plt.title(title)
    plt.xlabel(xlabel, labelpad=55)
    plt.ylabel(ylabel, labelpad=30)
    plt.ylim([mt.floor(min(y)), mt.ceil(max(y))])
    plt.savefig(f'./graphs/Plot - {file}.png', bbox_inches="tight")
    plt.clf()

async def fetch(x):
    if x==None:
        print('OPTION NOT SELECTED')
        return 1;
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={x}&outputsize=compact&apikey=UCUN7GQUJERVREJK") as response:
                data = await response.json()
                return data
    except Exception as e:
        print("NETWORK CONNECTION ERROR")
        print(e)
        return 0;

async def valuefetch():
    print(f"{value_inside.get()}")
    submit.config(text="Fetching...", state=tk.DISABLED)
    try:
        raw = await fetch(options[value_inside.get()])
        if raw==0:
            submit.config(text="Fetch Data", state=tk.NORMAL)
            msgbox.showerror("ERROR", "INTERNET CONNECTION ERROR")
            return None
        if raw==1:
            submit.config(text="Fetch Data", state=tk.NORMAL)
            msgbox.showerror("ERROR", "PLEASE SELECT SOMETHING")
            return None
        else:
            submit.config(text="Fetch Data", state=tk.NORMAL)
            raw = raw["Time Series (Daily)"]
            date, high, open, close, volume, low = [], [], [], [], [], []
            for i in raw:
                x = raw[i]
                date = list(raw.keys())
                high.append(float(x["2. high"]))
                low.append(float(x["3. low"]))
                open.append(float(x["1. open"]))
                close.append(float(x["4. close"]))
                volume.append(float(x["5. volume"]))
            msgbox.showinfo("COMPLETED", "STOCK MARKET ANALYZED\nCLICK OK TO SEE DATA")
            file_name=['date-high','date-low','date-open','date-close','date-volume']
            if os.path.exists("graphs"):
                # Delete the existing folder and its contents
                shutil.rmtree("graphs")

            # Create a new 'graphs' folder
            os.makedirs("graphs")

            plotter(date, high, "#32a852", "Date", "High", "Changes in High", file_name[0])
            plotter(date, low, "#32a852", "Date", "Low", "Changes in Low", file_name[1])
            plotter(date, open, "#32a852", "Date", "Open", "Changes in Open", file_name[2])
            plotter(date, close, "#32a852", "Date", "Close", "Changes in Close", file_name[3])
            plotter(date, volume, "#32a852", "Date", "Volume", "Changes in Volume", file_name[4])
            
            # Run show_graphs.py
            run_script()
            
    except Exception as e:
        submit.config(text="Fetch Data", state=tk.NORMAL)
        print(e)
        msgbox.showerror("ERROR", "ERROR FETCHING DATA")
    return None
def valuefetcher():
    asyncio.run(valuefetch())
# GUI
root.geometry(f"{width}x{height}")
root.title("Stock Market Analyzer")

question_menu = tk.OptionMenu(root, value_inside, *names) 
question_menu.pack(anchor="center")

submit=tk.Button(root, text="Fetch Data", command=valuefetcher)
submit.pack(anchor='center')


root.mainloop()