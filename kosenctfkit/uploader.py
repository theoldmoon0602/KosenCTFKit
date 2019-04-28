import os
from base64 import b64decode
from secrets import token_hex
from io import BytesIO
from PIL import Image


class Uploader:
    def init(self, directory, url_root):
        self.directory = directory
        self.url_root = url_root

    def upload_icon(self, icon_b64):
        filename = token_hex(16) + ".png"
        filepath = os.path.join(self.directory, filename)
        fileurl = os.path.join(self.url_root, filename)
        try:
            icon_data = b64decode(icon_b64)
            icon = Image.open(BytesIO(icon_data))
            icon.load()
            icon.save(filepath)
        except Exception as e:
            print(e)
            return None

        return fileurl


uploader = Uploader()
