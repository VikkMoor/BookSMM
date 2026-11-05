import requests


class VKPublisher:
    TIMEOUT = 30

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

        try:
            http_response = requests.get(
                url,
                params=params,
                timeout=self.TIMEOUT
            )
            http_response.raise_for_status()

            response = http_response.json()

        except requests.exceptions.Timeout:
            raise Exception("VK: превышено время ожидания при получении сервера загрузки фото.")
        except requests.exceptions.ConnectionError:
            raise Exception("VK: не удалось подключиться к серверу для получения адреса загрузки фото.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"VK: сервер вернул HTTP-ошибку при получении адреса загрузки фото: {e}")
        except requests.exceptions.JSONDecodeError:
            raise Exception("VK: сервер вернул некорректный ответ при получении адреса загрузки фото.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"VK: ошибка при получении сервера загрузки фото: {e}")

        if not isinstance(response, dict):
            raise Exception("VK: получен ответ неожиданного формата при запросе сервера загрузки фото.")

        if "error" in response:
            error_message = response["error"].get("error_msg", "Неизвестная ошибка VK API.")
            raise Exception(f"VK: {error_message}")

        if (
                not isinstance(response.get("response"), dict)
                or not response["response"].get("upload_url")
        ):
            raise Exception("VK: в ответе отсутствует адрес сервера загрузки фотографии.")

        upload_url = response["response"]["upload_url"]

        try:
            image_file = open(image_path, "rb")
        except FileNotFoundError:
            raise Exception(f"VK: файл изображения не найден: {image_path}")
        except OSError as e:
            raise Exception(f"VK: не удалось открыть файл изображения: {e}")

        with image_file:
            try:
                upload_http_response = requests.post(
                    upload_url,
                    files={"photo": image_file},
                    timeout=self.TIMEOUT
                )
                upload_http_response.raise_for_status()

                upload_response = upload_http_response.json()

            except requests.exceptions.Timeout:
                raise Exception("VK: превышено время ожидания при загрузке изображения.")
            except requests.exceptions.ConnectionError:
                raise Exception("VK: не удалось подключиться к серверу загрузки изображения.")
            except requests.exceptions.HTTPError as e:
                raise Exception(f"VK: сервер загрузки вернул HTTP-ошибку: {e}")
            except requests.exceptions.JSONDecodeError:
                raise Exception("VK: сервер загрузки вернул некорректный ответ.")
            except requests.exceptions.RequestException as e:
                raise Exception(f"VK: ошибка при загрузке изображения: {e}")

            print("Ответ сервера загрузки:")
            print("Server:", upload_response.get("server"))
            print("Hash:", upload_response.get("hash"))
            print("Photo:", repr(upload_response.get("photo")))
            print("Тип Photo:", type(upload_response.get("photo")))

        if not isinstance(upload_response, dict):
            raise Exception("VK: сервер загрузки вернул ответ неожиданного формата.")

        if "error" in upload_response:
            raise Exception(f"VK: ошибка загрузки изображения: {upload_response['error']}")

        if not all(upload_response.get(key) for key in ("server", "hash", "photo")):
            raise Exception("VK: сервер загрузки не вернул необходимые данные изображения.")

        save_url = "https://api.vk.com/method/photos.saveWallPhoto"

        save_params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "group_id": self.group_id,
            "server": upload_response["server"],
            "hash": upload_response["hash"],
            "photo": upload_response["photo"]
        }

        try:
            save_http_response = requests.post(
                save_url,
                params=save_params,
                timeout=self.TIMEOUT
            )
            save_http_response.raise_for_status()

            save_response = save_http_response.json()

        except requests.exceptions.Timeout:
            raise Exception("VK: превышено время ожидания при сохранении фотографии.")
        except requests.exceptions.ConnectionError:
            raise Exception("VK: не удалось подключиться к VK API для сохранения фотографии.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"VK: сервер вернул HTTP-ошибку при сохранении фотографии: {e}")
        except requests.exceptions.JSONDecodeError:
            raise Exception("VK: получен некорректный ответ при сохранении фотографии.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"VK: ошибка при сохранении фотографии: {e}")

        if not isinstance(save_response, dict):
            raise Exception("VK: получен ответ неожиданного формата при сохранении фотографии.")

        if "error" in save_response:
            error_message = save_response["error"].get("error_msg", "Неизвестная ошибка VK API.")
            raise Exception(f"VK: {error_message}")

        if (
                not isinstance(save_response.get("response"), list)
                or not save_response["response"]
        ):
            raise Exception("VK: в ответе отсутствуют данные сохранённой фотографии.")

        photo = save_response["response"][0]

        if not isinstance(photo, dict) or not photo.get("owner_id") or not photo.get("id"):
            raise Exception("VK: получены неполные данные сохранённой фотографии.")

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

        try:
            http_response = requests.post(
                url,
                params=params,
                timeout=self.TIMEOUT
            )
            http_response.raise_for_status()

            response = http_response.json()

        except requests.exceptions.Timeout:
            raise Exception("VK: превышено время ожидания при публикации поста.")
        except requests.exceptions.ConnectionError:
            raise Exception("VK: не удалось подключиться к VK API для публикации поста.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"VK: сервер вернул HTTP-ошибку при публикации поста: {e}")
        except requests.exceptions.JSONDecodeError:
            raise Exception("VK: получен некорректный ответ при публикации поста.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"VK: ошибка при публикации поста: {e}")

        if not isinstance(response, dict):
            raise Exception("VK: получен ответ неожиданного формата при публикации поста.")

        if "error" in response:
            error_message = response["error"].get("error_msg", "Неизвестная ошибка VK API.")
            raise Exception(f"VK: {error_message}")

        if "response" not in response:
            raise Exception("VK: в ответе отсутствует результат публикации поста.")

        return response["response"]
