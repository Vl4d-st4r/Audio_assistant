import traceback
import webbrowser
from vosk import Model, KaldiRecognizer
import pyttsx3
import random
from googlesearch import search
import wikipediaapi
from termcolor import colored
from dotenv import load_dotenv
import speech_recognition
import wave
import json
import os
from pars import weather_info
from openai import OpenAI
import time
import multiprocessing
import rkfdf

#from ffs import res
import pyautogui
#en-scottish
#en-westindies
#hungarian

def play_greetings(*args: tuple):
    greetings = [
        translator.get("Hello, {}! How can I help you?").format(person.name),
        translator.get("Good day to you {}! I would be glad to help.").format(person.name)
    ]
    play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])

def play_farewell_and_quit(*args: tuple):
    farewells = [
        translator.get("Goodbye, {}! Have a nice day!").format(person.name),
        translator.get("See you later, {}!").format(person.name)
    ]
    play_voice_assistant_speech(farewells[random.randint(0, len(farewells) - 1)])
    ttsEngine.stop()
    quit()
class Translation:
    with open("translation.json", "r") as file:
        translations = json.load(file)

    def get(self, text: str):
        if text in self.translations:
            return self.translations[text][assistant.speech_language]
        else:
            print(colored("Not translated phrase: {}".format(text), "red"))
            return text

class OwnerPerson:
    name = ""
    home_city = ""
    native_language = ""
    target_language = ""

class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "ru":
        assistant.recognition_language = "ru-RU"
        if assistant.sex == "female":
            ttsEngine.setProperty("rate", 190)
        else:
            ttsEngine.setProperty("rate", 190)
    else:
        assistant.recognition_language = "en-EN"
        ttsEngine.setProperty("rate", 190)

