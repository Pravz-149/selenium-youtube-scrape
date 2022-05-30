import os
import json
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'


def get_driver():
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):
    VIDEO_DIV_TAG = "ytd-video-renderer"
    driver.get(YOUTUBE_TRENDING_URL)
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
        'Title': title, 'url': url, 'Thumbnail URL': thumbnail_url,
        'channel name': channel_name, 'Description Text': description_text
    }

def send_email(body):
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server_ssl.ehlo()
    SENDER_EMAIL = 'pravallikatrailmail@gmail.com'
    RECEIVER_EMAIL = 'pravallika14998@gmail.com'
    my_secret = os.environ['GMAIL_PASSWORD']

    subject = 'YouTube Trending Videos'
    email_text = f"""
    From:{SENDER_EMAIL}
    To:{RECEIVER_EMAIL}
    Subject:{subject}
    {body}
    """
    server_ssl.login(SENDER_EMAIL,my_secret)
    server_ssl.sendmail(SENDER_EMAIL,RECEIVER_EMAIL,email_text)
    server_ssl.close()

    except:
      print('Something went wrong...')

def lambda_handler(event, context):
    #Create the browser
    driver = get_driver()
    #Get the Videos here
    videos = get_videos(driver)
    #Parse the top 10 videos
    videos_data = [parse_video(video) for video in videos[:10]]
    #Send the data over email
    body = json.dumps(videos_data)
    send_email(body)
    driver.close();
    driver.quit();
    response = {
        "statusCode": 200,
        "body": videos_data
    }
  return response


  
