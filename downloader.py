import os
import random
import subprocess
import logging
from dotenv import load_dotenv
from pytubefix import YouTube
from pytubefix.exceptions import PytubeFixError

# Загрузка переменных окружения
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class VideoDownloader:
    """
    Класс для скачивания видео с YouTube.
    Отвечает за загрузку видео в максимальном качестве.
    """

    def __init__(self):
        # Загрузка прокси из .env файла
        proxies_raw = os.getenv("PROXIES", "")
        if not proxies_raw:
            logging.warning("Прокси не настроены. Запросы будут выполняться без прокси.")
            self.proxies = []
        else:
            # Разделяем прокси по запятым и добавляем http/https
            self.proxies = [
                {"http": f"http://{proxy}", "https": f"https://{proxy}"}
                for proxy in proxies_raw.split(",") if proxy.strip()
            ]
            logging.info(f"Настроено {len(self.proxies)} прокси.")

        # Загрузка visitorData и PoToken
        self.visitor_data, self.po_token = self.load_po_token_data()

    def load_po_token_data(self):
        """
        Загружает visitorData и PoToken из файла или запрашивает их у пользователя.
        :return: Кортеж (visitorData, PoToken).
        """
        po_token_file = "po_token_cache.txt"
        if os.path.exists(po_token_file):
            with open(po_token_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) == 2:
                    visitor_data = lines[0].strip()
                    po_token = lines[1].strip()
                    logging.info("Загружены visitorData и PoToken из кэша.")
                    return visitor_data, po_token

        # Если файл отсутствует или данные некорректны, запрашиваем их у пользователя
        logging.warning("Файл с visitorData и PoToken не найден или поврежден. Запрашиваем новые данные.")
        visitor_data = input("Введите ваш visitorData: ").strip()
        po_token = input("Введите ваш PoToken: ").strip()

        # Сохраняем данные в файл
        with open(po_token_file, "w", encoding="utf-8") as file:
            file.write(f"{visitor_data}\n{po_token}")
        logging.info("visitorData и PoToken сохранены в файл для последующего использования.")

        return visitor_data, po_token

    def get_random_proxy(self):
        """
        Возвращает случайный прокси из списка или None, если прокси нет.
        :return: Словарь с прокси или None.
        """
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def create_youtube_object(self, url):
        """
        Создает объект YouTube с использованием прокси и PoToken.
        :param url: URL видео на YouTube.
        :return: Объект YouTube.
        """
        proxy = self.get_random_proxy()
        try:
            yt = YouTube(
                url,
                proxies=proxy,
                use_po_token=True,
                po_token_verifier=self.custom_po_token_verifier
            )
            return yt
        except Exception as e:
            logging.error(f"Ошибка при создании объекта YouTube для URL {url}: {e}")
            return None

    def custom_po_token_verifier(self):
        """
        Верификатор для получения visitorData и PoToken.
        :return: Кортеж (visitorData, PoToken).
        """
        return self.visitor_data, self.po_token

    def download_video_with_audio(self, yt, output_path="videos"):
        """
        Скачивает видео и аудио по отдельности, затем объединяет их.
        :param yt: Объект YouTube.
        :param output_path: Путь для сохранения видео.
        :return: Путь к объединенному файлу или None в случае ошибки.
        """
        try:
            # Создаем папку для сохранения файлов
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Выбираем видео-поток с максимальным качеством
            video_stream = yt.streams.filter(adaptive=True, only_video=True).order_by("resolution").desc().first()
            if not video_stream:
                logging.error("Не удалось найти видео-поток.")
                return None

            # Выбираем аудио-поток с максимальным битрейтом
            audio_stream = yt.streams.filter(adaptive=True, only_audio=True).order_by("abr").desc().first()
            if not audio_stream:
                logging.error("Не удалось найти аудио-поток.")
                return None

            # Скачиваем видео и аудио
            video_path = video_stream.download(output_path=output_path, filename=f"{yt.video_id}_video.mp4")
            audio_path = audio_stream.download(output_path=output_path, filename=f"{yt.video_id}_audio.mp4")

            # Объединяем видео и аудио с помощью ffmpeg
            output_file = os.path.join(output_path, f"{yt.video_id}.mp4")
            subprocess.run([
                "ffmpeg", "-i", video_path, "-i", audio_path,
                "-c:v", "copy", "-c:a", "aac", output_file
            ])

            # Удаляем временные файлы
            os.remove(video_path)
            os.remove(audio_path)

            logging.info(f"Видео успешно объединено: {output_file}")
            return output_file

        except Exception as e:
            logging.error(f"Произошла ошибка при скачивании видео для URL {yt.watch_url}: {e}")
        return None
    