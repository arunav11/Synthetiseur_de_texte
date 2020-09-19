import os
import youtube_dl
import moviepy.editor as mp
import requests
import speech_recognition as sr
from summa.summarizer import summarize


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
    questions: list = []
    pTextL = pText.replace("?", ".").replace("!", ".").split(". ")
    for t in pTextL:
        if t.find("__") != -1:
            questions.append(str(t))
    return questions


def punctuate_text(text):
    punctuated_text = os.popen('curl -d "text={}" http://bark.phon.ioc.ee/punctuator'.format(text))
    punctuatedText = punctuated_text.read()
    return punctuatedText


def generate_summary(text):
    text = summarize(text, ratio=0.7)
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
        text = text.replace(" " + word + " ", ", ")
    return text


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
    f = open("upload//Summary.txt", "w+")

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


def get_summary_from_youtube_link(url):
    filename = "file_name"
    audio = "file_name.wav"
    ydl_opts = {'outtmpl': 'file_name.mp4'}

    zxt = url.strip()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([zxt])

    clip = mp.VideoFileClip(r"file_name.mp4")

    # Insert Local Audio File Path
    clip.audio.write_audiofile(audio)

    clip.close()

    text = convert_to_text(audio)
    text = refine_text(text)
    punctuated_text = punctuate_text(text)
    question_list = generate_questions(text, punctuated_text)

    summary = generate_summary(punctuated_text)
    summary = addIndentation(summary)
    compression_ratio = (len(summary) / len(text)) * 100

    try:
        os.remove(filename + ".wav")
        os.remove(filename + ".mp4")
    except Exception as exc:
        print("Exception occurred: ", str(exc))
        pass

    original_text = punctuated_text
    print(original_text)
    # return [original_text, summary, question_list, compression_ratio]


# get_summary_from_youtube_link("https://youtu.be/5N2u_Mty13A")

def extract_summary_from_media_file(url: str) -> list:
    FILE_NAME = url.split("/")[-1].split(".")[0]
    EXTENSTION = url.split("/")[-1].split(".")[1]

    print('{}.{}'.format(FILE_NAME, EXTENSTION))
    # get the video from s3 using the url
    r = requests.get(url, allow_redirects=True)

    open('upload//{}.{}'.format(FILE_NAME, EXTENSTION), 'wb').write(r.content)

    # give path for the audio file
    filename = 'upload//{}.{}'.format(FILE_NAME, "wav")

    if EXTENSTION == "mp4":
        # convert video to audio
        clip = mp.VideoFileClip(r"upload//{}.{}".format(FILE_NAME, EXTENSTION))

        # Insert Local Audio File Path
        clip.audio.write_audiofile(filename)
        clip.close()

    text = convert_to_text(filename)
    text = refine_text(text)
    punctuated_text = punctuate_text(text)
    question_list = generate_questions(text, punctuated_text)

    summary = generate_summary(punctuated_text)
    summary = addIndentation(summary)
    compression_ratio = (len(summary) / len(text)) * 100

    try:
        os.remove(filename)
        os.remove('upload//{}.{}'.format(FILE_NAME, EXTENSTION))
    except Exception as exc:
        print("Exception occurred: ", str(exc))
        pass

    original_text = punctuated_text
    return [original_text, summary, question_list, compression_ratio]
