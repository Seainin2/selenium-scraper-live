import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):
    print('Get Video Divs')
    VIDEO_DIVS_TAG = 'ytd-video-renderer'
    length = 0
    count = 1
  
    while length<4 and count<100:
      print('Attempt ',count)
      driver.get(YOUTUBE_TRENDING_URL)
      videos = driver.find_elements(By.TAG_NAME, VIDEO_DIVS_TAG)
      length = len(videos)
      count = count + 1
    return videos


def parse_video(video):
    title_tag = video.find_element(By.ID, 'video-title')
    title = title_tag.text
    url = title_tag.get_attribute('href')

    thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
    thumbnail_url = thumbnail_tag.get_attribute('src')

    channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
    channel = channel_div.text

    description = video.find_element(By.ID, 'description-text').text

    views = video.find_element(By.ID, 'metadata-line').text

    return {
      'title': title,
      'url': url,
      'thumbnail_url': thumbnail_url,
      'channel': channel,
      'description': description,
      'views': views
    }

if __name__ == "__main__":

    print('Creating driver')
    driver = get_driver()

    print('Fetching the page')
    videos = get_videos(driver)

    print(f'Found {len(videos)}')

    print('Parsing videos')
    #title,url,thumbnail_url,channel,views,uploaded,description

    videos_data = [parse_video(video )for video in videos]

    print("Save the data to a CSV file")
    videos_df = pd.DataFrame(videos_data)
    print(videos_df)
    videos_df.to_csv('trending.csv')

  

