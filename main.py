import requests
import json
import pprint

class YaDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
                }

    def yd_upload_url(self):
        return 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def yd_resources_url(self):
        return 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, disk_path):
        upload_url = self.yd_resources_url()
        headers = self.get_headers()
        params = {"path": disk_path,
                  "overwrite": "true"}
        href = requests.put(upload_url,
                            headers=headers,
                            params=params).json().get("href", "")

    def upload_url_to_disk(self, disk_file_path, file_url):
        upload_url = self.yd_upload_url()
        headers = self.get_headers()
        params = {'url': file_url,
                  'path': disk_file_path,
                  'disable_redirects': 'true'}
        href = requests.post(upload_url,
                             headers=headers,
                             params=params).json().get("href", "")

    def upload_file_to_disk(self, disk_path, filename):
        upload_url = self.yd_upload_url()
        headers = self.get_headers()
        params = {"path": disk_path,
                  "overwrite": "true"}
        href = requests.get(upload_url,
                            headers=headers,
                            params=params).json().get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


class VkUser:

    def __init__(self, token, target_user, target_album, count_photos):
        self.url = 'https://api.vk.com/method/photos.get'
        self.params = {
            'owner_id': target_user,
            'album_id': target_album,
            'count': count_photos,
            'rev': 1,
            'extended': 1,
            'photo_sizes': 0,
            'access_token': token,
            'v': '5.131'
        }

    def get_photo_list(self):
        print(f'\nзапрашиваем VK список фотографий в альбоме [{target_album}]')
        res = requests.get(self.url, params=self.params)
        real_photo_count = res.json()['response']['count']
        photo_list = res.json()['response']['items']
        if real_photo_count < count_photos:
            print(f'\nв альбоме обнаруженно только {real_photo_count} фото')
        print('\nформируем список фотографий лучшего качества\n')
        list_x = []
        for photo_x in photo_list:
            max_size = 0
            for photo_size in photo_x['sizes']:
                if max_size < int(photo_size['height']):
                    max_size = photo_size['height']
                    size_x = photo_size['type']
                    url_х = photo_size['url']
                    # print(photo_size['url'])
            list_x.append({'photo_id': photo_x['id'],
                           'date': photo_x['date'],
                           'likes': photo_x['likes']['count'],
                           'size': size_x,
                           'url': str(url_х)
                           })
        return list_x

# ----------------------
with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()
with open('token_y.txt', 'r') as file_object:
    token_y = file_object.read().strip()
# ----------------------
target_user = '3711648'
target_album = 'profile'  # варианты: profile , saved, wall
count_photos = 7
# ----------------------
# token_y = input(f'\nвведите токен Яндекс.Диска: ')
# target_user = input(f'\nвведите id пользователя vk: ')
# target_album = input(f'\nвыберите фото-альбом (profile , saved, wall): ')
# count_photos = int(input(f'\nвыберите количество фотографий: '))
# ----------------------
folder_name = 'VK' + str(target_user)
data_file_name = 'info.txt'
file_path = '/' + folder_name + '/' + data_file_name
# ----------------------
vk = VkUser(token_vk, target_user, target_album, count_photos)
vk_plist = vk.get_photo_list()
# ----------------------
yadisk = YaDisk(token_y)
print(f'создаем на Yandex Диске \nдиректорию для хранения фотографий\n[{folder_name}] \n')
yadisk.create_folder(folder_name)
# ----------------------
info_list = []
for n in vk_plist:
    id_n = n['photo_id']
    likes_n = n['likes']
    size_n = n['size']
    url_n = n['url']
    name_n = 'id' + str(id_n) + '_(' + str(likes_n) + '-likes)' + '.jpg'
    path_n = '/' + folder_name + '/' + name_n
    print('сохраняем фото', name_n)
    yadisk.upload_url_to_disk(path_n, url_n)
    info_list.append({'file_name': name_n, 'size': str(size_n)})

# ----------------------
print(f'\nформируем файл отчета', data_file_name)
with open(data_file_name, "w") as info_x:
    info_x.write(json.dumps(info_list))
    info_x.close()
print(f'\nдобавляем файл на Yandex Диск')
yadisk.upload_file_to_disk(file_path, data_file_name)
print(f'\nвсе файлы записаны')