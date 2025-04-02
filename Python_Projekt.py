from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter

image_path = None
original_image = None  # Исходное изображение
edited_image = None  # Изображение с текстом
current_image = None  # Отображаемое изображение (с фильтром)
font_size = 14
text_position = "Center"
text_color = "red"
font_path = "arial.ttf"
text_entries = []  # Список всех добавленных текстов

def choose_image():
    global image_path, original_image, edited_image, current_image, text_entries
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path = file_path
        original_image = Image.open(file_path)
        edited_image = original_image.copy()
        current_image = edited_image.copy()
        text_entries = []  # Очистка списка текстов при загрузке нового изображения
        show_image()

def show_image():
    global current_image, canvas
    if current_image:
        img_resized = current_image.resize((600, 500))
        tk_image = ImageTk.PhotoImage(img_resized)
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 600, 500, outline="blue", width=4)
        canvas.image = tk_image
        canvas.create_image(300, 250, image=tk_image, anchor="center")

def add_text():
    global edited_image, current_image, text_entries
    if original_image:
        text = text_entry.get()
        if text:
            text_entries.append((text, text_position, text_color, font_size))
            redraw_texts()

def redraw_texts():
    global edited_image, current_image, text_entries
    edited_image = original_image.copy()
    draw = ImageDraw.Draw(edited_image)
    for text, position, color, size in text_entries:
        try:
            font = ImageFont.truetype(font_path, size)
        except IOError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        positions = {
            "Top Left": (10, 10),
            "Top Right": (edited_image.width - text_width - 10, 10),
            "Bottom Left": (10, edited_image.height - text_height - 10),
            "Bottom Right": (edited_image.width - text_width - 10, edited_image.height - text_height - 10),
            "Center": (edited_image.width // 2 - text_width // 2, edited_image.height // 2 - text_height // 2)
        }
        draw.text(positions[position], text, fill=color, font=font)
    current_image = edited_image.copy()
    show_image()

def remove_texts():
    global text_entries, edited_image, current_image
    text_entries = []
    redraw_texts()

def apply_filter(filter_name):
    global current_image, edited_image
    if edited_image:
        current_image = edited_image.copy()
        filters = {
            "BLUR": ImageFilter.BLUR,
            "CONTOUR": ImageFilter.CONTOUR,
            "DETAIL": ImageFilter.DETAIL,
            "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
            "EMBOSS": ImageFilter.EMBOSS,
            "SHARPEN": ImageFilter.SHARPEN,
            "SMOOTH": ImageFilter.SMOOTH,
            "FIND_EDGES": ImageFilter.FIND_EDGES,
        }
        if filter_name in filters:
            current_image = current_image.filter(filters[filter_name])
        show_image()

def save_image():
    global current_image
    if current_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if save_path:
            current_image.save(save_path)

def choose_color():
    global text_color
    color = colorchooser.askcolor()[1]
    if color:
        text_color = color

def update_font_size(val):
    global font_size
    font_size = int(val)

def update_position(val):
    global text_position
    text_position = val

def remove_image():
    global original_image, edited_image, current_image, image_path, text_entries
    original_image = None
    edited_image = None
    current_image = None
    image_path = None
    text_entries = []
    canvas.delete("all")

root = Tk()
root.title("Image Editor")
root.geometry("1000x600")

left_frame = Frame(root, bg="#2c3e50", padx=20, pady=20)
left_frame.pack(side="left", fill="y")

right_frame = Frame(root, bg="#ecf0f1", padx=20, pady=20)
right_frame.pack(side="right", fill="y")

center_frame = Frame(root, bg="#f4f4f4")
center_frame.pack(expand=True)

canvas = Canvas(center_frame, width=600, height=500, bg="lightgray", bd=2, relief="solid")
canvas.pack()

Button(left_frame, text="Add Image", font=("Arial", 12), bg="#3498db", fg="white", command=choose_image).pack(fill="x", pady=5)
Button(left_frame, text="Add Text", font=("Arial", 12), bg="#3498db", fg="white", command=add_text).pack(fill="x", pady=5)
Button(left_frame, text="Remove Texts", font=("Arial", 12), bg="#e67e22", fg="white", command=remove_texts).pack(fill="x", pady=5)
Button(left_frame, text="Save Photo", font=("Arial", 12), bg="#3498db", fg="white", command=save_image).pack(fill="x", pady=5)
Button(left_frame, text="Remove Image", font=("Arial", 12), bg="#c0392b", fg="white", command=remove_image).pack(fill="x", pady=5)

filter_var = StringVar(left_frame, "None")
filter_menu = OptionMenu(left_frame, filter_var, "None", "BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EMBOSS", "SHARPEN", "SMOOTH", "FIND_EDGES", command=apply_filter)
filter_menu.pack(fill="x", pady=5)

Label(right_frame, text="Text:", font=("Arial", 14), bg="#ecf0f1").pack()
text_entry = Entry(right_frame, font=("Arial", 14), width=20)
text_entry.pack(pady=5)

font_size_scale = Scale(right_frame, from_=10, to_=100, orient="horizontal", command=update_font_size)
font_size_scale.set(14)
font_size_scale.pack()

position_menu = OptionMenu(right_frame, StringVar(right_frame, "Center"), "Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", command=update_position)
position_menu.pack()

Button(right_frame, text="Choose Text Color", font=("Arial", 12), bg="#e74c3c", fg="white", command=choose_color).pack(fill="x", pady=5)

root.mainloop()
