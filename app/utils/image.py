import os
from PIL import Image


def save_profile_image(image_file, user_id: int, upload_dir: str = "uploads/profile_images") -> str:
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    image = Image.open(image_file)
    filename = f"{user_id}.png"
    image_path = os.path.join(upload_dir, filename)
    image.save(image_path)
    return image_path


def delete_profile_image(user_id: int, upload_dir: str = "uploads/profile_images"):
    filename = f"{user_id}.png"
    image_path = os.path.join(upload_dir, filename)
    if os.path.exists(image_path):
        os.remove(image_path)
