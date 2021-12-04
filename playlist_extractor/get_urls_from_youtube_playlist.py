from selenium import webdriver
import time
import yaml
import Youtube_to_mp3
import os

from results_as_we_go import results_as_we_go

def get_urls_from_playlist(youtube_playlist_url=None):
    output_dict = {}
    if youtube_playlist_url == None:
        print('Please enter a valid YouTube playlist url')
        return

    driver = webdriver.Firefox()
    driver.get(youtube_playlist_url)
    # scroll page down
    old_position = 0
    new_position = None
    position_script = """return (window.pageYOffset !== undefined) ?
          window.pageYOffset : (document.documentElement ||
          document.body.parentNode || document.body);"""
    while new_position != old_position:
        old_position = driver.execute_script(position_script)
        time.sleep(1)
        driver.execute_script(
            """var scrollingElement = (document.scrollingElement ||
             document.body);scrollingElement.scrollTop =
             scrollingElement.scrollHeight;""")
        new_position = driver.execute_script(position_script)
    source_page = driver.page_source
    driver.quit()

    # extract the urls and names
    counter = 1
    element_to_find = 'amp;index={}" ar'
    video_index = source_page.find(element_to_find.format(counter))  # 'amp;index=1" ar'
    while video_index != -1:
        title_element = ''
        count_name = video_index
        while title_element != 'title="':
            title_element = source_page[count_name: count_name + 7]
            count_name += 1
        count_name += 6
        start_title_position = count_name
        end_title = ''
        while end_title != '>':
            end_title = source_page[count_name]  # exit loop if end_title == '>'
            count_name += 1
        name = source_page[start_title_position:count_name - 2]  # extract the name of the video
        name = name.replace('&quot;', '"')
        video_id = source_page[video_index - 56: video_index - 45]  # extract video id
        print(str(counter)
              + '. link: ' + 'https://www.youtube.com/watch?v=' + video_id +
              ', name: ' + name)
        counter += 1
        video_index = source_page.find(element_to_find.format(counter))  # continue the next video

        filesafe_string = ''.join(e for e in name if e.isalnum())
        video_url = 'https://www.youtube.com/watch?v=' + video_id

        output_dict[video_url] = filesafe_string

    return output_dict


def get_playlists_from_yaml():
    with open('../youtube_playlists.yaml', 'r') as f:
        open_file = f.read()
        playlists = yaml.load_all(open_file, Loader=yaml.FullLoader)

    return playlists


def download_audio_from_videos_in_playlists(playlists):
    os.chdir('../extracted_mp3s')
    for dict in playlists:
        print(f'Grabbing {dict["name"]}')
        url_dict = get_urls_from_playlist(dict['url'])

        keys = url_dict.keys()

        print('Downloading.  Youtube_DL already checks if a file exists before downloading...')

        def get_mp3(url):
            try:
                print(url)
                Youtube_to_mp3.youtube_to_mp3([url])
            except Exception as e:
                print(e)

        # Multithreaded for great justice.
        results_as_we_go(get_mp3, keys)


        print(url_dict)


generated_playlists = get_playlists_from_yaml()
download_audio_from_videos_in_playlists(generated_playlists)
