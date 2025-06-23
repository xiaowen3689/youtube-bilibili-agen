from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import threading
from main_agent import YouTubeToBilibiliAgent

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store processing status
processing_status = {
    "is_processing": False,
    "current_step": 0,
    "progress": 0,
    "result": None,
    "error": None
}

def process_video_async(youtube_url, video_title, video_description, video_tags):
    """
    Asynchronous video processing function
    """
    global processing_status
    
    try:
        processing_status["is_processing"] = True
        processing_status["current_step"] = 0
        processing_status["progress"] = 0
        processing_status["result"] = None
        processing_status["error"] = None
        
        # Initialize agent
        agent = YouTubeToBilibiliAgent()
        
        # Process video with step-by-step updates
        steps = [
            "下载YouTube视频",
            "提取音频",
            "生成字幕",
            "翻译字幕",
            "合并双语字幕",
            "上传到B站"
        ]
        
        for i, step in enumerate(steps):
            processing_status["current_step"] = i
            processing_status["progress"] = (i / len(steps)) * 100
            
            # Simulate processing time for each step
            # In real implementation, you would call the actual functions here
            import time
            time.sleep(2)  # Simulate processing time
        
        # Call the actual agent processing
        result = agent.process_video(
            youtube_url, 
            video_title or "从YouTube转载的视频", 
            video_description or "这是一个从YouTube转载并添加了双语字幕的视频。", 
            video_tags.split(',') if video_tags else ["转载", "双语字幕", "YouTube"]
        )
        
        processing_status["result"] = result
        processing_status["progress"] = 100
        
    except Exception as e:
        processing_status["error"] = str(e)
    finally:
        processing_status["is_processing"] = False

@app.route('/api/process', methods=['POST'])
def process_video():
    """
    Start video processing
    """
    global processing_status
    
    if processing_status["is_processing"]:
        return jsonify({"error": "已有视频正在处理中，请稍后再试"}), 400
    
    data = request.json
    youtube_url = data.get('youtube_url')
    video_title = data.get('video_title', '')
    video_description = data.get('video_description', '')
    video_tags = data.get('video_tags', '')
    
    if not youtube_url:
        return jsonify({"error": "YouTube链接不能为空"}), 400
    
    # Start processing in a separate thread
    thread = threading.Thread(
        target=process_video_async,
        args=(youtube_url, video_title, video_description, video_tags)
    )
    thread.start()
    
    return jsonify({"message": "视频处理已开始"})

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Get current processing status
    """
    return jsonify(processing_status)

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "healthy"})

@app.route('/', methods=['GET'])
def index():
    """
    API information endpoint
    """
    return jsonify({
        "name": "YouTube到B站智能体API",
        "version": "1.0.0",
        "endpoints": {
            "/api/process": "POST - 开始视频处理",
            "/api/status": "GET - 获取处理状态",
            "/api/health": "GET - 健康检查"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

