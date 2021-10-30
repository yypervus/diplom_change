import requests
from tqdm import tqdm
import json
import datetime
from tqdm import tqdm
from loguru import logger
from Vk import *
from Ya import *
logger.add("info.log", format="{time}{level}{message}", rotation="10 mb", compression="zip", serialize=False)

if __name__ == '__main__':
    begemot_korovin = VkUser()
    admin = YaUser('tokenYa')
    admin.copying_photos_to_disk(begemot_korovin)
    logger.info(f'Конец')