
import requests
import datetime


class VKStats:
    TIMEOUT = 30

    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def get_stats(self, start_date, end_date):
        url = "https://api.vk.com/method/stats.get"

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        end_date = end_date.replace(
            hour=23,
            minute=59,
            second=59,
            tzinfo=datetime.timezone.utc
        )

        start_unix_time = int(start_date.timestamp())
        end_unix_time = int(end_date.timestamp())

        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "group_id": self.group_id,
            "timestamp_from": start_unix_time,
            "timestamp_to": end_unix_time
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
            raise Exception(
                "VK: превышено время ожидания при получении статистики сообщества."
            )
        except requests.exceptions.ConnectionError:
            raise Exception(
                "VK: не удалось подключиться к серверу при получении статистики сообщества."
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"VK: HTTP-ошибка при получении статистики сообщества: {e}"
            )
        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "VK: сервер вернул некорректный ответ при получении статистики сообщества."
            )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"VK: ошибка при получении статистики сообщества: {e}"
            )

        if not isinstance(response, dict):
            raise Exception(
                "VK: получен ответ в неожиданном формате при получении статистики сообщества."
            )

        if "error" in response:
            error = response["error"]
            error_message = (
                error.get("error_msg", "неизвестная ошибка")
                if isinstance(error, dict)
                else "неизвестная ошибка"
            )
            raise Exception(f"VK API: {error_message}")

        if "response" not in response:
            raise Exception(
                "VK: в ответе отсутствует поле со статистикой сообщества."
            )

        if not isinstance(response["response"], list):
            raise Exception(
                "VK: данные статистики сообщества имеют неожиданный формат."
            )

        return response["response"]

    def get_followers(self):
        url = "https://api.vk.com/method/groups.getMembers"

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
            raise Exception(
                "VK: превышено время ожидания при получении количества подписчиков."
            )
        except requests.exceptions.ConnectionError:
            raise Exception(
                "VK: не удалось подключиться к серверу при получении количества подписчиков."
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"VK: HTTP-ошибка при получении количества подписчиков: {e}"
            )
        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "VK: сервер вернул некорректный ответ при получении количества подписчиков."
            )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"VK: ошибка при получении количества подписчиков: {e}"
            )

        if not isinstance(response, dict):
            raise Exception(
                "VK: получен ответ в неожиданном формате при получении количества подписчиков."
            )

        if "error" in response:
            error = response["error"]
            error_message = (
                error.get("error_msg", "неизвестная ошибка")
                if isinstance(error, dict)
                else "неизвестная ошибка"
            )
            raise Exception(f"VK API: {error_message}")

        if "response" not in response:
            raise Exception(
                "VK: в ответе отсутствуют данные о подписчиках."
            )

        if (
            not isinstance(response["response"], dict)
            or not isinstance(response["response"].get("count"), int)
        ):
            raise Exception(
                "VK: в ответе отсутствует корректное количество подписчиков."
            )

        return response["response"]["count"]

    def get_posts(self, count=10):
        if not isinstance(count, int) or not 1 <= count <= 100:
            raise ValueError(
                "Количество публикаций должно быть от 1 до 100."
            )

        url = "https://api.vk.com/method/wall.get"

        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "owner_id": f"-{self.group_id}",
            "count": count
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
            raise Exception(
                "VK: превышено время ожидания при получении публикаций."
            )
        except requests.exceptions.ConnectionError:
            raise Exception(
                "VK: не удалось подключиться к серверу при получении публикаций."
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"VK: HTTP-ошибка при получении публикаций: {e}"
            )
        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "VK: сервер вернул некорректный ответ при получении публикаций."
            )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"VK: ошибка при получении публикаций: {e}"
            )

        if not isinstance(response, dict):
            raise Exception(
                "VK: получен ответ в неожиданном формате при получении публикаций."
            )

        if "error" in response:
            error = response["error"]
            error_message = (
                error.get("error_msg", "неизвестная ошибка")
                if isinstance(error, dict)
                else "неизвестная ошибка"
            )
            raise Exception(f"VK API: {error_message}")

        if "response" not in response:
            raise Exception(
                "VK: в ответе отсутствуют данные о публикациях."
            )

        if (
            not isinstance(response["response"], dict)
            or "items" not in response["response"]
        ):
            raise Exception(
                "VK: в ответе отсутствует корректный список публикаций."
            )

        if not isinstance(response["response"]["items"], list):
            raise Exception(
                "VK: список публикаций имеет неожиданный формат."
            )

        return response["response"]["items"]
