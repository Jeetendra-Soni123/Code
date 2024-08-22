# Imports
import asyncio
import tkinter as tk
from tkinter import messagebox as msgbox
import matplotlib
import aiohttp
from tkinter.ttk import *
# Variables
root=tk.Tk()
options = {
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
height, width = 600, 900

# Functions
async def fetch(x):
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
    else:
        submit.config(text="Fetch Data", state=tk.NORMAL)
        msgbox.showinfo("COMPLETED", "Stock market data has been anaylized")
        # New window
        newWindow = Toplevel(master)
        newWindow.title("New Window")
        newWindow.geometry("200x200")
        Label(newWindow, text ="This is a new window").pack()
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

root.mainloop()