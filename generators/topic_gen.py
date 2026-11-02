from openai import OpenAI


class TopicGenerator:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def generate_topic(self):
        response = self.client.responses.create(
            model="gpt-5.4-mini",
            instructions=(
                "Ты SMM-специалист книжного сообщества. "
                "Придумывай интересные темы для публикаций о книгах и литературе. "
                "Тема должна быть конкретной, интересной и подходить для поста "
                "в социальной сети. "
                "Не повторяй банальные формулировки. "
                "Отвечай только одной готовой темой без пояснений."
            ),
            input="Придумай одну тему для следующего поста книжного сообщества."
        )

        return response.output_text