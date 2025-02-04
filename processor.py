import logging
import time

from concurrent.futures import ThreadPoolExecutor


class YouTubeVideoProcessor:
    """
    Класс для обработки видео с YouTube.
    Объединяет логику скачивания видео и сохранения метаданных.
    """

    def __init__(self, downloader, metadata_saver):
        self.downloader = downloader
        self.metadata_saver = metadata_saver

    def process_video(self, url):
        """
        Обрабатывает видео: скачивает его и сохраняет метаданные.
        :param url: URL видео на YouTube.
        """
        try:
            # Создаем объект YouTube один раз
            yt = self.downloader.create_youtube_object(url)
            if not yt:
                logging.error(f"Не удалось создать объект YouTube для URL {url}. Пропускаем видео.")
                return

            # Получаем метаданные видео
            video_id = yt.video_id
            title = yt.title
            description = yt.description
            author = yt.author
            publish_date = yt.publish_date

            logging.info(f"Начинаем обработку видео: {title}")

            # Скачиваем видео с аудио
            video_path = self.downloader.download_video_with_audio(yt)
            if video_path:
                # Сохраняем метаданные
                self.metadata_saver.save(video_id, title, description, author, publish_date)

            # Добавляем задержку между запросами
            time.sleep(5)

        except Exception as e:
            logging.error(f"Произошла ошибка при обработке видео для URL {url}: {e}")

    def process_video_list(self, video_urls, max_workers=5):
        """
        Обрабатывает список видео в многопоточном режиме.
        :param video_urls: Список URL видео.
        :param max_workers: Максимальное количество потоков.
        """
        total_videos = len(video_urls)
        logging.info(f"Начинаем обработку {total_videos} видео в многопоточном режиме.")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.process_video, url) for url in video_urls]
            for future in futures:
                try:
                    future.result()  # Ждем завершения всех задач
                except Exception as e:
                    logging.error(f"Ошибка при обработке задачи: {e}")


