import logging
import os
import uuid
import shutil
from enum import Enum
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from cas.concurrency import CallBackThread

_LOGGER = logging.getLogger('cas.model.file')
_BUCKET_NAME = os.getenv('AWS_CURRENT_BUCKET_NAME', 'acabim-staging')


class AwsIfcFileDownloader:
    """This class is used to retrieve a file from the AWS S3. When this class goes out of scope, and is garbage
    collected, the downloaded file will automatically be removed from the temporary directory"""

    def __init__(self, file_name, auto_download=True, file_available_callback=None, file_unavailable_callback=None):
        if file_available_callback is not None and not callable(file_available_callback):
            raise TypeError('expected callable function, not {0}'.format(type(file_available_callback)))

        if file_unavailable_callback is not None and not callable(file_unavailable_callback):
            raise TypeError('expected callable function, not {0}'.format(type(file_unavailable_callback)))

        self.file_name = file_name
        self.__download_thread = None
        self.__temp_folder = str(uuid.uuid4())
        self.__file_available_callback = file_available_callback
        self.__file_unavailable_callback = file_unavailable_callback

        _LOGGER.debug('Initialised S3 Access for IFC File "%s"', file_name)
        if auto_download:
            self.download_file()

    def __del__(self):
        _LOGGER.debug('Removing downloaded file "%s"', self.file_name)
        try:
            if self.is_file_downloaded():
                os.remove(self.get_local_file_path())
                shutil.rmtree(self.__get_temp_path(), ignore_errors=True)
        except OSError as e:
            _LOGGER.exception(e, 'Unable to cleanup data')

    def is_file_downloaded(self):
        return os.path.exists(self.get_local_file_path())

    def is_downloading(self):
        return self.__download_thread is not None

    def get_local_file_path(self):
        return '{0}/{1}.ifc'.format(self.get_local_file_dir(), self.file_name)

    def get_local_file_name(self):
        return '{0}.ifc'.format(self.file_name)

    def get_local_file_dir(self):
        return self.__get_temp_path()

    def wait_for_download(self):
        if self.__download_thread is not None:
            self.__download_thread.join()

    def download_file(self):
        if not self.is_file_downloaded():
            if self.__download_thread is None:
                def download_impl():
                    _LOGGER.debug('Starting S3 File download from bucket %s', _BUCKET_NAME)
                    boto3.client('s3').download_file(Bucket=_BUCKET_NAME, Key='IFC/{0}.ifc'.format(self.file_name),
                                                     Filename=self.get_local_file_path())

                self.__download_thread = CallBackThread(download_impl, callback=self.__on_download_finished,
                                                        exception_callback=self.__on_download_exception)
                self.__download_thread.setName('cas_aws_file_dl:{0}'.format(self.file_name))
                self.__download_thread.daemon = True
                self.__download_thread.start()
                _LOGGER.debug('File download started for "%s"', self.file_name)
            else:
                _LOGGER.warning('File is already downloading')
        else:
            _LOGGER.debug('File is already downloaded')

    def __get_temp_path(self):
        folder_path = '{0}/.local/acabim-python/{1}/'.format(str(Path.home()), self.__temp_folder)
        if not os.path.exists(folder_path):
            _LOGGER.debug('Creating Path "%s"', folder_path)
            os.makedirs(folder_path)

        return folder_path

    def __on_download_finished(self):
        _LOGGER.info('File "%s" download complete', self.file_name)
        self.__download_thread = None
        if self.__file_available_callback is not None:
            self.__file_available_callback(self)

    def __on_download_exception(self, exception):
        _LOGGER.exception(exception)
        self.__download_thread = None
        if self.__file_unavailable_callback is not None:
            self.__file_unavailable_callback(exception)


class AwsFileType(Enum):
    IFC = 1
    GLB = 2


def upload_file(file_path, file_type):
    file_name = os.path.basename(file_path)
    obj_name = '{0}/{1}'.format(file_type.name, file_name)
    try:
        boto3.client('s3').upload_file(file_path, _BUCKET_NAME, obj_name)
        _LOGGER.info('File %s uploaded to %s successfully', file_name, _BUCKET_NAME)
    except ClientError as e:
        _LOGGER.exception(e, 'Unable to upload file %s to bucket %s', file_path, _BUCKET_NAME)
        return False
    return True


if __name__ == '__main__':
    import cas.configure as c
    c.configure_logging()
    AwsIfcFileDownloader('Linwood')
    import time
    time.sleep(40)
