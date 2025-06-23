import pysrt

def merge_subtitles(original_srt_path, translated_srt_path, output_srt_path):
    """
    Merges two SRT subtitle files into a single bilingual SRT file.

    Args:
        original_srt_path (str): The path to the original language SRT file.
        translated_srt_path (str): The path to the translated language SRT file.
        output_srt_path (str): The path to save the merged bilingual SRT file.

    Returns:
        str: The path to the merged SRT file if successful, None otherwise.
    """
    try:
        original_subs = pysrt.open(original_srt_path, encoding="utf-8")
        translated_subs = pysrt.open(translated_srt_path, encoding="utf-8")

        merged_subs = pysrt.SubRipFile()

        # Assuming both SRT files have the same number of subtitles and are aligned
        for i in range(len(original_subs)):
            original_text = original_subs[i].text
            translated_text = translated_subs[i].text
            
            # Merge the texts with a newline in between
            merged_text = f"{original_text}\n{translated_text}"
            
            new_sub = pysrt.SubRipItem(
                index=original_subs[i].index,
                start=original_subs[i].start,
                end=original_subs[i].end,
                text=merged_text
            )
            merged_subs.append(new_sub)
        
        merged_subs.save(output_srt_path, encoding="utf-8")
        print("Bilingual subtitle merging successful!")
        return output_srt_path
    except Exception as e:
        print(f"Error merging subtitles: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Create dummy original and translated SRT files for testing
    dummy_original_srt_content = """
1
00:00:00,000 --> 00:00:02,000
Hello, world.

2
00:00:02,500 --> 00:00:04,500
This is a test.
"""
    dummy_translated_srt_content = """
1
00:00:00,000 --> 00:00:02,000
你好，世界。

2
00:00:02,500 --> 00:00:04,500
这是一个测试。
"""
    original_srt_path = "./dummy_original.srt"
    translated_srt_path = "./dummy_translated.srt"
    output_merged_srt = "./dummy_bilingual.srt"

    with open(original_srt_path, "w", encoding="utf-8") as f:
        f.write(dummy_original_srt_content)
    with open(translated_srt_path, "w", encoding="utf-8") as f:
        f.write(dummy_translated_srt_content)

    merged_file = merge_subtitles(original_srt_path, translated_srt_path, output_merged_srt)
    if merged_file:
        print(f"Merged bilingual subtitles saved to: {merged_file}")
    else:
        print("Bilingual subtitle merging failed.")


