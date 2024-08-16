from PIL import Image, ImageTk

def create_button_image(image_file):
    img_btn = Image.open(image_file)
    img_btn = img_btn.resize((24, 24), Image.Resampling.LANCZOS)  # Resize image to 24x24 pixel
    img_btn = ImageTk.PhotoImage(img_btn)
    return img_btn