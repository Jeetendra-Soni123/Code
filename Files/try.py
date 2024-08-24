from tkinter import PhotoImage, Toplevel, Frame, Canvas, Scrollbar, messagebox as msgbox
import tkinter as tk
newWindow = tk.Tk()
newWindow.title("Scrollable Image Viewer")
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
file_name=['date-high','date-low','date-open','date-close','date-volume']
# Load and display images
for file_nam in file_name:
    try:
        # Load the image file
        graph_img = PhotoImage(file=f"Plot - {file_nam}.png")

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
        print(f"Error loading image {file_nam}: {e}")

# Update scroll region after all images are loaded
def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the configure event to update scroll region dynamically
image_frame.bind("<Configure>", update_scroll_region)

newWindow.mainloop()