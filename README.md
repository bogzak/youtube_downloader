# YouTube Video Downloader

A Python-based tool to download videos from YouTube, extract metadata, and save the information into a CSV file. The program supports proxies and PoToken for legitimate requests to the YouTube API.

---

## Features

- **Download Videos**: Download video and audio streams separately, then merge them into a single file using `ffmpeg`.
- **Extract Metadata**: Save video metadata (ID, title, description, author, publish date) into a CSV file.
- **Proxy Support**: Use proxies to bypass IP restrictions and prevent blocking.
- **PoToken Integration**: Use `visitorData` and `PoToken` for legitimate requests to the YouTube API.
- **Sequential Processing**: Process videos one by one with a delay between requests to avoid bot detection.
- **CSV Input/Output**:
  - Read video URLs from a CSV file (`video_urls.csv`).
  - Save metadata into another CSV file (`video_metadata.csv`).

---

## Requirements

Before running the program, ensure you have the following installed:

1. **Python 3.8+**
2. **FFmpeg**: Required for merging video and audio streams.
   - Install FFmpeg: [FFmpeg Download](https://ffmpeg.org/download.html)
3. **Dependencies**:
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
4. **Environment Variables**:
   - Create a `.env` file in the project root and add your proxies:
     ```
     PROXIES=http://user1:pass1@proxy1:port,http://user2:pass2@proxy2:port
     ```

---


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/youtube-downloader.git
   cd youtube-downloader
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:
    - Create a .env file in the project root and add your proxies (if needed):
    ```bash
    PROXIES=http://user1:pass1@proxy1:port,http://user2:pass2@proxy2:port
    ```
4. Prepare input files:
    - Create a video_urls.csv file with the following format:
    ```bash
    url
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    https://www.youtube.com/watch?v=another_video_id
    ```

---

## Usage

1. Run the program:
   ```bash
   python main.py
   ```
2. The program will:
    - Read video URLs from video_urls.csv.
    - Download each video and merge video/audio streams.
    - Save metadata into video_metadata.csv.
3. Output:
    - Downloaded videos will be saved in the videos/ folder.
    - Metadata (video ID, title, description, author, publish date) will be saved in video_metadata.csv.
4. Notes:
    - If the program requires a PoToken, it will prompt you to enter visitorData and PoToken. These values will be cached in po_token_cache.txt for future use.
    - A delay is added between requests to avoid bot detection.

---

## Project Structure

```
project/
│
├── main.py # Main entry point for the program
├── downloader.py # Handles video downloading
├── metadata_saver.py # Saves video metadata into a CSV file
├── processor.py # Processes videos sequentially
├── utils.py # Utility functions (e.g., reading CSV files)
├── .env # Environment variables (proxies)
├── video_urls.csv # Input file with video URLs
└── video_metadata.csv # Output file with video metadata
```

- **main.py**: The main script to run the program.
- **downloader.py**: Contains logic for downloading videos and handling proxies.
- **metadata_saver.py**: Handles saving video metadata into a CSV file.
- **processor.py**: Manages the sequential processing of videos.
- **utils.py**: Provides utility functions, such as reading URLs from a CSV file.
- **.env**: Stores environment variables like proxies.
- **video_urls.csv**: Input file containing a list of YouTube video URLs.
- **video_metadata.csv**: Output file where video metadata is saved.

---

## Configuration

### `.env` File
- Add your proxies to the `.env` file:
    ```
    PROXIES=http://user1:pass1@proxy1:port,http://user2:pass2@proxy2:port
    ```
- If no proxies are provided, the program will run without them.
- Proxies are used to bypass IP restrictions and prevent blocking by YouTube.

### `video_urls.csv`
Provide a list of YouTube video URLs in the following format:
    ```
    url
    https://www.youtube.com/watch?v=dQw4w9WgXcQ
    https://www.youtube.com/watch?v=another_video_id
    ```
- Each line (except the header) should contain a valid YouTube video URL.
- The program reads this file to process the videos sequentially.

## PoToken Cache

- If the program requires a PoToken, it will prompt you to enter visitorData and PoToken.
- These values will be cached in po_token_cache.txt for future use, so you won't need to enter them again unless they expire.

---

## Contributing

Contributions are welcome! If you find a bug or want to add a feature, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
