import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name = "dr9ritwbk",
    api_key = "353241786855269",
    api_secret = "f5xV0yfUbcyGPNHejZ_mdFSmaYA"
)

base = 'media'

for root, dirs, files in os.walk(base):
    for filename in files:
        filepath = os.path.join(root, filename)
        relative = os.path.relpath(filepath, base)
        public_id = relative.replace('\\', '/').rsplit('.', 1)[0]

        print(f"Uploading: {public_id}")
        cloudinary.uploader.upload(
            filepath,
            public_id=public_id,
            overwrite=True,
            resource_type="image",
            use_filename=True,
            unique_filename=False
        )
        print(f"✅ Done: {public_id}")

print("\nAll images uploaded!")