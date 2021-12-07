from PIL import Image
from django.conf import settings
import os


def average_rating(rating_list):
    if not rating_list:
        return 0
    return round(sum(rating_list) / len(rating_list))


def image_transformation(image_field, image_path):
    image_size = (50, 50)
    image = Image.open(image_field)
    image.thumbnail(image_size)
    image.save(image_path)
    return image
