from tkinter import PhotoImage, Frame, Canvas, Scrollbar
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
             