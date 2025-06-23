import subprocess
import os

def extract_audio(video_path, output_audio_path):
    """
    Extracts audio from a video file using ffmpeg.

    Args:
        video_path (str): The path to the input video file.
        output_audio_path (str): The path to save the extracted audio file (e.g., audio.mp3).

    Returns:
        str: The path to the extracted audio file if successful, None otherwise.
    """
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn", # No video
            "-acodec", "libmp3lame", # Audio codec
            "-q:a", "2", # Variable bitrate (VBR) quality, 2 is good quality
            output_audio_path
        ]
        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Audio extraction successful!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return output_audio_path
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Create a dummy video file for testing
    dummy_video_path = "./test_video.mp4"
    with open(dummy_video_path, "w") as f:
        f.write("This is a dummy video file.")

    output_audio_file = "./extracted_audio.mp3"
    extracted_file = extract_audio(dummy_video_path, output_audio_file)
    if extracted_file:
        print(f"Audio extracted to: {extracted_file}")
    else:
        print("Audio extraction failed.")
    
    # Clean up dummy file
    if os.path.exists(dummy_video_path):
        os.remove(dummy_video_path)
    if os.path.exists(output_audio_file):
        os.remove(output_audio_file)


