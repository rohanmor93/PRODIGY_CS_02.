import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import random

def scramble_image(img, key):
    random.seed(key)
    width, height = img.size
    pixels = list(img.getdata())
    
    # Create a shuffled copy of indices
    indices = list(range(len(pixels)))
    random.shuffle(indices)

    scrambled_pixels = [pixels[i] for i in indices]
    scrambled_img = Image.new(img.mode, img.size)
    scrambled_img.putdata(scrambled_pixels)

    return scrambled_img, indices  # Also return order for decryption

def unscramble_image(img, key):
    random.seed(key)
    width, height = img.size
    pixels = list(img.getdata())
    
    indices = list(range(len(pixels)))
    random.shuffle(indices)

    original_pixels = [None] * len(pixels)
    for i, idx in enumerate(indices):
        original_pixels[idx] = pixels[i]

    unscrambled_img = Image.new(img.mode, img.size)
    unscrambled_img.putdata(original_pixels)
    return unscrambled_img

# GUI Functions
def select_image():
    file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.bmp")])
    if file:
        image_path.set(file)

def save_output_image(img):
    path = filedialog.asksaveasfilename(defaultextension=".png")
    if path:
        img.save(path)
        messagebox.showinfo("Saved", f"Image saved at:\n{path}")

def process_image(mode):
    path = image_path.get()
    key = key_entry.get()
    
    if not path or not key:
        messagebox.showerror("Missing", "Please select an image and enter a key.")
        return

    try:
        img = Image.open(path)
        if mode == "scramble":
            scrambled_img, _ = scramble_image(img, key)
            save_output_image(scrambled_img)
        elif mode == "unscramble":
            unscrambled_img = unscramble_image(img, key)
            save_output_image(unscrambled_img)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# GUI Layout
root = tk.Tk()
root.title("Image Scrambler / Unscrambler")
root.geometry("500x300")

image_path = tk.StringVar()

tk.Label(root, text="1. Select Image").pack()
tk.Entry(root, textvariable=image_path, width=60).pack()
tk.Button(root, text="Browse", command=select_image).pack()

tk.Label(root, text="2. Enter Key (string)").pack()
key_entry = tk.Entry(root, width=30)
key_entry.pack()

tk.Button(root, text="🔀 Scramble Image", command=lambda: process_image("scramble"),
          bg="#FF9800", fg="white").pack(pady=10)

tk.Button(root, text="🔁 Unscramble Image", command=lambda: process_image("unscramble"),
          bg="#4CAF50", fg="white").pack(pady=10)

root.mainloop()
