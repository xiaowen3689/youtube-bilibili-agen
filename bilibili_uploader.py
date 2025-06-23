import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def upload_video_to_bilibili(video_path, title, description, tags):
    """
    Uploads a video to Bilibili using Selenium.

    Args:
        video_path (str): The absolute path to the video file.
        title (str): The title of the video.
        description (str): The description of the video.
        tags (list): A list of tags for the video.

    Returns:
        bool: True if upload is successful, False otherwise.
    """
    # Initialize Chrome WebDriver
    # Make sure you have chromedriver installed and in your PATH, or specify its path.
    # For sandbox environment, usually chromedriver is pre-installed.
    service = Service(executable_path="/usr/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless") # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to Bilibili upload page
        driver.get("https://member.bilibili.com/video/upload.html")

        # Wait for the upload button to be present and clickable
        upload_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type=\"file\"]"))
        )
        
        # Send the video file path to the input element
        upload_button.send_keys(video_path)

        print(f"Uploading video: {video_path}")

        # Wait for upload to start and progress bar to appear (adjust as needed)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CLASS_NAME, "upload-progress-v2"))
        )
        print("Video upload started...")

        # Wait for upload to complete (progress bar disappears or success message appears)
        WebDriverWait(driver, 600).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "upload-progress-v2"))
        )
        print("Video upload completed.")

        # Fill in video title
        title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "video-title-input"))
        )
        title_input.clear()
        title_input.send_keys(title)
        print(f"Set title: {title}")

        # Fill in video description
        description_textarea = driver.find_element(By.CLASS_NAME, "description-textarea")
        description_textarea.clear()
        description_textarea.send_keys(description)
        print(f"Set description: {description}")

        # Add tags (this part might need adjustment based on Bilibili's UI)
        # Bilibili's tag input is dynamic, so we might need to simulate typing and selecting
        tag_input = driver.find_element(By.CLASS_NAME, "tag-input")
        for tag in tags:
            tag_input.send_keys(tag)
            tag_input.send_keys(Keys.ENTER) # Simulate pressing Enter after each tag
            time.sleep(0.5) # Small delay
        print(f"Set tags: {', '.join(tags)}")

        # Click the submit button (this XPath might need to be more specific)
        submit_button = driver.find_element(By.XPATH, "//div[contains(@class, 'submit-btn') and text()='立即投稿']")
        submit_button.click()
        print("Clicked submit button.")

        # Wait for success message or redirection
        WebDriverWait(driver, 30).until(
            EC.url_contains("member.bilibili.com/video/submission") # Or check for a success element
        )
        print("Video uploaded successfully!")
        return True

    except Exception as e:
        print(f"An error occurred during Bilibili upload: {e}")
        return False
    finally:
        driver.quit()

if __name__ == '__main__':
    # Example usage:
    # Create a dummy video file for testing
    dummy_video_path = "./dummy_video.mp4"
    with open(dummy_video_path, "w") as f:
        f.write("This is a dummy video content.")

    video_title = "测试视频上传"
    video_description = "这是一个通过自动化脚本上传的测试视频。"
    video_tags = ["测试", "自动化", "B站"]

    success = upload_video_to_bilibili(dummy_video_path, video_title, video_description, video_tags)
    if success:
        print("Bilibili video upload example finished successfully.")
    else:
        print("Bilibili video upload example failed.")
    
    # Clean up dummy file
    if os.path.exists(dummy_video_path):
        os.remove(dummy_video_path)


