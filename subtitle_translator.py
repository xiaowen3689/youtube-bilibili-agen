from google.cloud import translate_v2 as translate
import pysrt

def translate_subtitle(srt_path, target_language, output_srt_path):
    """
    Translates an SRT subtitle file to a target language using Google Cloud Translate.

    Args:
        srt_path (str): The path to the input SRT file.
        target_language (str): The target language code (e.g., "zh-CN" for Simplified Chinese).
        output_srt_path (str): The path to save the translated SRT file.

    Returns:
        str: The path to the translated SRT file if successful, None otherwise.
    """
    translate_client = translate.Client()

    try:
        subs = pysrt.open(srt_path, encoding="utf-8")
        translated_subs = pysrt.SubRipFile()

        for sub in subs:
            text = sub.text
            result = translate_client.translate(text, target_language=target_language)
            translated_text = result["translatedText"]
            
            new_sub = pysrt.SubRipItem(index=sub.index, start=sub.start, end=sub.end, text=translated_text)
            translated_subs.append(new_sub)
        
        translated_subs.save(output_srt_path, encoding="utf-8")
        print("Subtitle translation successful!")
        return output_srt_path
    except Exception as e:
        print(f"Error translating subtitles: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Create a dummy SRT file for testing
    dummy_srt_content = """
1
00:00:00,000 --> 00:00:02,000
Hello, world.

2
00:00:02,500 --> 00:00:04,500
This is a test.
"""
    dummy_srt_path = "./dummy.srt"
    with open(dummy_srt_path, "w", encoding="utf-8") as f:
        f.write(dummy_srt_content)

    output_translated_srt = "./dummy_translated.srt"
    translated_file = translate_subtitle(dummy_srt_path, "zh-CN", output_translated_srt)
    if translated_file:
        print(f"Translated subtitles saved to: {translated_file}")
    else:
        print("Subtitle translation failed.")


