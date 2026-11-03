import requests


class VKPublisher:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def upload_photo(self, image_path):
        url = "https://api.vk.com/method/photos.getWallUploadServer"

        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "group_id": self.group_id
        }

        response = requests.get(url, params=params).json()

        if "error" in response:
            raise Exception(response["error"]["error_msg"])

        upload_url = response["response"]["upload_url"]

        with open(image_path, "rb") as image_file:
            upload_response = requests.post(
                upload_url,
                files={"photo": image_file}
            ).json()

            print("Ответ сервера загрузки:")
            print("Server:", upload_response.get("server"))
            print("Hash:", upload_response.get("hash"))
            print("Photo:", repr(upload_response.get("photo")))
            print("Тип Photo:", type(upload_response.get("photo")))

        if "error" in upload_response:
            raise Exception(upload_response["error"])

        save_url = "https://api.vk.com/method/photos.saveWallPhoto"

        save_params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "group_id": self.group_id,
            "server": upload_response["server"],
            "hash": upload_response["hash"],
            "photo": upload_response["photo"]
        }

        save_response = requests.post(
            save_url,
            params=save_params
        ).json()

        if "error" in save_response:
            raise Exception(save_response["error"]["error_msg"])

        photo = save_response["response"][0]

        return f"photo{photo['owner_id']}_{photo['id']}"

    def publish_post(self, content, attachment=None):
        url = "https://api.vk.com/method/wall.post"

        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "owner_id": f"-{self.group_id}",
            "from_group": 1,
            "message": content
        }

        if attachment:
            params["attachments"] = attachment

        response = requests.post(
            url,
            params=params
        ).json()

        if "error" in response:
            raise Exception(response["error"]["error_msg"])

        return response["response"]