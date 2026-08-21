from openai import OpenAI

class PostGenerator:
    def __init__(self, openai_key, tone, topic):
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self):
        response = self.client.responses.create(
            model="gpt-5.4-mini",
            instructions=(
                "Ты SMM-специалист книжного сообщества. "
                "Создавай интересные и естественные посты о книгах и литературе. "
                "Текст должен быть дружелюбным, увлекательным и подходить. "
                "для публикации в социальной сети. "
                "Отвечай только готовым текстом поста. "
                "Не добавляй пояснения, вступления и предложения создать дополнительные варианты."
            ),
            input=f"Сгенерируй пост на тему: {self.topic}. "
                  f"Используй тон: {self.tone}."
        )

        return response.output_text

    def generate_post_image_description(self):
        response = self.client.responses.create(
            model="gpt-5.4-mini",
            instructions=(
                "Ты специалист по созданию промптов для генерации изображений. "
                "Создай подробное визуальное описание изображения для книжного "
                "сообщества. Изображение должно соответствовать теме поста, "
                "быть атмосферным и подходить для публикации в социальной сети. "
                "Отвечай только готовым описанием изображения, без пояснений."
            ),
            input=f"Создай описание изображения для поста на тему: {self.topic}."
        )

        return response.output_text