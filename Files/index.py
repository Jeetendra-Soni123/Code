# Imports
import asyncio
import tkinter as tk
from tkinter import PhotoImage, Toplevel, Frame, Canvas, Scrollbar, messagebox as msgbox
import matplotlib.pyplot as plt
import aiohttp
import numpy as np
import math as mt
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
    "Vanguard Small Cap Index": "VXCV",
    "CAC 40 Index": "XAX",
    "NYSE Composite": "XBX",
    "FTSE 100 Index": "XCAX",
    "Xetra Dax": "XDAX",
    "NYSE Composite": "XNET",
    "FTSE 100 Index": "XSE"
           }
names = list(options.keys())
value_inside = tk.StringVar(root) 
value_inside.set("Select a Stock")
data = 0
height, width = 300, 350

# Functions

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
    plt.savefig(f'Plot - {file}.png', bbox_inches="tight")
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
            plotter(date, high, "#32a852", "Date", "High", "Changes in High", file_name[0])
            plotter(date, low, "#32a852", "Date", "Low", "Changes in Low", file_name[1])
            plotter(date, open, "#32a852", "Date", "Open", "Changes in Open", file_name[2])
            plotter(date, close, "#32a852", "Date", "Close", "Changes in Close", file_name[3])
            plotter(date, volume, "#32a852", "Date", "Volume", "Changes in Volume", file_name[4])
            # New window
            newWindow = Toplevel(root)
            newWindow.title("Analysis")
            #newWindow.geometry("500x400")
            newWindow.attributes('-fullscreen', True)
            newWindow.resizable(False, False)
            newWindow.bind("<Escape>", lambda event: newWindow.destroy())


            # Create a main frame to hold the canvas and vertical scrollbar
            main_frame = Frame(newWindow)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Create a canvas within the main frame
            canvas = Canvas(main_frame)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Add a vertical scrollbar to the main frame
            y_scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Add a horizontal scrollbar directly to the newWindow, spanning full width
            x_scrollbar = Scrollbar(newWindow, orient=tk.HORIZONTAL, command=canvas.xview)
            x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

            # Configure the canvas to work with the scrollbars
            canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            # Create a frame within the canvas to hold the images
            image_frame = Frame(canvas)
            canvas.create_window((0, 0), window=image_frame, anchor="nw")

            # List to keep references to the PhotoImage objects
            images = []

            # Load and display images
            for file in file_name:
                try:
                    # Load the image file
                    graph_img = PhotoImage(file=f"Plot - {file}.png")

                    # Get the screen width and adjust the image width to fit the screen
                    screen_width = newWindow.winfo_screenwidth()
                    img_width = graph_img.width()
                    if img_width > screen_width:
                        scaling_factor = img_width / screen_width
                        graph_img = graph_img.subsample(int(scaling_factor))

                    # Keep a reference to the image to prevent garbage collection
                    images.append(graph_img)

                    # Create a label for each image and pack it
                    label = tk.Label(image_frame, image=graph_img)
                    label.pack(pady=10)  # Add some vertical spacing between images
                except Exception as e:
                    print(f"Error loading image {file}: {e}")

            # Update scroll region after all images are loaded
            def update_scroll_region(event=None):
                canvas.configure(scrollregion=canvas.bbox("all"))

            # Bind the configure event to update scroll region dynamically
            image_frame.bind("<Configure>", update_scroll_region)
            
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