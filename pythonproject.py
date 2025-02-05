import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Global variables to manage state
current_image = 'C:\\Users\\Sneha R Hattimarad\\OneDrive\\Documents\\python'  # Path to images
displayed_image = None
image_list = []
current_index = -1
zoom_factor = 1.0
root = None
image_label = None
slideshow_running = False
slideshow_delay = 2000  # Delay between images in milliseconds (2 seconds)
slideshow_id = None  # ID to track the slideshow timer

# Function to create the GUI layout
def create_widgets():
    global root, image_label

    # Menu bar
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open", command=open_image)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_application)  # Exit command
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    # Welcome message at the center of the window with Algerian font
    welcome_label = tk.Label(root, text="......Welcome to Image Viewer......\nPlease select an option", 
                              font=("Algerian", 16), bg='navajowhite', fg='saddlebrown')
    welcome_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)  # Centered at the top

    # Image display area with no border and highlight thickness
    image_label = tk.Label(root, bd=0, highlightthickness=0)
    image_label.pack(expand=True)

    # Navigation buttons with no border and highlight thickness (optional)
    prev_button = tk.Button(root, text="Previous", command=show_previous_image, bd=0)
    next_button = tk.Button(root, text="Next", command=show_next_image, bd=0)
    prev_button.pack(side="left", padx=10, pady=10)
    next_button.pack(side="right", padx=10, pady=10)

    # Zoom and Rotate buttons with no border and highlight thickness (optional)
    zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in, bd=0)
    zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out, bd=0)
    rotate_button = tk.Button(root, text="Rotate", command=rotate_image, bd=0)
    zoom_in_button.pack(side="left", padx=10, pady=10)
    zoom_out_button.pack(side="left", padx=10, pady=10)
    rotate_button.pack(side="left", padx=10, pady=10)

    # Slideshow button with no border and highlight thickness (optional)
    slideshow_button = tk.Button(root, text="Start Slideshow", command=toggle_slideshow, bd=0)
    slideshow_button.pack(side="bottom", padx=10, pady=10)

    # Bind keyboard keys for navigation and actions
    root.bind("<Left>", lambda event: show_previous_image())
    root.bind("<Right>", lambda event: show_next_image())
    root.bind("<Up>", lambda event: zoom_in())  # Zoom In with Up Arrow
    root.bind("<Down>", lambda event: zoom_out())  # Zoom Out with Down Arrow
    root.bind("<space>", lambda event: toggle_slideshow())  # Start/Stop Slideshow with Spacebar

# Function to open an image using a file dialog
def open_image():
    global current_image, displayed_image, image_list, current_index, zoom_factor

    directory = filedialog.askdirectory()
    if not directory:
        return

    image_list = get_images_in_directory(directory)

    if image_list:
        current_index = 0
        zoom_factor = 1.0
        load_image(image_list[current_index])
        change_background_color("navajowhite")  # Change background color when images are loaded
        
        # Set the background image with the correct path
        set_background(r"C:\Users\Sneha R Hattimarad\OneDrive\Documents\python\background_image.png")  # Update the path
    else:
        messagebox.showerror("Error", "No images found in the selected directory.")

# Function to load an image and reset zoom factor
def load_image(image_path):
    global current_image, displayed_image

    try:
        img = Image.open(image_path)
        current_image = img
        displayed_image = img.copy()
        display_image(displayed_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

# Function to display the image in the label
def display_image(img):
    global image_label

    img_copy = img.copy()
    img_copy.thumbnail((800, 600))
    img_tk = ImageTk.PhotoImage(img_copy)

    image_label.config(image=img_tk)
    image_label.image = img_tk  # To prevent garbage collection

# Function to show the next image
def show_next_image():
    global current_index

    if current_index < len(image_list) - 1:
        current_index += 1
    else:
        current_index = 0  # Loop back to the first image
    
    load_image(image_list[current_index])

# Function to show the previous image
def show_previous_image():
    global current_index

    if current_index > 0:
        current_index -= 1
    else:
        current_index = len(image_list) - 1  # Loop back to the last image
    
    load_image(image_list[current_index])

# Function to zoom in the image
def zoom_in():
    global zoom_factor

    if current_image:
        zoom_factor *= 1.2
        resize_image()

# Function to zoom out the image
def zoom_out():
    global zoom_factor

    if current_image:
        zoom_factor *= 0.8
        resize_image()

# Function to resize the image based on zoom factor
def resize_image():
    global current_image, displayed_image

    if current_image:
        new_size = (int(current_image.width * zoom_factor), int(current_image.height * zoom_factor))
        resized_image = current_image.resize(new_size)
        display_image(resized_image)

# Function to rotate the image by 90 degrees
def rotate_image():
    global current_image

    if current_image:
        current_image = current_image.rotate(90, expand=True)
        display_image(current_image)

# Function to get all images in the current directory
def get_images_in_directory(directory):
   images = [os.path.join(directory, f) for f in os.listdir(directory) 
             if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
   
   return sorted(images)

# Function to start/stop the slideshow
def toggle_slideshow():
   global slideshow_running, slideshow_id

   if slideshow_running:
       root.after_cancel(slideshow_id)
       slideshow_running = False
   else:
       slideshow_running = True
       slideshow_id = root.after(slideshow_delay, slideshow)

# Function for the slideshow to display next image after delay
def slideshow():
   global slideshow_id

   if slideshow_running:
       show_next_image()
       slideshow_id = root.after(slideshow_delay, slideshow)

# Function to change background color of the main window.
def change_background_color(color):
   root.configure(bg=color)  # Change main window background color

# Function to set a tiled background image for the main window.
def set_background(image_path):
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)  # Resize to fit the window
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_image_tk)
        bg_label.place(relwidth=1, relheight=1)  # Cover the entire window
        bg_label.image = bg_image_tk  # Keep a reference to prevent garbage collection
    except Exception as e:
        print(f"Error loading background image: {e}")

# Function to exit the application gracefully and stop the slideshow if running.
def exit_application():
    global slideshow_running, slideshow_id

    # Stop the slideshow if it's running
    if slideshow_running:
        root.after_cancel(slideshow_id)
        slideshow_running = False

    # Close the application window
    root.quit()

# Main function to run the application 
def main():
   global root
   
   root = tk.Tk()
   
   root.title("Simple Image Viewer")
   
   # Set initial window size and colorful background 
   root.geometry("800x600")
   change_background_color('navajowhite')  # Set a default nude shade of brown
   
   # Add a border around the main window by configuring borderwidth and relief style.
   root.configure(borderwidth=5, relief=tk.SUNKEN) 

   create_widgets()
   root.mainloop()

# Run the main function if this file is executed 
if name == "main":
   main()


phase 2
