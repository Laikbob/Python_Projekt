from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

image_label = None
text_entry = None
image_path = None
pil_image = None
font_size = 14  # Default font size
text_position = "Top Left"  # Default position
text_color = "red"  # Default text color

# Use a standard font (make sure you have a valid TTF font in your system)
font_path = "arial.ttf"  # You can change this to any TTF font on your system

def choose_image():
    global image_path, pil_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path = file_path
        pil_image = Image.open(file_path)
        show_image()

def show_image():
    global pil_image, image_label
    if pil_image:
        img_resized = pil_image.resize((400, 300))
        tk_image = ImageTk.PhotoImage(img_resized)
        image_label.config(image=tk_image)
        image_label.image = tk_image

def add_text():
    global pil_image, text_entry, font_size, text_position, text_color
    if pil_image:
        text = text_entry.get()
        draw = ImageDraw.Draw(pil_image)

        # Load the font with the desired size
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            # Fallback to default font if the specific font is not found
            font = ImageFont.load_default()

        # Get text position based on user selection
        if text_position == "Top Left":
            position = (10, 10)
        elif text_position == "Top Right":
            position = (pil_image.width - len(text) * font_size, 10)
        elif text_position == "Bottom Left":
            position = (10, pil_image.height - font_size - 10)
        elif text_position == "Bottom Right":
            position = (pil_image.width - len(text) * font_size, pil_image.height - font_size - 10)
        elif text_position == "Center":
            position = (pil_image.width // 2 - len(text) * font_size // 2, pil_image.height // 2 - font_size // 2)
        
        draw.text(position, text, fill=text_color, font=font)
        show_image()

def save_image():
    global pil_image
    if pil_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if save_path:
            pil_image.save(save_path)
            print("Image saved successfully!")

def choose_color():
    global text_color
    color = colorchooser.askcolor()[1]  # This returns a tuple, the second element is the hex color code
    if color:
        text_color = color

# Font size selection
def update_font_size(val):
    global font_size
    font_size = int(val)

# Text position selection
def update_position(val):
    global text_position
    text_position = val


root = Tk()
root.title("Adobe Photoshop 1bit")
root.geometry("800x600")
root.config(bg="#f4f4f4")  # Set the background color of the window

# Create a Frame to organize the right-side controls
right_frame = Frame(root, bg="#f4f4f4", padx=20, pady=20)
right_frame.pack(side="right", padx=20, pady=20)

# Create a Frame to display the image in the center
center_frame = Frame(root, bg="#f4f4f4")
center_frame.pack(side="left", padx=20, pady=20)

# Add a label to display the image (centered in the left frame)
image_label = Label(center_frame, bg="#f4f4f4")
image_label.grid(row=0, column=0, pady=10)

label3 = Label(root, text="Picture:", font=("Helvetica", 18), fg="green", bg="lightgray")
label3.place(x=20, y=100)

label4 = Label(root, text="TEXT:", font=("Helvetica", 18), fg="green", bg="lightgray")
label4.place(x=1700, y=280)

# Text entry field with some enhancements
text_entry = Entry(right_frame, font=("Helvetica", 14), bd=2, relief="solid", width=20, justify="center")
text_entry.grid(row=0, column=0, pady=10, padx=10)

# Font size scale slider
font_size_scale = Scale(right_frame, from_=10, to_=100, orient="horizontal", label="Font Size", command=update_font_size, bg="#f4f4f4")
font_size_scale.set(14)  # Set the default font size
font_size_scale.grid(row=1, column=0, pady=10, padx=10)

# Position selection menu
position_var = StringVar(right_frame, "Center")
position_menu = OptionMenu(right_frame, position_var, "Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", command=update_position)
position_menu.grid(row=2, column=0, pady=10, padx=10)

# Button for choosing text color
color_button = Button(right_frame, text="Choose Text Color", font=("Helvetica", 12, "bold"), bg="green", fg="white", relief="solid", command=choose_color)
color_button.grid(row=3, column=0, pady=10)

# Buttons for adding image, text, and saving the photo
button1 = Button(right_frame, text="ADD IMAGE", font=("Helvetica", 12, "bold"), bg="orange", fg="white", relief="solid", command=choose_image)
button1.grid(row=4, column=0, pady=10, padx=10)

button2 = Button(right_frame, text="ADD TEXT", font=("Helvetica", 12, "bold"), bg="yellow", fg="black", relief="solid", command=add_text)
button2.grid(row=5, column=0, pady=10, padx=10)

button3 = Button(right_frame, text="Save Photo", font=("Helvetica", 12, "bold"), bg="blue", fg="white", relief="solid", command=save_image)
button3.grid(row=6, column=0, pady=10)

root.mainloop()  