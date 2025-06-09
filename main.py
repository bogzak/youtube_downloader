import os
from dotenv import load_dotenv
from downloader import VideoDownloader
from metadata_saver import MetadataSaver
from processor import YouTubeVideoProcessor
from utils import read_video_urls_from_csv


# Загрузка переменных окружения из .env файла
load_dotenv()


def main():
    # Инициализация компонентов
    downloader = VideoDownloader()
    metadata_saver = MetadataSaver()
    processor = YouTubeVideoProcessor(downloader, metadata_saver)

    # Путь к CSV файлу с URL видео
    csv_file_path = "files/video_urls.csv"

    # Чтение списка URL видео из CSV файла
    video_urls = read_video_urls_from_csv(csv_file_path)

    if not video_urls:
        print("Список URL видео пуст. Проверьте CSV файл.")
        return

    # Запуск массовой обработки видео с многопоточностью
    # processor.process_video_list(video_urls, max_workers=5)

    # Запуск массовой обработки видео
    for index, url in enumerate(video_urls, start=1):
        print(f"Обработка видео {index}/{len(video_urls)}: {url}")
        processor.process_video(url)


if __name__ == "__main__":
    main()
