from dataclasses import dataclass
from gtts import gTTS
import gradio as gr
from io import BytesIO
import tempfile

class Languages:
    """ Languages currently supported by the application. """

    lang = {'Afrikaans': 'af','Arabic':'ar','Bulgarian':'bg','Bengali':'bn','Bosnian':'bs',
    'Catalan':'ca','Czech':'cs','Danish':'da','German':'de','Greek':'el','English':'en',
    'Spanish':'es','Estonian':'et','Finnish':'fi','French':'fr','Gujarati':'gu','Hindi':'hi',
    'Croatian':'hr','Hungarian':'hu','Indonesian':'id','Icelandic':'is','Italian':'it',
    'Hebrew':'iw','Japanese':'ja','Javanese':'jw','Khmer':'km','Kannada':'kn','Korean':'ko',
    'Latin':'la','Latvian':'lv','Malayalam':'ml','Marathi':'mr','Malay':'ms',
    'Myanmar (Burmese)':'my','Nepali':'ne', 'Dutch':'nl','Norwegian':'no',
    'Polish':'pl','Portuguese':'pt','Romanian':'ro','Russian':'ru','Sinhala':'si',
    'Slovak':'sk', 'Albanian':'sq','Serbian':'sr','Sundanese':'su','Swedish':'sv',
    'Swahili':'sw','Tamil':'ta','Telugu':'te','Thai':'th','Filipino':'tl','Turkish':'tr',
    'Ukrainian':'uk','Urdu':'ur','Vietnamese':'vi','Chinese (Simplified)':'zh-CN',
    'Chinese (Mandarin/Taiwan)':'zh-TW',
    'Chinese (Mandarin)':'zh'}

class TLD:
    """ Depending on the top-level domain, gTTS can speak in different accents. """

    tld = {'English(Australia)':'com.au', 'English (United Kingdom)':'co.uk',
    'English (United States)':'us', 'English (Canada)':'ca','English (India)':'co.in',
    'English (Ireland)':'ie','English (South Africa)':'co.za','French (Canada)':'ca',
    'French (France)':'fr','Portuguese (Brazil)':'com.br','Portuguese (Portugal)':'pt',
    'Spanish (Mexico)':'com.mx','Spanish (Spain)':'es','Spanish (United States)':'us'}

class TTSLayer():
    """ Layer on top of gTTS """
    def __init__(self, text, tld, lang) -> None:
        self.text = text   # The text that needs to be converted.
        self.tld = tld     # used for accents and all.
        self.lang = lang   # the language to which we need to generate the voice
    
    def tts(self):
        tts = gTTS(text=self.text,tld= TLD.tld[self.tld], lang=Languages.lang[self.lang])
        tts.save('tts.mp3')
        with open('tts.mp3') as fp:
            return fp.name



class RadioInterface:
    def __init__(self, function, inputs, outputs) -> None:
        # Necessary for interface
        self._function = function,
        self._inputs = inputs,
        self.outputs = outputs,

        # Necessary for descriptive content
        self.title = 'title',
        self.description = 'desc'
        self.article = 'article'

    pass


# Populate the input with the dictionary keys 
langs = Languages()
top_level_domain = TLD()

# Text, tld and language will be extracted from the input thing.
# tts = TTSLayer()


def greet(Text,Language, Accent):
    print(Text, Language, Accent)
    tts = TTSLayer(Text,Accent, Language)
    return tts.tts()

# gr.TextArea()

demo = gr.Interface(fn=greet, 
        inputs=[
            gr.TextArea(),
            gr.Dropdown([key for key,_ in langs.lang.items()]), 
            gr.Dropdown([key for key,_ in top_level_domain.tld.items()])], 
        
        outputs=gr.Audio())

demo.launch()
