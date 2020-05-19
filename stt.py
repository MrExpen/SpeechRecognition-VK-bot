# -*- coding: utf-8 -*-

import speech_recognition as sr
import subprocess
import os


def stt(file: str):
    """
    return a text
    :param file:
    :return: str
    """
    def remake(path: str):
        process = subprocess.run(['ffmpeg.exe', '-y', '-i', path, path[:-3] + 'wav'], capture_output=True)
        return path[:-3] + 'wav'

    r = sr.Recognizer()
    with sr.AudioFile(remake(file)) as source:
        audio = r.listen(source)
    os.remove(file)
    os.remove(file[:-3] + 'wav')
    try:
        text = r.recognize_google(audio, language='ru-RU')
        return str(text)
    except:
        return None