import os
from gtts import gTTS
import gradio as gr
from translate import Translator
import speech_recognition as sr

os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

auth_token = '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'   # For accesing HugginFace Facebook Model. 

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
    """ Layer on top of gTTS - providing text to speech for """

    def __init__(self, text, tld, lang) -> None:
        """ [Constructor takes in text, the top-level domain and the language in which the text is : ] """
        self.text = text
        self.tld = tld    
        self.lang = lang
    
    def tts(self):
        """ [Converts the text to speech.] """
        tts = gTTS(text=self.text,tld= TLD.tld[self.tld], lang=Languages.lang[self.lang])
        tts.save('tts.mp3')
        with open('tts.mp3') as fp:
            return fp.name

langs = Languages()
top_level_domain = TLD()

""" [Utiility Functions] """

def T2TConversion(text, dest):
    """ [(Utility Function) : Converts sentence from english to another language ] """
    translator = Translator(to_lang=langs.lang[dest])
    return translator.translate(text)

def convert_text(Text,Language, Accent):
    """ [(Utility Function) : Performs Text-To-Speech provided language and accent.] """
    tts = TTSLayer(Text,Accent, Language)
    return tts.tts()


class GRadioInterface:
    """ [Class for managing UI for the application.] """
    def __init__(self, function) -> None:
        """ [Interface for packaging GRadio Application] """
        
        # Necessary for interface
        self._function = function
        self._inputs = [
                gr.TextArea(label = 'The Text to be Converted to Audio'),
                gr.Dropdown([key for key,_ in langs.lang.items()], label='Languages Available',), 
                gr.Dropdown([key for key,_ in top_level_domain.tld.items()])]

        self.outputs = gr.Audio()

        # Necessary for descriptive content
        self.title = 'A Text-To-Speech Converter for Low Resource Languages'
        self.description = 'Support over 50 languages !'
        self.article = 'How does it work ? Just write a sentence (in target language) in the space provided and select the target language and accent and press submit. That is it. Wait and Enjoy.'
    
    def start(self):
        """ [Launching the interface in a tabbed manner.] """

        it_1 = gr.Interface(fn=self._function, inputs=self._inputs,outputs=self.outputs,
            title = self.title,
            description=  self.description,
            article= self.article)
            
        it_2 =  gr.Interface(fn=T2TConversion, 
            inputs = [ 
                gr.Text(label='Write a sentence in English'),
                gr.Dropdown([key for key,_ in langs.lang.items()])], 
            outputs= gr.Text(label='The Converted Text'),
            title = 'Translation from English',
            description='Write a sentence in english and convert to other languages for speech synthesis',
            article='What if you do not have a sentence in a particular language? Just write the sentence in english and let us do the magic.')

        it_3 =  gr.Interface.load(
                "huggingface/facebook/wav2vec2-base-960h",
                title="Automatic Speech Recognition",
                inputs=gr.Audio(),
                description="What you cookin' ?",
                api_key=auth_token
        )

        demo = gr.TabbedInterface([it_1, it_2, it_3],['Speech Synthesis', 'Sentence Translation', 'Automatic Speech Recognition'])
        demo.launch()

demo_app = GRadioInterface(function=convert_text)
demo_app.start()
