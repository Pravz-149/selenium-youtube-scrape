from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):
    driver.get(YOUTUBE_TRENDING_URL)
    print('Page Title:', driver.title)
    VIDEO_DIV_TAG = "ytd-video-renderer"
    videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
    return videos


def parse_video(video):
    # Title,url,thumbnail url,channel,views,uploaded,description

    # To get the title from a tag
    title_tag = video.find_element(By.ID, 'video-title')
    title = title_tag.text

    # To get the link we need href Attribute from a tag
    url = title_tag.get_attribute('href')

    # To get the thumbnail link we need src Attribute from img tag
    thumbnail_tag = video.find_element(By.TAG_NAME, "img")
    thumbnail_url = thumbnail_tag.get_attribute('src')

    # To get the channel name
    channel_class = video.find_element(By.CLASS_NAME, "ytd-channel-name")
    channel_name = channel_class.text

    # To get the Description text
    description_tag = video.find_element(By.ID, "description-text")
    description_text = description_tag.text

    return {
        'Title:', title, 'url:', url, 'Thumbnail URL:', thumbnail_url,
        "channel name:", channel_name, "Description Text:", description_text
    }


if __name__ == '__main__':
    print('creating driver')
    driver = get_driver()

    print('Fetching trending videos')
    videos = get_videos(driver)

    print(f'Found {len(videos)} videos')

    print('Parsing top 10 Videos')
    videos_data = [parse_video(video) for video in videos[:10]]

    print('Save the data to a CSV')
    videos_df = pd.DataFrame(videos_data)
    print(videos_df)
    videos_df.to_csv('trending.csv')

  
