import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = 'https://youtube.com/feed/trending'


def get_driver():
  chrome_options = Options()

  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  driver.get(url)
  VIDEO_DIV_TAG = "ytd-video-renderer"
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos
def parse_video(video):
    title_tag = video.find_element(By.ID, "video-title")
    title = title_tag.text
    video_url = title_tag.get_attribute('href')
    
    thumbnail_tag=  video.find_element(By.TAG_NAME, 'img')
    thumbnail_url = thumbnail_tag.get_attribute('src')
  
    channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
    channel = channel_div.text
    info_div = video.find_element(By.ID, 'metadata-line')
    views, uploaded = info_div.text.splitlines()
    desc = video.find_element(By.ID,'description-text')

    video_info = {
                'title': title,
                'url':video_url,
                'thumbnail_url':thumbnail_url,
                'channel':channel,
                'views':views,
                'uploaded':uploaded,
                'description':desc.text
                 }
    return video_info  
if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()
  
  print('Getting trending Videos')
  videos = get_videos(driver)
  
  print(f'Found {len(videos)} videos')

  print('Parsing first 10 videos')
  print('\n')

  videos_data = [parse_video(video) for video in videos[:10]]

  print('Saving the data to CSV file')
  videos_df = pd.DataFrame(videos_data)
  videos_df.to_csv('trending.csv')
  
  