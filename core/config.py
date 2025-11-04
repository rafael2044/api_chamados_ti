import cloudinary


from core.settings import Settings

cloudinary.config(
    cloud_name = Settings().CLOUD_NAME,
    api_key = Settings().CLOUD_API_KEY,
    api_secret = Settings().CLOUD_SECRET_KEY
)