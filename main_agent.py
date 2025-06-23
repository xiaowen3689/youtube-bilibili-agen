import os
import sys
from youtube_downloader import download_youtube_video
from audio_extractor import extract_audio
from subtitle_generator import generate_subtitles
from subtitle_translator import translate_subtitle
from bilingual_subtitle_merger import merge_subtitles
from bilibili_uploader import upload_video_to_bilibili

class YouTubeToBilibiliAgent:
    def __init__(self, work_dir="./work"):
        self.work_dir = work_dir
        os.makedirs(work_dir, exist_ok=True)
    
    def process_video(self, youtube_url, video_title, video_description, video_tags, target_language="zh-CN"):
        """
        Complete workflow: Download YouTube video, generate bilingual subtitles, and upload to Bilibili.
        
        Args:
            youtube_url (str): YouTube video URL
            video_title (str): Title for the Bilibili video
            video_description (str): Description for the Bilibili video
            video_tags (list): Tags for the Bilibili video
            target_language (str): Target language for subtitle translation
            
        Returns:
            dict: Result status and file paths
        """
        result = {
            "success": False,
            "video_path": None,
            "audio_path": None,
            "original_srt": None,
            "translated_srt": None,
            "bilingual_srt": None,
            "upload_success": False,
            "error": None
        }
        
        try:
            print("=== 开始处理视频 ===")
            print(f"YouTube URL: {youtube_url}")
            
            # Step 1: Download YouTube video
            print("\n1. 下载YouTube视频...")
            video_path = download_youtube_video(youtube_url, self.work_dir)
            if not video_path:
                raise Exception("视频下载失败")
            result["video_path"] = video_path
            print(f"视频下载成功: {video_path}")
            
            # Step 2: Extract audio
            print("\n2. 提取音频...")
            audio_path = os.path.join(self.work_dir, "extracted_audio.mp3")
            extracted_audio = extract_audio(video_path, audio_path)
            if not extracted_audio:
                raise Exception("音频提取失败")
            result["audio_path"] = extracted_audio
            print(f"音频提取成功: {extracted_audio}")
            
            # Step 3: Generate subtitles
            print("\n3. 生成字幕...")
            original_srt_path = os.path.join(self.work_dir, "original_subtitles.srt")
            generated_srt = generate_subtitles(extracted_audio, original_srt_path)
            if not generated_srt:
                raise Exception("字幕生成失败")
            result["original_srt"] = generated_srt
            print(f"字幕生成成功: {generated_srt}")
            
            # Step 4: Translate subtitles
            print("\n4. 翻译字幕...")
            translated_srt_path = os.path.join(self.work_dir, "translated_subtitles.srt")
            translated_srt = translate_subtitle(generated_srt, target_language, translated_srt_path)
            if not translated_srt:
                raise Exception("字幕翻译失败")
            result["translated_srt"] = translated_srt
            print(f"字幕翻译成功: {translated_srt}")
            
            # Step 5: Merge bilingual subtitles
            print("\n5. 合并双语字幕...")
            bilingual_srt_path = os.path.join(self.work_dir, "bilingual_subtitles.srt")
            bilingual_srt = merge_subtitles(generated_srt, translated_srt, bilingual_srt_path)
            if not bilingual_srt:
                raise Exception("双语字幕合并失败")
            result["bilingual_srt"] = bilingual_srt
            print(f"双语字幕合并成功: {bilingual_srt}")
            
            # Step 6: Upload to Bilibili
            print("\n6. 上传到B站...")
            upload_success = upload_video_to_bilibili(video_path, video_title, video_description, video_tags)
            result["upload_success"] = upload_success
            if upload_success:
                print("B站上传成功!")
            else:
                print("B站上传失败")
            
            result["success"] = True
            print("\n=== 处理完成 ===")
            
        except Exception as e:
            result["error"] = str(e)
            print(f"\n处理失败: {e}")
        
        return result

def main():
    """
    Command line interface for the agent
    """
    if len(sys.argv) < 2:
        print("使用方法: python main_agent.py <YouTube_URL>")
        print("示例: python main_agent.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        return
    
    youtube_url = sys.argv[1]
    
    # Default values (can be customized)
    video_title = "从YouTube转载的视频"
    video_description = "这是一个从YouTube转载并添加了双语字幕的视频。"
    video_tags = ["转载", "双语字幕", "YouTube"]
    
    # Initialize agent
    agent = YouTubeToBilibiliAgent()
    
    # Process video
    result = agent.process_video(youtube_url, video_title, video_description, video_tags)
    
    # Print results
    print("\n=== 处理结果 ===")
    print(f"成功: {result['success']}")
    if result["error"]:
        print(f"错误: {result['error']}")
    if result["video_path"]:
        print(f"视频文件: {result['video_path']}")
    if result["bilingual_srt"]:
        print(f"双语字幕: {result['bilingual_srt']}")
    print(f"B站上传: {'成功' if result['upload_success'] else '失败'}")

if __name__ == "__main__":
    main()

