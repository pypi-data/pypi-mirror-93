from __future__ import absolute_import

import logging

from . import google
import pmxbot.core

log = logging.getLogger(__name__)


def set_key():
    key = pmxbot.config.get('Google API key')
    assert key
    google.translate.API_key = key


@pmxbot.core.command("translate", aliases=('trans', 'googletrans', 'googletranslate'))
def translate(client, event, channel, nick, rest):
    """
    Translate a phrase using Google Translate. First argument should be
    the language[s]. It is a 2 letter abbreviation. It will auto detect
    the orig lang if you only give one; or two languages joined by a |,
    for example 'en|de' to trans from English to German. Follow this by
    the phrase you want to translate.
    """
    try:
        set_key()
    except Exception:
        return (
            "No API key configured. Google charges for translation. "
            "Please register for an API key at "
            "https://code.google.com/apis/console/?api=translate&promo=tr "
            "and set the 'Google API key' config variable to a valid key"
        )
    rest = rest.strip()
    langpair, _, rest = rest.partition(' ')
    source_lang, _, target_lang = langpair.rpartition('|')
    try:
        return google.translate(rest.encode('utf-8'), target_lang, source_lang)
    except Exception:
        log.exception("Error occurred in translate")
        tmpl = "An error occurred. " "Are you sure {langpair} is a valid language?"
        return tmpl.format(**vars())


def test_translate(self):
    """
    The translate function should be able to translate a simple string.
    """
    query = '|en que no desea la nueva pregunta'
    res = translate(None, None, '#test', 'testrunner', query)
    assert 'new question' in res.lower()
    query = 'es|en que no desea la nueva pregunta'
    res = translate(None, None, '#test', 'testrunner', query)
    assert 'new question' in res.lower()


def test_translate_invalid_lang(self):
    """
    An invalid language should give a nice error message.
    """
    # sp is not a language
    invalid_query = 'sp|en que no desea la nueva pregunta'
    res = translate(None, None, '#test', 'testrunner', invalid_query)
    assert 'are you sure' in res.lower()
