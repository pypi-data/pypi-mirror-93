import logging
import os
import time

from skippy.data.utils import get_file_name_urn

_LOCAL_SKIPPY_STORAGE = "/openfaas-local-storage/"


def has_local_storage_file(urn: str) -> bool:
    file_name = get_file_name_urn(urn)
    return os.path.exists(_LOCAL_SKIPPY_STORAGE + file_name)


def load_file_content_local_storage(urn: str):
    file_name = get_file_name_urn(urn)
    path = _LOCAL_SKIPPY_STORAGE + file_name
    logging.info('Reading file path %s' % path)
    start_time = time.time()
    content = open(path, 'r').read()
    logging.info('File read in %s' % (time.time() - start_time))
    return content


def save_file_content_local_storage(content: str, urn: str):
    file_name = get_file_name_urn(urn)
    path = _LOCAL_SKIPPY_STORAGE + file_name
    logging.info('Save file in local storage %s' % path)
    start_time = time.time()
    try:
        with open(path, 'w') as x_file:
            x_file.write(content)
        logging.info('File saved in %s' % (time.time() - start_time))
    except Exception as e:
        logging.error('Error trying to save file in local storage: %s', e)
