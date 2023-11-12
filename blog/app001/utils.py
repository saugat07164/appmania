import os
import uuid

def upload_to_post_images(instance, filename):
    # This function generates a unique filename for each uploaded image
    ext = filename.split('.')[-1]
    # Use a universally unique identifier (UUID) to ensure a unique filename
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the full path where the image will be uploaded
    return os.path.join('post_images', filename)
