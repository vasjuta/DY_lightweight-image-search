# downloader/download.py
import os
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor
import logging
import time
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageDownloader:
    def __init__(self, output_dir, max_workers=2):
        self.output_dir = output_dir
        self.max_workers = max_workers
        os.makedirs(output_dir, exist_ok=True)

        # Setup session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def is_valid_image(self, response):
        """Check if the response contains a valid image"""
        content_type = response.headers.get('content-type', '')
        return (
                content_type.startswith('image/') and
                len(response.content) > 1000 and  # Minimum size check
                response.content[:8] not in [b'<!DOCTYPE', b'<html><t']  # Not HTML
        )

    def download_image(self, url):
        """Download a single image"""
        try:
            # Basic URL validation
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return None

            # Download with timeout
            response = self.session.get(url, timeout=10, stream=True)
            response.raise_for_status()

            if not self.is_valid_image(response):
                logger.warning(f"Invalid image: {url}")
                return None

            # Generate filename from content hash
            content = response.content
            file_hash = hashlib.md5(content).hexdigest()[:10]
            ext = os.path.splitext(url)[-1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                ext = '.jpg'

            filename = f"{file_hash}{ext}"
            filepath = os.path.join(self.output_dir, filename)

            # Save image
            with open(filepath, 'wb') as f:
                f.write(content)

            logger.info(f"Downloaded: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            return None

    def download_from_file(self, url_file):
        """Download all images from the URL file"""
        with open(url_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

        logger.info(f"Starting download of {len(urls)} images")

        # Download images using thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.download_image, url) for url in urls]

            # Process results as they complete
            for future in futures:
                try:
                    future.result(timeout=30)
                except Exception as e:
                    logger.error(f"Download failed: {str(e)}")


if __name__ == "__main__":
    downloader = ImageDownloader('/app/images')
    downloader.download_from_file('/app/image_urls.txt')