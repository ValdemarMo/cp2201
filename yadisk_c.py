import requests

class YaDisk:

    def __init__(self, token):
        self.token = token
          
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)}

    def yd_upload_url(self):
        return 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def yd_resources_url(self):
        return 'https://cloud-api.yandex.net/v1/disk/resources'
       
    def create_folder(self, disk_path):
        upload_url = self.yd_resources_url()
        headers = self.get_headers()
        params = {
            "path": disk_path,
            "overwrite": "true"}
        requests.put(upload_url, headers=headers, params=params)

    def upload_url_to_disk(self, disk_file_path, file_url):
        upload_url = self.yd_upload_url()
        headers = self.get_headers()
        params = {
            'url': file_url,
            'path': disk_file_path,
            'disable_redirects': 'true'}
        requests.post(upload_url, headers=headers, params=params)

    def upload_file_to_disk(self, disk_path, filename):
        upload_url = self.yd_upload_url()
        headers = self.get_headers()
        params = {
            "path": disk_path,
            "overwrite": "true"}
        href = requests.get(upload_url, headers=headers, 
                            params=params).json().get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")