import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

media_folder = 'media'

for root, dirs, files in os.walk(media_folder):
    for filename in files:
        filepath = os.path.join(root, filename)
        print(f"Uploading {filepath}...")
        cloudinary.uploader.upload(filepath)
        print(f"✅ Done: {filename}")

print("All images uploaded!")