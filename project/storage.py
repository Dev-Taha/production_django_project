import cloudinary.api
from cloudinary_storage.storage import MediaCloudinaryStorage


IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg', 'ico', 'tiff', 'tif', 'avif'}


class SmartCloudinaryStorage(MediaCloudinaryStorage):
    def _get_resource_type(self, name):
        ext = name.lower().rsplit('.', 1)[-1] if '.' in name else ''
        return 'image' if ext in IMAGE_EXTENSIONS else 'raw'

    def exists(self, name):
        name = self._prepend_prefix(name)
        try:
            cloudinary.api.resource(name, resource_type=self._get_resource_type(name))
            return True
        except cloudinary.exceptions.NotFound:
            return False
