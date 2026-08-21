from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
import config as conf

post_gen = PostGenerator(
    conf.openai_key,
    tone="дружелюбный и увлекательный",
    topic="5 книг, которые стоит прочитать этим летом"
)

content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

print(content)
print(img_desc)

img_gen = ImageGenerator(conf.openai_key)
image_path = img_gen.generate_image(img_desc)

print(image_path)