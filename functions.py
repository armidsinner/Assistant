import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('алина', 'алиночка', 'дорогая', 'милая', 'алин',
              'элин', 'алян', 'олина', 'элина', 'али'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "vodka": ('закажи водки', 'где водка'),
        "play": ('давай послушаем музыку'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()



def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("Голос не распознан!")
    except sr.RequestError as e:
        print("Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'vodka':
        speak('Алкаш')

# Блок функции воспроизведения из ск

    elif cmd == 'play':
        speak('Будем слушать старую музыку или найдем то-то новое?')
        # Тело функции взаимодействия с ск. Открыть в браузере саунклауд. Если новое, то спросить жанр, если старое
        # Воспроизвести понравившиеся треки. После выбора жанра прочитать название первого трека, если да, воспроизвести
        # Если нет - следующий трек





    else:
        print('Команда не распознана, повторите!')
    speak_engine.endLoop()

# запуск
r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)


speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')


# voices = engine.getProperty('voices')
# for voice in voices:
#     print("Voice:")
#     print(" - ID: %s" % voice.id)
#     print(" - Name: %s" % voice.name)
#     print(" - Languages: %s" % voice.languages)
#     print(" - Gender: %s" % voice.gender)
#     print(" - Age: %s" % voice.age)

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.yuri')


speak("Че тебе надо?")

stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)  # infinity loop