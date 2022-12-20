import json
import vk_c
import yadisk_c

with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()
with open('token_y.txt', 'r') as file_object: 
    token_y = file_object.read().strip()

vk = vk_c.VkUser(token_vk)
target_user = 'none'

while target_user != True:
    target_user = input(f'\nвведите id или screen_name пользователя vk: ')
    target_user = vk.get_user_id(target_user)
    if target_user: break
    print(f'\nпопробуйте ещё раз')

target_album = 'profile'  # варианты: profile , saved, wall
# target_album = input(f'\nвыберите фото-альбом (profile , saved, wall): ')
count_photos = int(input(f'\nвыберите количество фотографий: '))

folder_name = 'VK' + str(target_user)
data_file_name = 'info.json'
file_path = '/' + folder_name + '/' + data_file_name

vk_plist = vk.get_photo_list(target_album, count_photos, target_user)

yadisk = yadisk_c.YaDisk(token_y)
print(f'создаем на Yandex Диске \nпапку для хранения фотографий\
    \n[{folder_name}] \n')
yadisk.create_folder(folder_name)

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

print(f'\nформируем файл отчета', data_file_name)
with open(data_file_name, "w") as info_x:
    info_x.write(json.dumps(info_list))
    info_x.close()

print(f'\nдобавляем файл на Yandex Диск')
yadisk.upload_file_to_disk(file_path, data_file_name)
print(f'\nвсе файлы записаны')