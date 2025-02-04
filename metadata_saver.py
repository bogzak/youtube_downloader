import os
import csv
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MetadataSaver:
    """
    Класс для сохранения метаданных видео в CSV файл.
    Отвечает за запись данных о видео в файл.
    """

    def __init__(self, file_name="files/video_metadata.csv"):
        self.file_name = file_name

    def save(self, video_id, title, description, author, publish_date):
        """
        Сохраняет метаданные видео в CSV файл.
        :param video_id: ID видео.
        :param title: Название видео.
        :param description: Описание видео.
        :param author: Автор видео.
        :param publish_date: Дата публикации видео.
        """
        file_exists = os.path.isfile(self.file_name)

        try:
            with open(self.file_name, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow(["Video ID", "Title", "Description", "Author", "Publish Date"])

                writer.writerow([video_id, title, description, author, publish_date])

            logging.info("Метаданные успешно сохранены в CSV файл.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении метаданных для видео {video_id}: {e}")
