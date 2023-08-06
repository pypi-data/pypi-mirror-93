import requests


def translate(text, target_lang='en', source_lang=None):
    """
    Use the Google v2 API to translate the text. You had better have set
    the API key on this function before calling it.
    """
    url_base = 'https://www.googleapis.com/language/translate/v2'
    params = dict(
        key=translate.API_key,
        q=text,
        target=target_lang,
    )
    if source_lang:
        params['source'] = source_lang
    resp = requests.get(url_base, params=params)
    resp.raise_for_status()
    return resp.json()['data']['translations'][0]['translatedText']
