import os
import csv
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def read_video_urls_from_csv(file_path):
    """
    Читает список URL видео из CSV файла.
    :param file_path: Путь к CSV файлу.
    :return: Список URL видео.
    """
    try:
        if not os.path.exists(file_path):
            logging.error(f"Файл {file_path} не найден.")
            return []

        video_urls = []
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                url = row.get("url")
                if url:
                    video_urls.append(url.strip())

        logging.info(f"Прочитано {len(video_urls)} URL из файла {file_path}.")
        return video_urls

    except Exception as e:
        logging.error(f"Ошибка при чтении CSV файла {file_path}: {e}")
        return []
    