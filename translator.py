# モジュールを読み込む。
import requests  # HTTP通信ライブラリ

# ======================================================================================================================
# DeepL APIのURLを設定する。
DEEPL_API_URL = 'https://api.deepl.com/v2/translate'
# ======================================================================================================================


# DeepLで翻訳する。
def deepl_translate(src_text, target_lang, deepl_api_key):
    # 翻訳言語のコードを設定する。
    if target_lang == 'German':
        target_lang_code = 'DE'
    elif target_lang == 'English':
        target_lang_code = 'EN'
    elif target_lang == 'French':
        target_lang_code = 'FR'
    elif target_lang == 'Italian':
        target_lang_code = 'IT'
    elif target_lang == 'Japanese':
        target_lang_code = 'JA'
    elif target_lang == 'Spanish':
        target_lang_code = 'ES'
    elif target_lang == 'Dutch':
        target_lang_code = 'NL'
    elif target_lang == 'Polish':
        target_lang_code = 'PL'
    elif target_lang == 'Portuguese':
        target_lang_code = 'PT'
    elif target_lang == 'Russian':
        target_lang_code = 'RU'
    elif target_lang == 'Chinese':
        target_lang_code = 'ZH'
    else:
        target_lang_code = None

    deepl_trans_result = requests.post(
        DEEPL_API_URL,
        data={
            "auth_key": deepl_api_key,
            "text": src_text,
            "target_lang": target_lang_code}
    ).json()
    trans_text = deepl_trans_result["translations"][0]["text"]

    return trans_text