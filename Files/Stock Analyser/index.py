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
import pandas as pd

# Variables
graphfile = "show_graphs"
with open(f"./{graphfile}.py", "w") as tf:
    tf.write('''from tkinter import PhotoImage, Frame, Canvas, Scrollbar
import tkinter as tk

newWindow = tk.Tk()
newWindow.title("Scrollable Image Viewer")
newWindow.attributes('-fullscreen', True)
newWindow.resizable(False, False)
newWindow.bind("<Escape>", lambda event: newWindow.destroy())

main_frame = Frame(newWindow)
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.bind("<Left>",  lambda event: canvas.xview_scroll(-1, "units"))
canvas.bind("<Right>", lambda event: canvas.xview_scroll( 1, "units"))
canvas.bind("<Up>",    lambda event: canvas.yview_scroll(-1, "units"))
canvas.bind("<Down>",  lambda event: canvas.yview_scroll( 1, "units"))

y_scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
x_scrollbar = Scrollbar(newWindow, orient=tk.HORIZONTAL, command=canvas.xview)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
image_frame = Frame(canvas)
canvas.create_window((0, 0), window=image_frame, anchor="nw")

images = []
file_name = ['date-high', 'date-low', 'date-open', 'date-close', 'date-volume']

for file_nam in file_name:
    try:
        graph_img = PhotoImage(file=f"./graphs/Plot - {file_nam}.png")

        screen_width = newWindow.winfo_screenwidth()
        img_width = graph_img.width()
        if img_width > screen_width:
            scaling_factor = img_width / screen_width
            graph_img = graph_img.subsample(int(scaling_factor))

        images.append(graph_img)

        label = tk.Label(image_frame, image=graph_img)
        label.pack(pady=10)
    except Exception as e:
        print(f"Error loading image {file_nam}: {e}")

def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

image_frame.bind("<Configure>", update_scroll_region)

# Set focus on the canvas to capture key events
canvas.focus_set()

newWindow.mainloop()
             ''')
    print("Done!")
root=tk.Tk()
'''options = {
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
           }'''

df = pd.read_csv("./listing_status.csv")
options = df.set_index('name')['symbol'].to_dict()
unsorted = list(options.keys())
names = []
for i in unsorted:
    names.append(str(i))
names.sort()
value_inside = tk.StringVar(root) 
value_inside.set("Select a Stock")
data = 0
height, width = 300, 350

# Functions
def run_script():
    subprocess.run(["python", f"./{graphfile}.py"], check=True)


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
            submit.config(text="Loading Data...")
            raw = raw["Time Series (Daily)"]
            date, high, opens, close, volume, low = [], [], [], [], [], []
            for i in raw:
                x = raw[i]
                date = list(raw.keys())
                date.reverse()
                high.append(float(x["2. high"]))
                low.append(float(x["3. low"]))
                opens.append(float(x["1. open"]))
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
            plotter(date, opens, "#32a852", "Date", "Open", "Changes in Open", file_name[2])
            plotter(date, close, "#32a852", "Date", "Close", "Changes in Close", file_name[3])
            plotter(date, volume, "#32a852", "Date", "Volume", "Changes in Volume", file_name[4])
            
            # Run show_graphs.py
            run_script()
            data = tk.Toplevel(root)
            data.geometry("200X600")
            tk.Label(data,text="High",font=('bold',10)).pack()
            highdata=tk.Label(data,text=f"Average: 0\nMode: 0\nMeadian: 0")
            highdata.pack()
            tk.Label(data,text="Low",font=('bold',10)).pack()
            lowdata=tk.Label(data,text=f"Average: 0\nMode: 0\nMeadian: 0")
            lowdata.pack()
            tk.Label(data,text="Open",font=('bold',10)).pack()
            opendata=tk.Label(data,text=f"Average: 0\nMode: 0\nMeadian: 0")
            opendata.pack()
            tk.Label(data,text="Close",font=('bold',10)).pack()
            closedata=tk.Label(data,text=f"Average: 0\nMode: 0\nMeadian: 0")
            closedata.pack()
            tk.Label(data,text="Volume",font=('bold',10)).pack()
            voldata=tk.Label(data,text=f"Average: 0\nMode: 0\nMeadian: 0")
            voldata.pack()
            
            
            submit.config(text="Fetch Data", state=tk.NORMAL)
            
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
