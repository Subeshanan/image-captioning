
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from transformers import pipeline
import threading

# ---------------- AI MODEL ----------------

caption_model = None
selected_image = None
preview_image = None


def load_model():
    global caption_model

    if caption_model is None:
        status_label.config(text="Loading AI model... Please wait")
        caption_model = pipeline(
            "image-to-text",
            model="Salesforce/blip-image-captioning-base"
        )

    return caption_model


# ---------------- UPLOAD IMAGE ----------------

def upload_image():
    global selected_image, preview_image

    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")
        ]
    )

    if not file_path:
        return

    try:
        selected_image = Image.open(file_path).convert("RGB")

        display_image = selected_image.copy()
        display_image.thumbnail((450, 300))

        preview_image = ImageTk.PhotoImage(display_image)

        image_label.config(image=preview_image, text="")
        caption_label.config(
            text="Your AI-generated caption will appear here."
        )
        status_label.config(text="Image uploaded successfully!")

        generate_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Image Error", str(e))


# ---------------- GENERATE CAPTION ----------------

def generate_caption():
    if selected_image is None:
        messagebox.showwarning(
            "Warning",
            "Please upload an image first!"
        )
        return

    generate_button.config(state=tk.DISABLED)
    status_label.config(text="Generating caption...")

    threading.Thread(
        target=caption_worker,
        daemon=True
    ).start()


def caption_worker():
    try:
        model = load_model()

        result = model(selected_image)

        caption = result[0]["generated_text"]

        root.after(0, show_caption, caption)

    except Exception as e:
        root.after(0, show_error, str(e))


def show_caption(caption):
    caption_label.config(text=caption)
    status_label.config(text="Caption generated successfully!")
    generate_button.config(state=tk.NORMAL)


def show_error(error):
    status_label.config(text="Something went wrong.")
    generate_button.config(state=tk.NORMAL)

    messagebox.showerror(
        "AI Model Error",
        error
    )


# ---------------- COPY CAPTION ----------------

def copy_caption():
    caption = caption_label.cget("text")

    if not caption or caption.startswith("Your AI-generated"):
        messagebox.showwarning(
            "Warning",
            "Generate a caption first!"
        )
        return

    root.clipboard_clear()
    root.clipboard_append(caption)
    root.update()

    messagebox.showinfo(
        "Copied",
        "Caption copied successfully!"
    )


# ---------------- CLEAR IMAGE ----------------

def clear_image():
    global selected_image, preview_image

    selected_image = None
    preview_image = None

    image_label.config(
        image="",
        text="Upload an image to get started"
    )

    caption_label.config(
        text="Your AI-generated caption will appear here."
    )

    status_label.config(text="Ready to upload an image")

    generate_button.config(state=tk.DISABLED)


# ---------------- MAIN GUI ----------------

root = tk.Tk()

root.title("AI Image Caption Generator")
root.geometry("750x720")
root.configure(bg="#F0F4F8")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="AI IMAGE CAPTION GENERATOR",
    font=("Arial", 22, "bold"),
    bg="#F0F4F8",
    fg="#19376D"
)
heading.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Upload an image and let AI describe it!",
    font=("Arial", 12),
    bg="#F0F4F8",
    fg="#555555"
)
subtitle.pack(pady=5)

# Image display frame
image_frame = tk.Frame(
    root,
    bg="white",
    width=500,
    height=320,
    highlightbackground="#B4C5D6",
    highlightthickness=2
)
image_frame.pack(pady=20)

image_frame.pack_propagate(False)

image_label = tk.Label(
    image_frame,
    text="Upload an image to get started",
    font=("Arial", 14),
    bg="white",
    fg="#777777"
)
image_label.pack(expand=True)

# Upload button
upload_button = tk.Button(
    root,
    text="📁 Upload Image",
    font=("Arial", 12, "bold"),
    bg="#19376D",
    fg="white",
    width=20,
    command=upload_image,
    cursor="hand2"
)
upload_button.pack(pady=8)

# Generate caption button
generate_button = tk.Button(
    root,
    text="✨ Generate Caption",
    font=("Arial", 12, "bold"),
    bg="#159D82",
    fg="white",
    width=20,
    command=generate_caption,
    state=tk.DISABLED,
    cursor="hand2"
)
generate_button.pack(pady=8)

# Caption heading
caption_title = tk.Label(
    root,
    text="GENERATED CAPTION",
    font=("Arial", 14, "bold"),
    bg="#F0F4F8",
    fg="#19376D"
)
caption_title.pack(pady=10)

# Caption display
caption_label = tk.Label(
    root,
    text="Your AI-generated caption will appear here.",
    font=("Arial", 12),
    bg="white",
    fg="#222222",
    wraplength=600,
    width=65,
    height=3,
    relief="solid",
    bd=1
)
caption_label.pack(pady=5)

# Copy and clear buttons
button_frame = tk.Frame(root, bg="#F0F4F8")
button_frame.pack(pady=12)

copy_button = tk.Button(
    button_frame,
    text="📋 Copy Caption",
    font=("Arial", 11, "bold"),
    bg="#FFB703",
    fg="black",
    width=17,
    command=copy_caption,
    cursor="hand2"
)
copy_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(
    button_frame,
    text="🗑 Clear",
    font=("Arial", 11, "bold"),
    bg="#E63946",
    fg="white",
    width=17,
    command=clear_image,
    cursor="hand2"
)
clear_button.grid(row=0, column=1, padx=10)

# Status
status_label = tk.Label(
    root,
    text="Ready to upload an image",
    font=("Arial", 10),
    bg="#F0F4F8",
    fg="#555555"
)
status_label.pack(pady=10)

# Footer
footer = tk.Label(
    root,
    text="CODSOFT Internship | Task 3 - Image Captioning AI",
    font=("Arial", 9),
    bg="#F0F4F8",
    fg="#777777"
)
footer.pack(side=tk.BOTTOM, pady=12)

# Run application
root.mainloop()
