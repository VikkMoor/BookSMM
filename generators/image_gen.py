from openai import OpenAI
import base64


class ImageGenerator:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def generate_image(self, prompt):
        response = self.client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size="1024x1024",
            quality="low",
        )

        image_data = base64.b64decode(response.data[0].b64_json)

        image_path = "generated_image.png"

        with open(image_path, "wb") as image_file:
            image_file.write(image_data)

        print("Размер изображения:", len(image_data), "байт")

        return image_path