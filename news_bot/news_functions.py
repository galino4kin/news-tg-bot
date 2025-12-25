from logger_config import logger
from aiogram import types 

async def show_top_news(message: types.Message, current_topic: str, gnews_client):
    await message.answer(f"🔍 Ищу новости по теме: «{current_topic}»")
    try:
        news = gnews_client.get_news(current_topic, max_results=5)
        if not news:
            await message.answer("Новости не найдены.")
            return

        response = f"Топ новостей по теме «{current_topic}»:\n\n"
        for i, article in enumerate(news, 1):
            response += (
                f"{i}. {article.get('title', 'Без заголовка')}\n"
                f"{article.get('url', '')}\n\n"
            )

        await message.answer(response, disable_web_page_preview=True)

    except Exception:
        logger.exception("Ошибка при получении новостей")
        await message.answer("Ошибка при получении новостей.")

async def show_summary_sentiment(message: types.Message, current_topic: str, gnews_client, nlp_service):
    await message.answer(f"📝 Анализирую тему: «{current_topic}»")
    try:
        news = gnews_client.get_news(current_topic, max_results=5)
        if not news:
            await message.answer("Недостаточно данных")
            return

        text = nlp_service.prepare_news_text(news, max_articles=3)
        summary = nlp_service.summarize_text(
            text=text,
            topic=current_topic,
            n=3,
            max_tokens=200
        )

        sentiment = nlp_service.sent_analysis(text).get("sentiment", "Не определён")

        await message.answer(
            f"Краткая выжимка:\n{summary}\n\n"
            f"Тональность: {sentiment}"
        )

    except Exception:
        logger.exception("Ошибка анализа")
        await message.answer("Ошибка при анализе новостей.")