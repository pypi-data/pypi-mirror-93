import shutil
import re
import os
from kpl_helper.base import get_config
import requests
import uuid
import logging


HAN_SCRIPT_PAT = re.compile(
    r'[\u4E00-\u9FEF\u3400-\u4DB5\u20000-\u2A6D6\u2A700-\u2B734'
    r'\u2B740-\u2B81D\u2D820-\u2CEA1\u2CEB0-\u2EBE0]'
)


class Uploader:
    def __init__(self):
        self._api = get_config().get_api_url()
        self._token = get_config().get_jwt_token()
        self.sess = requests.session()
        self.post = self._wrap(self.sess.post)

    def _wrap(self, func):
        def wrapped_http(router, **kwargs):
            kwargs["headers"] = {"Authorization": self._token}
            kwargs["url"] = self._api + router
            res = func(**kwargs)
            if not res.ok:
                raise Exception("Network error. status code:", res.status_code)
            response = res.json()
            if response['code'] != 'Success':
                raise Exception("Response error. code: [{}]. message: [{}]".format(response['code'], response['msg']))
            return response.get('data', None)
        return wrapped_http

    @staticmethod
    def _make_archive(root_dir, base_dir):
        tar_path = os.path.join("/tmp", uuid.uuid4().hex)
        shutil.make_archive(tar_path, "tar",
                            root_dir=root_dir,
                            base_dir=base_dir)
        return tar_path + ".tar"

    def _upload(self, route, name, desc, path, make_archive=False):
        path = os.path.abspath(path)
        if os.path.islink(path):
            raise Exception("[kpl-helper]: `{}` is symbol link. cannot make archive".format(path))
        if not get_config().get_inner():
            return
        upload_file = path
        if make_archive:
            root_dir = os.path.abspath(os.path.join(path, ".."))
            upload_file = self._make_archive(root_dir, os.path.basename(path))
        with open(upload_file, "rb") as fi:
            self.post(route,
                      data={"name": name, "description": desc},
                      files={"file": (os.path.basename(upload_file), fi)})
        if make_archive:
            os.remove(upload_file)

    def upload_dataset(self, name, desc, path):
        self._upload("/upload/dataset", name, desc, path, True)

    def upload_dataset_fs(self, name, desc, path):
        self._upload("/upload/dataset_fs", name, desc, path, True)

    def upload_model(self, name, desc, path):
        self._upload("/upload/model", name, desc, path, os.path.isdir(path))


def save_dataset(path, name, description, as_serialized=False):
    try:
        uploader = Uploader()
        if as_serialized:
            uploader.upload_dataset(name, description, path)
        else:
            uploader.upload_dataset_fs(name, description, path)
    except Exception as e:
        logging.exception(e)
        return
    logging.info("[kpl-helper]: Save dataset success~")


def save_model(path, name, description):
    try:
        uploader = Uploader()
        uploader.upload_model(name, description, path)
    except Exception as e:
        logging.exception(e)
        return
    logging.info("[kpl-helper]: Save model success~")

