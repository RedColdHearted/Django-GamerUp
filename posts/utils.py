import os
import uuid


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
