import os
import uuid
from random import randint

from app.settings import DEFAULT_PROFILE_PICS


def get_profile_image_upload_path(instance, filename: str) -> str:
    """
    This function is creating unique path name for profile pic file
    """
    ext = filename.split('.')[-1]
    new_filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_images', new_filename)


def get_post_image_upload_path(instance, filename: str) -> str:
    """
    This function is creating unique path name for post pic file
    """
    ext = filename.split('.')[-1]
    new_filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('post_images', new_filename)


def get_random_profile_picture() -> str:
    pic_path = DEFAULT_PROFILE_PICS[randint(0, 5)] + '.png'
    return pic_path


def is_not_default_pic(file_name: str) -> bool:
    if file_name in DEFAULT_PROFILE_PICS:
        return False
    return True

