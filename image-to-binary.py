import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import io
import base64
import json

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.bmp;*.gif")])
    if file_path:
        try:
            img = Image.open(file_path)
            img_binary = image_to_binary(img)
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, img_binary)
        except Exception as e:
            print(f"Error loading image: {e}")

def image_to_binary(img):
    img_info = {
        "format": img.format,
        "size": img.size,
        "mode": img.mode
    }
    img_bytes = img.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    data = {
        "img_info": img_info,
        "img_data": img_base64
    }
    binary_data = json.dumps(data)
    return binary_data

def binary_to_image():
    binary_data = text_box.get(1.0, tk.END).strip()
    try:
        img = reconstruct_image(binary_data)
        display_image(img)
    except Exception as e:
        print(f"Error converting binary to image: {e}")

def reconstruct_image(binary_data):
    data = json.loads(binary_data)
    img_info = data['img_info']
    img_base64 = data['img_data']
    img_bytes = base64.b64decode(img_base64)
    img = Image.frombytes(img_info['mode'], img_info['size'], img_bytes)
    return img

def display_image(img):
    img.thumbnail((canvas.winfo_width(), canvas.winfo_height()))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

root = tk.Tk()
root.title("Image to Binary Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

upload_button = tk.Button(frame, text="Upload Image", command=open_image)
upload_button.pack(pady=5)

text_box = ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
text_box.pack(pady=5)

convert_button = tk.Button(frame, text="Convert Binary to Image", command=binary_to_image)
convert_button.pack(pady=5)

canvas = tk.Canvas(frame, width=300, height=300, bg="white")
canvas.pack(pady=5)

root.mainloop()
