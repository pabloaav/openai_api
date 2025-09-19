#!/usr/bin/env python3
import os
from dotenv import load_dotenv

from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_completion(messages: list[dict]):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo más económico
            messages=messages,  # Mensajes del usuario
            max_tokens=100,  # Tokens máximos
            temperature=0.7,  # Temperatura
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


messages = list(
    [
        {
            "role": "system",
            "content": "Eres un asistente experto de la app SysNetVision presentate como tal.",
        },
        {"role": "user", "content": "Hola como estas?."},
    ]
)
if __name__ == "__main__":
    print(chat_completion(messages))
