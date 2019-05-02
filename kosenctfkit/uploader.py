import os
import shutil
from base64 import b64decode
from secrets import token_hex
from io import BytesIO
from PIL import Image


class Uploader:
    def init(self, app):
        self.icon_dir = os.path.join(app.static_folder, app.config["ICON_DIR"])
        self.static_dir = os.path.join(app.static_folder, app.config["STATIC_DIR"])
        self.static_url_path = app.static_url_path

    def upload_icon(self, icon_b64):
        filename = token_hex(16) + ".png"
        filepath = os.path.join(self.icon_dir, filename)
        try:
            icon_data = b64decode(icon_b64)
            icon = Image.open(BytesIO(icon_data))
            icon.load()
            icon.save(filepath)
        except Exception as e:
            print(e)
            return None

        return filepath

    def upload_attachment(self, name):
        basename = os.path.basename(name)
        path = os.path.join(self.static_dir, basename)
        try:
            shutil.copyfile(name, path)
        except Exception as e:
            print(e)
            return None

        return os.path.join(self.static_url_path, basename)


uploader = Uploader()
