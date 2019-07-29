import os
import shutil
import boto3
import os
from base64 import b64decode
from io import BytesIO
from PIL import Image
from uuid import uuid4


def unique_name():
    return str(uuid4()).replace("-", "")


class S3Uploader:
    def __init__(self, app):
        self.aws_credential = {
            "aws_access_key_id": app.config["AWS_ACCESS_KEY"],
            "aws_secret_access_key": app.config["AWS_ACCESS_SECRET"],
        }
        self.icon_dir = app.config["ICON_DIR"]
        self.bucket = app.config["S3_BUCKET"]
        self.region = app.config["S3_REGION"]

    def upload(self, data, key):
        # upload
        s3 = boto3.client("s3", region_name=self.region, **self.aws_credential)
        s3.put_object(Body=data, Bucket=self.bucket, ACL="public-read", Key=key)

        # get url
        url = "{}/{}/{}".format(s3.meta.endpoint_url, self.bucket, key)
        return url

    def upload_icon(self, icon_b64):
        filename = os.path.join(self.icon_dir, unique_name())
        return self.upload(b64decode(icon_b64), filename)

    def upload_attachment(self, name):
        key = os.path.join(unique_name(), os.path.basename(name))
        return self.upload(open(name, "rb"), key)


class LocalUploader:
    def __init__(self, app):
        self.icon_dir = os.path.join(app.static_folder, app.config["ICON_DIR"])
        self.static_dir = os.path.join(app.static_folder, app.config["STATIC_DIR"])
        self.static_url_path = app.static_url_path

    def upload_icon(self, icon_b64):
        filename = unique_name() + ".png"
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
        directory = unique_name()
        directory_path = os.path.join(self.static_dir, directory)
        path = os.path.join(directory_path, basename)
        try:
            os.mkdir(directory_path)
            shutil.copyfile(name, path)
        except Exception as e:
            print(e)
            return None

        return os.path.join(self.static_url_path, directory, basename)
