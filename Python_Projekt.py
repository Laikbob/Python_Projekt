from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter

image_label = None
text_entry = None
image_path = None
original_image = None  # Храним оригинальное изображение
pil_image = None  # Текущее изменённое изображение
font_size = 14  # Default font size
text_position = "Top Left"  # Default position
text_color = "red"  # Default text color

font_path = "arial.ttf"

def choose_image():
    global image_path, original_image, pil_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path = file_path
        original_image = Image.open(file_path)  # Сохраняем оригинал
        pil_image = original_image.copy()
        show_image()

def show_image():
    global pil_image, canvas
    if pil_image:
        img_resized = pil_image.resize((600, 500))
        tk_image = ImageTk.PhotoImage(img_resized)
        
        # Очистка canvas перед добавлением нового изображения
        canvas.delete("all")
        
        # Нарисуем рамку вокруг изображения
        canvas.create_rectangle(0, 0, 600, 500, outline="blue", width=4)
        
        # Добавляем изображение в центр canvas
        canvas.image = tk_image  # Держим ссылку, чтобы изображение не удалилось из памяти
        canvas.create_image(300, 250, image=tk_image, anchor="center")


def add_text():
    global pil_image
    if pil_image:
        text = text_entry.get()
        draw = ImageDraw.Draw(pil_image)
        
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        positions = {
            "Top Left": (10, 10),
            "Top Right": (pil_image.width - text_width - 10, 10),
            "Bottom Left": (10, pil_image.height - text_height - 10),
            "Bottom Right": (pil_image.width - text_width - 10, pil_image.height - text_height - 10),
            "Center": (pil_image.width // 2 - text_width // 2, pil_image.height // 2 - text_height // 2)
        }
        
        draw.text(positions[text_position], text, fill=text_color, font=font)
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
    color = colorchooser.askcolor()[1]
    if color:
        text_color = color

def apply_filter(filter_name):
    global pil_image, original_image
    if original_image:
        pil_image = original_image.copy()  # Reset to original before applying filter
        if filter_name == "BLUR":
            pil_image = pil_image.filter(ImageFilter.BLUR)
        elif filter_name == "CONTOUR":
            pil_image = pil_image.filter(ImageFilter.CONTOUR)
        elif filter_name == "DETAIL":
            pil_image = pil_image.filter(ImageFilter.DETAIL)
        elif filter_name == "EDGE_ENHANCE":
            pil_image = pil_image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_name == "EMBOSS":
            pil_image = pil_image.filter(ImageFilter.EMBOSS)
        elif filter_name == "SHARPEN":
            pil_image = pil_image.filter(ImageFilter.SHARPEN)
        elif filter_name == "SMOOTH":
            pil_image = pil_image.filter(ImageFilter.SMOOTH)
        elif filter_name == "FIND_EDGES":
            pil_image = pil_image.filter(ImageFilter.FIND_EDGES)
        show_image()

def update_font_size(val):
    global font_size
    font_size = int(val)

def update_position(val):
    global text_position
    text_position = val

root = Tk()
root.title("Adobe Photoshop 1bit")
root.geometry("800x600")
root.config(bg="#f4f4f4")

right_frame = Frame(root, bg="#f4f4f4", padx=20, pady=20)
right_frame.pack(side="right", padx=20, pady=20)

center_frame = Frame(root, bg="#f4f4f4")
center_frame.pack(side="left", padx=20, pady=20)

# Create a Frame to display the image in the center
center_frame = Frame(root, bg="#f4f4f4")
center_frame.pack(side="left", padx=20, pady=20)

# Add a Canvas to draw a simple border (400x300) and place the image inside
canvas = Canvas(center_frame, width=600, height=500, bg="lightgray", bd=2, relief="solid")
canvas.grid(row=1, column=0, pady=10)

# Нарисуем рамку вокруг изображения (обычный прямоугольник)
canvas.create_rectangle(0, 0, 600, 500, outline="blue", width=4)

image_label = Label(center_frame, bg="#f4f4f4")
image_label.grid(row=0, column=0, pady=10)

text_entry = Entry(right_frame, font=("Helvetica", 14), bd=2, relief="solid", width=20, justify="center")
text_entry.grid(row=0, column=0, pady=10, padx=10)

font_size_scale = Scale(right_frame, from_=10, to_=100, orient="horizontal", label="Font Size", command=update_font_size, bg="#f4f4f4")
font_size_scale.set(14)
font_size_scale.grid(row=1, column=0, pady=10, padx=10)

position_var = StringVar(right_frame, "Center")
position_menu = OptionMenu(right_frame, position_var, "Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", command=update_position)
position_menu.grid(row=2, column=0, pady=10, padx=10)

color_button = Button(right_frame, text="Choose Text Color", font=("Helvetica", 12, "bold"), bg="green", fg="white", relief="solid", command=choose_color)
color_button.grid(row=3, column=0, pady=10)

button1 = Button(right_frame, text="ADD IMAGE", font=("Helvetica", 12, "bold"), bg="orange", fg="white", relief="solid", command=choose_image)
button1.grid(row=4, column=0, pady=10, padx=10)

button2 = Button(right_frame, text="ADD TEXT", font=("Helvetica", 12, "bold"), bg="yellow", fg="black", relief="solid", command=add_text)
button2.grid(row=5, column=0, pady=10, padx=10)

button3 = Button(right_frame, text="Save Photo", font=("Helvetica", 12, "bold"), bg="blue", fg="white", relief="solid", command=save_image)
button3.grid(row=6, column=0, pady=10)

filter_var = StringVar(right_frame, "None")
filter_menu = OptionMenu(right_frame, filter_var, "None", "BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EMBOSS", "SHARPEN", "SMOOTH", "FIND_EDGES", command=apply_filter)
filter_menu.grid(row=7, column=0, pady=10, padx=10)


root.mainloop()
