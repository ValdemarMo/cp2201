import requests

class VkUser:

    def __init__(self, token):
        self.token = token

    def get_user_id(self, target_user):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': target_user,
            'fields': 'screen_name',
            'access_token': self.token,
            'v': '5.131'
        }      
        res = requests.get(url, params=params)
        if not res.json()['response']:
            print(f'пользователь не обнаружен')
            return None    
        if res.json()['response'][0]['is_closed'] != False:
            print(f'\nпользователь закрыл профиль')
            return None
        target_user = res.json()['response'][0]['id']
        return target_user
        
    def get_photo_list(self, target_album, count_photos, target_user_id):
        print(f'\nзапрашиваем VK список фотографий в альбоме')
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': target_user_id,
            'album_id': target_album,
            'count': count_photos,
            'rev': 1,
            'extended': 1,
            'photo_sizes': 0,
            'access_token': self.token,
            'v': '5.131'}      
        res = requests.get(url, params=params)
        real_count = res.json()['response']['count']
        photo_list = res.json()['response']['items']
        if real_count < count_photos:
            print(f'\nв альбоме обнаруженно только {real_count} фото')
        print('\nформируем список фотографий лучшего качества\n')
        list_x = []
        for photo_x in photo_list:
            max_size = 0
            for photo_size in photo_x['sizes']:
                if max_size < int(photo_size['height']):
                    max_size = photo_size['height']
                    size_x = photo_size['type']
                    url_х = photo_size['url']
            list_x.append({
                'photo_id': photo_x['id'],
                'date': photo_x['date'],
                'likes': photo_x['likes']['count'],
                'size': size_x,
                'url': str(url_х)
            })
        return list_x