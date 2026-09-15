from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher
import config as conf


# 1. Генерируем изображение через OpenAI
print("1. Генерируем изображение...")

img_gen = ImageGenerator(conf.openai_key)

image_path = img_gen.generate_image(
    "Красивое атмосферное изображение книг для публикации в книжном сообществе"
)

print("Изображение создано:", image_path)


# 2. Подключаем VK
print("2. Подключаемся к VK...")

vk_pub = VKPublisher(
    conf.vk_api_key,
    conf.vk_group_id
)


# 3. Загружаем изображение в VK
print("3. Загружаем изображение в VK...")

attachment = vk_pub.upload_photo(image_path)

print("Attachment:", attachment)


# 4. Публикуем пост
print("4. Публикуем пост...")

result = vk_pub.publish_post(
    "Новый пост BookSMM с изображением, сгенерированным с помощью ИИ",
    attachment
)

print("Пост опубликован:", result)