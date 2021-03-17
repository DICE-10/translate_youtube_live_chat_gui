# モジュールを読み込む。
import requests  # HTTP通信ライブラリ

# ======================================================================================================================
# APIのURLを設定する。
YOUTUBE_API_VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'  # YouTubeビデオ
YOUTUBE_API_CHAT_URL = 'https://www.googleapis.com/youtube/v3/liveChat/messages'  # YouTubeチャット
# ======================================================================================================================


# YouTubeLiveのURLからビデオIDを取得する。
def get_video_id(youtube_live_url):
    video_id = youtube_live_url.replace('https://www.youtube.com/watch?v=', '')
    return video_id


# 指定したビデオIDのビデオデータを取得する。
def get_video_data(video_id, youtube_api_key):
    video_data = requests.get(
        YOUTUBE_API_VIDEO_URL,
        params={
            'key': youtube_api_key,
            'id': video_id,
            'part': 'liveStreamingDetails'}
    ).json()
    return video_data


# チャットIDを取得する。
def get_chat_id(video_data):
    # YouTubeLive以外の場合処理を中断する。
    if len(video_data['items']) == 0:
        chat_id = None
        error_message = 'Not Live'
    elif 'liveStreamingDetails' not in video_data['items'][0].keys():
        chat_id = None
        error_message = 'Not Live'
    elif 'activeLiveChatId' not in video_data['items'][0]['liveStreamingDetails'].keys():
        chat_id = None
        error_message = 'No Chat'
    else:
        chat_id = video_data['items'][0]['liveStreamingDetails']['activeLiveChatId']
        error_message = None
    return chat_id, error_message


# ページトークンを取得する。
def get_page_token(chat_data):
    page_token = chat_data['nextPageToken']
    return page_token


# 指定したチャットIDのチャットデータを取得する。
def get_chat_data(chat_id, page_token, youtube_api_key):
    chat_data = requests.get(
        YOUTUBE_API_CHAT_URL,
        params={
            'key': youtube_api_key,
            'liveChatId': chat_id,
            'part': 'id,snippet,authorDetails',
            'pageToken': page_token}
    ).json()
    return chat_data


# メッセージリストを作成する。
def get_message_list(chat_data):
    message_list = []
    for chat_item in chat_data['items']:  # チャットアイテムの数だけ繰り返す。
        message_list.append(chat_item['snippet']['displayMessage'])
    return message_list


# ユーザー名リストを作成する。
def get_user_name_list(chat_data):
    user_name_list = []
    for chat_item in chat_data['items']:  # チャットアイテムの数だけ繰り返す。
        user_name_list.append(chat_item['authorDetails']['displayName'])
    return user_name_list