from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(".env.example")

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

YOUR_SITE_URL = os.getenv("YOUR_SITE_URL")
YOUR_SITE_NAME = os.getenv("YOUR_SITE_NAME")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"Проанализируйте следующий текст и определите тон общения (положительный, нейтральный или негативный). Дайте рекомендации по улучшению общения. Если текст слишком короткий или неинформативный, укажите это в рекомендациях.\n\nТекст: {text}\n\nОтветьте строго в формате:\nТон: [оценка]\nРекомендации: [рекомендации]\n\nНе добавляйте лишних пробелов в начале строк и никакого дополнительного текста после рекомендаций."

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": YOUR_SITE_URL,
                "X-Title": YOUR_SITE_NAME,
            },
            extra_body={},
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        response_text = completion.choices[0].message.content
        print("Ответ модели:", response_text)

        lines = [line.strip() for line in response_text.split('\n') if line.strip()]
        
        tone = None
        recommendations = None
        for line in lines:
            if line.startswith("Тон:"):
                tone = line.split(":", 1)[1].strip()
            elif line.startswith("Рекомендации:"):
                recommendations = line.split(":", 1)[1].strip()

        if tone and recommendations:
            return jsonify({"tone": tone, "recommendations": recommendations})
        else:
            return jsonify({
                "error": "Модель не вернула ожидаемый формат",
                "raw_response": response_text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)