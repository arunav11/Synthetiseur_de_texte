import requests
from summa.summarizer import summarize

import speech_recognition as sr
import moviepy.editor as mp
import os


def backend(url):
    # get the video from s3 using the url

    r = requests.get(url, allow_redirects=True)

    open('upload//testvideolecture.mp4', 'wb').write(r.content)
    # convert video to audio
    clip = mp.VideoFileClip(r"upload//testvideolecture.mp4")

    # Insert Local Audio File Path
    clip.audio.write_audiofile(r"upload//testvideolecture-1.wav")

    # convert audio to text using google speech to text api

    # give path for the audio file
    filename = "upload//testvideolecture-1.wav"

    text = convert_to_text(filename)

    text1 = refine_text(text)
    text = text1

    punctuatedText = punctuate_text(text)
    questionList = generate_questions(text, punctuatedText)
    print("Questions are:", questionList)
    print("/n")

    text = generate_summary(punctuatedText)
    text = addIndentation(text)
    save_summary(text)

    print("function called")
    print("ran1")


def generate_questions(text, pText):
    textL = text.split(" ")
    textS = list(set(textL))

    keywords = []
    for i in range(len(textL) // 20 + 1):
        word = max(set(textS), key=textL.count)
        keywords.append(word)
        textS.remove(word)
    for word in keywords:
        pText = pText.replace(word, "_" * len(word))
    # pText -> punctuated text with blanks
    # keywords -> word bank
    questions = []
    pTextL = pText.replace("?", ".").replace("!", ".").split(". ")
    for t in pTextL:
        if t.find("__") != -1:
            questions.append(t)
    return questions


def punctuate_text(text):
    punctuated_text = os.popen('curl -d "text={}" http://bark.phon.ioc.ee/punctuator'.format(text))
    punctuatedText = punctuated_text.read()
    return punctuatedText


def generate_summary(text):
    text = summarize(text, ratio=0.9)
    return text


def addIndentation(text):
    text = text.split(' ')
    line_length = 0
    index = 0

    for word in text:
        if (line_length + len(word)) < 70:
            index += 1
            line_length += len(word) + 1
        else:
            text.insert(index, '\n')
            index += 2
            line_length = len(word) + 1

    text = ' '.join(text)
    return text


def refine_text(text):
    list1 = ["very", "so", "pretty", "always", "the", "are", "is", "but",
             "and", "for", "in", "they", "a"]
    for word in list1:
        text1 = text.replace(" " + word + " ", " ")
    return text1


def convert_to_text(filename):
    r = sr.Recognizer()
    text1 = ""

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        text1 = text1 + " " + text
        return text1


def save_summary(text):
    f = open("upload//Summary.txt", "a")

    f.write(text)

    f.close()


def save_questions(question_list):
    with open('questions.txt', 'w') as f:
        for item in question_list:
            if not item == '':
                for i in item:
                    f.write("%s\n" % i)
            else:
                f.write("%s\n" % item)

