import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
vk_group_id = os.getenv("VK_GROUP_ID")
vk_api_key = os.getenv("VK_API_KEY")
