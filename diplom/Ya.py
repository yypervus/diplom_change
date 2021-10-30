import requests
from tqdm import tqdm
import json
import datetime
from loguru import logger
from Vk import *

class YaUser:
    @logger.catch()
    def __init__(self, token: str):
        self.token = token
        self.directory_upload = ''

    def create_folder(self, direct=None):
        if direct is not None:
            directory = direct
        else:
            directory = 'directory_file'
        response = requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            params={
                        "path": directory
            },
            headers={
                    "Authorization": f"OAuth {self.token}"
            }
            )
        self.directory_upload = directory
        if 'message' in response.json():
            logger.warning(f'Указанная папка на Яндекс диске была создана ранее')
        elif 'method' in response.json():
            logger.info(f'Папка на Яндекс диске создана успешно')
        else:
            response.raise_for_status()
        return directory

    @logger.catch()
    def upload(self, user):
        if isinstance(user, VkUser):
            for load in tqdm(user.info_foto_list, desc='Идет загрузка файлов', leave=False):
                file_name = load['file-name']
                file_url = load['url']
                response = requests.post(
                    "https://cloud-api.yandex.net/v1/disk/resources/upload",
                    params={
                        "path": f'{self.directory_upload}/{file_name}',
                        'url': file_url
                    },
                    headers={
                    "Authorization": f"OAuth {self.token}"
                    }
                )
                response.raise_for_status()
        logger.info(f'Фотографии загружены')
        return

    @logger.catch()
    def copying_photos_to_disk(self, user):
        if isinstance(user, VkUser):
            user.create_list_with_requested_information()
            self.create_folder()
            self.upload(user)
            user.create_json()
            logger.info(f'\nПрограмма завершена успешно!')
            return