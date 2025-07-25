# Агент оценки звонков

Это минимальное приложение, которое анализирует текст телефонного разговора, оценивает тон общения (положительный, нейтральный или негативный) и предоставляет одну-две рекомендации по улучшению. Реализация выполнена на Python с использованием Flask, интегрирована с Telegram через N8N и использует модель Deepseek R1 0528 Qwen3 8B через OpenRouter API.

## Выбранная модель
- **Модель**: DeepSeek: Deepseek R1 0528 Qwen3 8B (free)
- **Источник**: [OpenRouter](https://openrouter.ai/deepseek/deepseek-r1-0528-qwen3-8b:free)
- **Причина выбора**: Бесплатная, доступна через API, поддерживает генерацию текста с инструкциями.

## Как запустить локально

### Требования
- Python 3.9+
- Docker (опционально)
- N8N (для интеграции с Telegram)
- API-ключ от OpenRouter

### Шаги
1. **Клонируйте репозиторий**:
   ```
   git clone <ссылка_на_репозиторий>
   cd <название_папки>
   ```

2. **Создайте виртуальное окружение и установите зависимости**:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения**:
   - Скопируйте `.env.example` в `.env`:
     ```
     cp .env.example .env
     ```
   - Отредактируйте `.env`, указав:
     - `OPENROUTER_API_KEY` — ваш API-ключ от OpenRouter (уже указан)
     - `YOUR_SITE_URL` — URL вашего сайта (например, http://localhost:5000)
     - `YOUR_SITE_NAME` — название сайта (например, "CallAgent")

4. **Запустите Flask-приложение**:
   ```
   python app.py
   ```
   Приложение будет доступно на `http://localhost:5000`.

5. **Настройка Ngrok**
   - Используйте `ngrok` для локального туннеля:
     ```
     ngrok http 5000
     ```

5. **Для интеграции с Telegram**:
   - Установите и запустите N8N (локально или на сервере).
   - Создайте "Workflow".
   - Загрузите файл "Text analysis AI.json" в рабочую область.
   - В нод Http Request измените URL на URL полученный в ngrok и добавьте в конце "/analyze" (URL + /analyze, например: https://1faf3a633ed5.ngrok-free.app/analyze).
   - Сохраните и активируйте workflow.

6. **Тестирование**:
   - Отправьте сообщение в Telegram, которое содержит расшифровку телефонного разговора.

### Запуск через Docker
1. Соберите образ:
   ```
   docker build -t call-agent .
   ```
2. Запустите контейнер:
   ```
   docker run -p 5000:5000 --env-file .env call-agent
   ```

## Архитектура
```mermaid
graph LR
    A[Telegram] --> B[N8N]
    B --> C[Flask API]
    C --> D[Deepseek R1 0528 Qwen3 8B free]
    D --> C
    C --> B
    B --> A
```
- **Telegram**: Пользователь отправляет текст разговора.
- **N8N**: Обрабатывает сообщение и отправляет запрос в API.
- **Flask API**: Принимает текст, отправляет в модель, возвращает JSON.
- **Deepseek R1 0528 Qwen3 8B (free)**: Анализирует текст и генерирует ответ.

## Ограничения
- Модель может неточно оценивать тон или давать общие рекомендации.
- Интеграция с Telegram зависит от стабильности N8N и ngrok (для локального тестирования).

## Что можно улучшить при большем времени
- Улучшить промпт для более точных ответов.
- Развернуть приложение на сервере (например, Heroku или AWS).
