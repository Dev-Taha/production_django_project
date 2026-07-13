import cloudinary.api
from cloudinary_storage.storage import MediaCloudinaryStorage


IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg', 'ico', 'tiff', 'tif', 'avif'}
RAW_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'csv', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'tex', 'bib'}


class SmartCloudinaryStorage(MediaCloudinaryStorage):
    def _get_resource_type(self, name):
        ext = name.lower().rsplit('.', 1)[-1] if '.' in name else ''
        if ext in IMAGE_EXTENSIONS:
            return 'image'
        if ext in RAW_EXTENSIONS:
            return 'raw'
        return 'image'

    def exists(self, name):
        name = self._prepend_prefix(name)
        for rt in ('image', 'raw'):
            try:
                cloudinary.api.resource(name, resource_type=rt)
                return True
            except cloudinary.exceptions.NotFound:
                continue
        return False
