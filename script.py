import requests
from dotenv import load_dotenv
import os
import random


def wall_post(info, alt, access_token, group_id):
    url = 'https://api.vk.com/method/wall.post'
    owner_id = info['owner_id']
    media_id = info['id']
    params = {'from_group': 0,
              'owner_id': -int(group_id),
              'message': alt,
              'attachments': f'photo{owner_id}_{media_id}',
              'access_token': access_token,
              'v': 5.92}
    requests.post(url, params=params)


def save_wall_photo(group_id, server, hash, photo, access_token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'server': server,
              'hash': hash,
              'photo': photo,
              'group_id': group_id,
              'access_token': access_token,
              'v': 5.92}
    response = requests.post(url, params=params)
    info = response.json()
    return info


def upload_image_on_server(upload_url, group_id, comics):
    with open(f'{comics}.png', 'rb') as f:
        image = f.read()
    files = {'photo': (f'{comics}.png', image)}
    params = {'group_id': group_id, 'v': 5.92}
    response = requests.post(upload_url, files=files, params=params)
    return response.json()['server'], response.json()['photo'], response.json()['hash']


def get_wall_upload_server(access_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': access_token, 'group_id': group_id, 'v': 5.92}
    response = requests.get(url, params=params)
    return response.json()['response']['upload_url']


def parse_json(json_content):
    return json_content['img'], json_content['alt']


def download_picture(image_url, comics_number):
    response = requests.get(image_url)
    with open(f'{comics_number}.png', 'wb') as f:
        f.write(response.content)


def number_of_comics():
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    return response.json()['num']


def main():
    load_dotenv()
    access_token = os.getenv('access_token')
    group_id = os.getenv('group_id')
    comics_number = number_of_comics()
    comics = random.randint(0, comics_number)
    url = f'https://xkcd.com/{comics}/info.0.json'
    response = requests.get(url)
    image_url, alt = parse_json(response.json())
    download_picture(image_url, comics)
    upload_url = get_wall_upload_server(access_token, group_id)
    server, photo, hash = upload_image_on_server(upload_url, group_id, comics)
    info = save_wall_photo(group_id, server, hash, photo, access_token)
    wall_post(*info['response'], alt, access_token, group_id)
    os.remove(f'{comics}.png')


if __name__ == "__main__":
    main()