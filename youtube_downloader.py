import subprocess
import os

def download_youtube_video(url, output_path="."):
    """
    Downloads a YouTube video using yt-dlp.

    Args:
        url (str): The URL of the YouTube video.
        output_path (str): The directory to save the downloaded video.

    Returns:
        str: The path to the downloaded video file if successful, None otherwise.
    """
    os.makedirs(output_path, exist_ok=True)
    try:
        command = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
            url
        ]
        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Download successful!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Extract the downloaded filename from stdout
        for line in result.stdout.splitlines():
            if "[Merger] Merging formats into" in line:
                # The filename is usually enclosed in double quotes after 'Merging formats into'
                return line.split("Merging formats into \"")[1].split("\"")[0]
            elif "[download] Destination:" in line:
                return line.split("Destination:")[1].strip()

        return None

    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' # Replace with a real YouTube video URL for testing
    downloaded_file = download_youtube_video(video_url, output_path='./downloads')
    if downloaded_file:
        print(f"Video downloaded to: {downloaded_file}")
    else:
        print("Video download failed.")


