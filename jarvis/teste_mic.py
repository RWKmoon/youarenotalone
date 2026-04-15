import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=12) as source:
    print("Fale algo...")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)

print("Reconhecendo...")

try:
    texto = r.recognize_google(audio, language="pt-BR")
    print("Você disse:", texto)
except Exception as e:
    print("Erro:", e)