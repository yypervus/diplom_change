import requests
from tqdm import tqdm
import json
import datetime
from loguru import logger

class VkUser:
    url = 'https://api.vk.com/method/'
    TOKEN_VK = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    VERSION = '5.126'
    params = {
        'access_token': TOKEN_VK,
        'v': VERSION
    }
    @logger.catch()
    def __init__(self, user_id=None):
        self.info_foto_list = []
        if user_id is not None:
            self.user_id = user_id
        else:
            self.user_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    @logger.catch()
    def photos_get(self, count=None):
        photos_get_url = self.url + 'photos.get'
        if count is not None:
            counter = count
        else:
            counter = 5
        photos_get_params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': counter,
            'rev': '1'
            }
        res = requests.get(photos_get_url, params={**self.params, **photos_get_params})
        res.raise_for_status()
        info_foto_dict = res.json()
        logger.info(f'Информация из Vk запрошена успешно')
        return info_foto_dict

    @logger.catch()
    def conv_dict_list(self, information_dict):
        foto_list = []
        for dict_ in information_dict['response']['items']:
            dict_foto = {}
            dict_foto['date'] = datetime.datetime.fromtimestamp(dict_['date']).strftime('%d.%m.%Y %H.%M.%S')
            dict_foto['likes'] = dict_['likes']['count']
            example = 0
            for var_url in dict_['sizes']:
                size = var_url['height'] * var_url['width']
                if size > example:
                    example = size
                    dict_foto['url'] = var_url['url']
                    dict_foto['size'] = var_url['type']
            foto_list.append(dict_foto)

        info_foto_list = []
        num = len(foto_list)
        for i in range(num - 1):
            dict_ = foto_list.pop()
            for string in foto_list:
                if string['likes'] == dict_['likes']:
                    dict_['file-name'] = '(' + str(dict_['date']) + ')' + str(dict_['likes']) + '.jpg'
                    break
                else:
                    dict_['file-name'] = str(dict_['likes']) + '.jpg'

            info_foto_list.append(dict_)

        last_dict = foto_list.pop()
        last_dict['file-name'] = str(last_dict['likes']) + '.jpg'
        info_foto_list.append(last_dict)
        logger.info(f'Информация отконвертирована в список')
        return info_foto_list

    @logger.catch()
    def create_list_with_requested_information(self, count=None):
        self.info_foto_list = self.conv_dict_list(self.photos_get(count))
        return

    @logger.catch
    def create_json(self, name=None):
        if name is not None:
            name_file = name
        else:
            name_file = 'output'
        info_list = self.info_foto_list
        for string in info_list:
            del string['likes'], string['date'], string['url']
        with open(name_file + '.json', "w") as f:
            json.dump(info_list, f, ensure_ascii=False, indent=4)
        logger.info(f'Создан файл с информацией по сохранённым фотографиям')
        return info_list
