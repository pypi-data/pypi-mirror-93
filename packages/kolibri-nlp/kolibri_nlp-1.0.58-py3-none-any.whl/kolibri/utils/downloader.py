import os
import sys
import logging
import tarfile
import shutil
import requests
import re
from tqdm import tqdm
from kolibri.settings import resources_path

DATA_DIR = resources_path
LOGGER = logging.getLogger(__name__)


class Downloader(object):
    def __init__(self, pkg, sub_package=None, url=None, download_dir=DATA_DIR):
        self._error = None
        self.url = url
        self.pkg = pkg
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        if not os.path.exists(os.path.join(download_dir, pkg)):
            os.makedirs(os.path.join(download_dir, pkg))
            self.download_dir = os.path.join(os.path.join(download_dir, pkg))
            self._download_data()
        if sub_package:
            if not os.path.exists(os.path.join(download_dir, pkg, sub_package)):
                self.download_dir = os.path.join(os.path.join(download_dir, pkg))
                self._download_data()
        else:
            LOGGER.info('data already set up')

    @staticmethod
    def get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename="(.+)"', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def _download_data(self):
        LOGGER.info('downloading data for {}...'.format(self.pkg))
        r = requests.get(self.url, stream=True)
        total_length = r.headers.get('content-length', 0)
        pbar = tqdm(
                unit='B', unit_scale=True,
                total=int(total_length))
        if total_length is None:
            LOGGER.error("Couldn't fetch model data.")
            raise Exception("Couldn't fetch model data.")
        else:
            filename = self.get_filename_from_cd(
                r.headers.get('content-disposition'))
            path = os.path.join(self.download_dir, filename)
            with open(path, 'wb') as f:
                for data in r.iter_content(chunk_size=4096):
                    f.write(data)
                    pbar.update(len(data))
            if filename.endswith('.tar.gz'):
                tar = tarfile.open(path, "r:gz")
                for tarinfo in tar:
                    tar.extract(tarinfo, self.download_dir)
                tar.close()
            # clean raw tar gz
            os.remove(path)
            LOGGER.info('download complete')
