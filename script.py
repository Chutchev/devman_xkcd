import requests
from dotenv import load_dotenv
import os
import random


VERSION_API = 5.92


def wall_post(info, alt, access_token, group_id):
    url = 'https://api.vk.com/method/wall.post'
    owner_id = info['owner_id']
    media_id = info['id']
    params = {'from_group': 0,
              'owner_id': -int(group_id),
              'message': alt,
              'attachments': f'photo{owner_id}_{media_id}',
              'access_token': access_token,
              'v': VERSION_API}
    requests.post(url, params=params)


def save_wall_photo(group_id, server, hash, photo, access_token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'server': server,
              'hash': hash,
              'photo': photo,
              'group_id': group_id,
              'access_token': access_token,
              'v': VERSION_API}
    response = requests.post(url, params=params)
    info = response.json()
    return info


def upload_image_on_server(upload_url, group_id, comics):
    with open(f'{comics}.png', 'rb') as f:
        image = f.read()
    files = {'photo': (f'{comics}.png', image)}
    params = {'group_id': group_id, 'v': VERSION_API}
    response = requests.post(upload_url, files=files, params=params)
    json_content = response.json()
    return json_content['server'], json_content['photo'], json_content['hash']


def get_wall_upload_server(access_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': access_token, 'group_id': group_id, 'v': VERSION_API}
    response = requests.get(url, params=params)
    return response.json()['response']['upload_url']


def download_picture(image_url, comics_number):
    response = requests.get(image_url)
    with open(f'{comics_number}.png', 'wb') as f:
        f.write(response.content)


def main():
    load_dotenv()
    access_token = os.getenv('access_token')
    group_id = os.getenv('group_id')
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    comics_number = response.json()['num']
    comics = random.randint(0, comics_number)
    url = f'https://xkcd.com/{comics}/info.0.json'
    response = requests.get(url)
    image_url, alt = response.json()['img'], response.json()['alt']
    download_picture(image_url, comics)
    upload_url = get_wall_upload_server(access_token, group_id)
    server, photo, hash = upload_image_on_server(upload_url, group_id, comics)
    info = save_wall_photo(group_id, server, hash, photo, access_token)
    wall_post(*info['response'], alt, access_token, group_id)
    os.remove(f'{comics}.png')


if __name__ == "__main__":
    main()