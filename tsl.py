from translate import Translator

def text_translate(to_lang, from_lang, text_to_translate):
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(text_to_translate)
    return translation

print(text_translate('en', 'id',  'anda luar biasa'))