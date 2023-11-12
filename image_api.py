import base64
import requests
import os
from json import JSONDecodeError


# OpenAI API Key for the direct requests API calls
api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def submit_image(prompt, image_path):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 700
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    try:
        return response.json()
    except JSONDecodeError:
        print(response.text)
        return None