def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""

        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, None, 5)

            with open("microphone_res.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            play_voice_assistant_speech(translator.get("Can u check if your mic is on, please?"))
            traceback.print_exc()
            return

        try:
            print("started recognition...")
            recognized_data = recognizer.recognize_google(audio, language=assistant.recognition_language).lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print(colored("check your internet connection, please", "cyan"))
            recognized_data = use_offline_recognition()
        return recognized_data

def use_offline_recognition():
    recognized_data = ""
    try:
        if not os.path.exists("models/vosk-model-small-ru-0.4"):
            print("pls download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        wave_audio_file = wave.open("microphone-res.wav", "rb")
        model = Model("model/vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        traceback.print_exc()
        print(colored("sorry, speech service is unavailable. try again later", "red"))
    return recognized_data

def execute_command_with_name(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass
def search_for_term_on_google(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])

    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    search_result = []
    try:
        for _ in search(search_term, tld="com", lang=assistant.speech_language, num=1, start=0, stop=1, pause=1.0):
            search_result.append(_)
            webbrowser.get().open(_)
    except:
        play_voice_assistant_speech("Seems like we have a trouble. See logs for more information")
        traceback.print_exc()
        return
    print(search_result)
    play_voice_assistant_speech("Here is what I found for {} on google".format(search_term))

def search_for_video_on_youtube(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech("Here is what I found for {} on youtube".format(search_term))


def search_for_definition_on_wikipedia(*args: tuple):
    if not args[0]:
        return
    search_term = " ".join(args[0])

    wiki = wikipediaapi.Wikipedia(headers, assistant.speech_language)
    wiki_page = wiki.page(search_term)

    try:
        if wiki_page.exists():
            play_voice_assistant_speech("Here is what I found for {} on Wikipedia".format(search_term))
            webbrowser.get().open(wiki_page.fullurl)
            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            play_voice_assistant_speech("Can't find {} on Wikipedia. But here is what I found on google".format(search_term))
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
    except:
        play_voice_assistant_speech("Seems like we have a trouble. See logs for more information")
        traceback.print_exc()
        return

def get_weather_forecast(arg):
    temp, weather, wind = weather_info()
    print(colored("Weather in " + "Saint-Petersburg" + ":\n * Status: " + weather +
                  "\n * Wind speed (m/sec): " + wind +
                  "\n * Temperature (Celsius): " + temp, "green"))

    play_voice_assistant_speech(("It is {0} in {1}").format(weather, "Saint-Petersburg"))
    play_voice_assistant_speech(("The temperature is {} degrees Celsius").format(str(temp)))
    play_voice_assistant_speech(("The wind speed is {} meters per second").format(str(wind)))
    #play_voice_assistant_speech(translator.get("The pressure is {} mm Hg").format(str(pres)))

def acquaintance(*args: tuple):
    if not args[0]:
        return
    play_voice_assistant_speech("Hi, I'm Chris. I'm a voice assistant written in Python. This is a project created by Vlad Kucher.")


def Openai(*args: tuple):
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI()
    if not args[0]: return

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a assistant"},
            {"role": "user", "content": "{}".format(args[0])}

        ]
    )
    print(colored(completion.choices[0].message.content, 'green'))
    play_voice_assistant_speech(completion.choices[0].message.content)


def run_person_through_social_nets_databases(*args: tuple):
    if not args[0]: return
    google_search_term = " ".join(args[0])
    vk_search_term = "_".join(args[0])

    url = "https://google.com/search?q=" + google_search_term + "site: vk.com"
    webbrowser.get().open(url)

    vk_url = "https://vk.com/people/" + vk_search_term
    webbrowser.get().open(vk_url)

    play_voice_assistant_speech("Here is what I found on social nets")

def change_language(*args: tuple):
    assistant.speech_language = "ru" if assistant.speech_language == "en" else "en"
    setup_assistant_voice()
    print("Language switched to " + assistant.speech_language)

def what_time(*args: tuple):
    day_of_week = time.strftime("%A")
    date = time.strftime("%d-%B-%Y")
    hour, min = time.strftime("%H:%M").split(':')
    print(day_of_week, '\n', date, '\n', hour+':'+min)
    play_voice_assistant_speech(day_of_week)
    time.sleep(0.5)
    play_voice_assistant_speech(date)
    time.sleep(0.5)
    play_voice_assistant_speech("{} hours".format(hour))
    play_voice_assistant_speech("{} minutes".format(min))




commands = {
    ("hello", "hi", "morning", "привет"): play_greetings,
    ("bye", "goodbye", "quit", "exit", "stop", "пока", "стоп"): play_farewell_and_quit,
    ("weather", "forecast", "погода", "прогноз"): get_weather_forecast,
    ("video", "youtube", "watch", "видео"): search_for_video_on_youtube,
    ("search", "google", "find", "найди"): search_for_term_on_google,
    ("wikipedia", "wiki", "вики", "википедия"): search_for_definition_on_wikipedia,
    ("tell us about yourself", "расскажи о себе") : acquaintance,
    ("gpt", "нейронка"): Openai,
    ("вк", "person", "run", "пробей", "контакт"): run_person_through_social_nets_databases,
    ("language", "язык"): change_language,
    ("time", "время"): what_time,
}
'''
    ("translate", "interpretation", "translation", "перевод", "перевести", "переведи"): get_translation,
    ("toss", "coin", "монета", "подбрось"): toss_coin,
'''

if __name__ == '__main__':
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    ttsEngine = pyttsx3.init()
    headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

    person = OwnerPerson()
    person.name = "Vlad"
    person.home_city = "Saint-Petersburg"
    person.native_language = "ru"
    person.target_language = "en"

    assistant = VoiceAssistant()
    assistant.name = "Kris"
    assistant.sex = "female"
    assistant.speech_language = "en"

    setup_assistant_voice()
    translator = Translation()
    play_greetings()
    while True:
        voice_input = record_and_recognize_audio()
        os.remove("microphone_res.wav")
        print(voice_input)

        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)
        time.sleep(1)
