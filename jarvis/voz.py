import speech_recognition as sr
import pyttsx3
from interface import estado_microfone, atualizar_texto_voz

engine = pyttsx3.init()

def falar(texto):
    print("Jarvis:", texto)
    engine.say(texto)
    engine.runAndWait()

def ouvir():

    r = sr.Recognizer()

    with sr.Microphone(device_index=12) as source:

        estado_microfone("listening")

        print("🎤 Ouvindo...")

        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            estado_microfone("idle")
            return ""

    estado_microfone("idle")

    try:

        comando = r.recognize_google(audio, language="pt-BR")

        print("Você disse:", comando)

        atualizar_texto_voz(comando)

        return comando.lower()

    except:
        return ""