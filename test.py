from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
import config as conf
from social_publishers.vk_publisher import VKPublisher


print("1. Генерируем текст поста...")

generator = PostGenerator(
    openai_key=conf.openai_key,
    tone="дружелюбный",
    topic="Почему стоит перечитать любимую книгу во взрослом возрасте"
)

post = generator.generate_post()

print("Текст поста:")
print(post)


print("\n2. Генерируем описание изображения...")

image_description = generator.generate_post_image_description()

print("Описание изображения:")
print(image_description)


print("\n3. Генерируем изображение...")

img_gen = ImageGenerator(conf.openai_key)

image_path = img_gen.generate_image(image_description)

print("Изображение создано:", image_path)


print("\n4. Подключаемся к VK...")

vk_pub = VKPublisher(
    conf.vk_api_key,
    conf.vk_group_id
)


print("5. Загружаем изображение в VK...")

attachment = vk_pub.upload_photo(image_path)

print("Attachment:", attachment)


print("6. Публикуем пост...")

result = vk_pub.publish_post(
    post,
    attachment
)

print("Пост опубликован:", result)