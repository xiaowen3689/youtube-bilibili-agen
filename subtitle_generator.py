import datetime
import whisper
import os

def generate_subtitles(audio_path, output_srt_path, model_name="base"):
    """
    Generates subtitles from an audio file using OpenAI Whisper.

    Args:
        audio_path (str): The path to the input audio file.
        output_srt_path (str): The path to save the generated SRT file.
        model_name (str): The name of the Whisper model to use (e.g., "base", "small", "medium", "large").

    Returns:
        str: The path to the generated SRT file if successful, None otherwise.
    """
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path)
        
        with open(output_srt_path, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start_time = str(0) + str(datetime.timedelta(seconds=segment["start"])) + ",000"
                end_time = str(0) + str(datetime.timedelta(seconds=segment["end"])) + ",000"
                text = segment["text"]
                f.write(f"{segment['id'] + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text.strip()}\n\n")
        
        print("Subtitle generation successful!")
        return output_srt_path
    except Exception as e:
        print(f"Error generating subtitles: {e}")
        return None

if __name__ == '__main__':
    # Example usage (requires an audio file and a Whisper model downloaded)
    # You can download a small audio file for testing or use the extracted_audio.mp3 from audio_extractor.py
    dummy_audio_path = "./extracted_audio.mp3" # Replace with a real audio file for testing
    output_srt_file = "./output.srt"
    
    # Create a dummy audio file for testing if it doesn't exist
    if not os.path.exists(dummy_audio_path):
        with open(dummy_audio_path, "w") as f:
            f.write("This is a dummy audio file.")

    generated_file = generate_subtitles(dummy_audio_path, output_srt_file)
    if generated_file:
        print(f"Subtitles generated to: {generated_file}")
    else:
        print("Subtitle generation failed.")
    
    # Clean up dummy file
    if os.path.exists(dummy_audio_path):
        os.remove(dummy_audio_path)
    if os.path.exists(output_srt_file):
        os.remove(output_srt_file)


