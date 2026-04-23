import os
import requests
import re
import mimetypes
from typing import Callable, Optional

class DownloaderService:
    def __init__(self):
        self.timeout = 30

    def get_filename_from_cd(self, content_disposition: str) -> Optional[str]:
        """
        Extract filename from content-disposition header.
        """
        if not content_disposition:
            return None
        fname = re.findall('filename\*?=(?:utf-8\'\')?([^;]+)', content_disposition, re.IGNORECASE)
        if len(fname) == 0:
            return None
        return fname[0].strip().strip('"').strip("'")

    def download_file(
        self, 
        url: str, 
        save_dir: str, 
        progress_callback: Callable[[float, float, float], None], 
        status_callback: Callable[[str], None],
        error_callback: Callable[[str], None]
    ):
        """
        Download a file from a URL with streaming and progress reporting.
        progress_callback: (downloaded_bytes, total_bytes, speed_bps)
        """
        try:
            status_callback("Connecting...")
            response = requests.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()

            # Detect filename
            filename = self.get_filename_from_cd(response.headers.get('content-disposition'))
            if not filename:
                filename = url.split('/')[-1].split('?')[0] or "downloaded_file"
            
            # If filename has no extension, try to guess from Content-Type
            if '.' not in filename:
                content_type = response.headers.get('content-type', '').split(';')[0]
                ext = mimetypes.guess_extension(content_type)
                if ext:
                    filename += ext

            save_path = os.path.join(save_dir, filename)
            
            # Check for name collision and append index if necessary
            base, ext = os.path.splitext(save_path)
            counter = 1
            while os.path.exists(save_path):
                save_path = f"{base}_{counter}{ext}"
                counter += 1

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            status_callback(f"Downloading: {os.path.basename(save_path)}")
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress_callback(downloaded, total_size, 0) # Speed calculation can be added later
                        else:
                            # If total_size is unknown, pass -1
                            progress_callback(downloaded, -1, 0)
            
            status_callback(f"Success! Saved to {os.path.basename(save_path)}")
            return True

        except requests.exceptions.RequestException as e:
            error_callback(f"Connection Error: {str(e)}")
        except Exception as e:
            error_callback(f"Error: {str(e)}")
        return False
