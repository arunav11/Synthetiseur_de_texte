import os
import random
import re

import moviepy.editor as mp
import requests
import speech_recognition as sr
import youtube_dl
from summa.summarizer import summarize
from textblob import TextBlob


def generate_questions():
    file1 = open("upload//Original.txt", "r+", encoding="utf-8")
    ww2 = file1.read()
    ww2b = TextBlob(ww2)
    sposs = {}
    questions = []
    for sentence in ww2b.sentences:

        # We are going to prepare the dictionary of parts-of-speech as the key and value is a list of words:
        # {part-of-speech: [word1, word2]}
        # We are basically grouping the words based on the parts-of-speech
        poss = {}
        sposs[sentence.string] = poss;
        for t in sentence.tags:
            tag = t[1]
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(t[0])

    # Create the blank in string
    def replace_ic(word, sentence):
        insensitive_hippo = re.compile(re.escape(word), re.IGNORECASE)
        return insensitive_hippo.sub('__________________', sentence)

    # For a sentence create a blank space.
    # It first tries to randomly selection proper-noun
    # and if the proper noun is not found, it selects a noun randomly.
    def remove_word(sentence, poss):
        words = None
        if 'NNP' in poss:
            words = poss['NNP']
        elif 'NN' in poss:
            words = poss['NN']
        else:
            # print("NN and NNP not found")
            return None, sentence, None
        if len(words) > 0:
            word = random.choice(words)
            replaced = replace_ic(word, sentence)
            return word, sentence, replaced
        else:
            print("words are empty")
            return None, sentence, None

    for sentence in sposs.keys():
        poss = sposs[sentence]
        (word, osentence, replaced) = remove_word(sentence, poss)
        if replaced is None:
            # print("Founded none for ")
            # print(sentence)
            pass
        else:
            # print(replaced)
            questions.append(replaced)
            # print(" $ ")
            # print("Ans: " + word)
            # print(" $ ")
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


def save_original(text):
    f = open("upload//Original.txt", "w+")

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
    print("Current Working Directory: ", os.getcwd())
    filename = os.getcwd() + "/temp_file"
    audio = os.getcwd() + "/temp_file.wav"
    ydl_opts = {
        'outtmpl': filename,
        'format': 'worstvideo[filesize<50M] + bestaudio/best[filesize<50M]',
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'wav',
        #     'preferredquality': '192'
        # }],
        # 'postprocessor_args': [
        #     '-ar', '16000'
        # ],
        'prefer_ffmpeg': True,
    }

    zxt = url.strip()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([zxt])

    clip = mp.VideoFileClip(filename + ".mkv")

    # Insert Local Audio File Path
    clip.audio.write_audiofile(audio)

    clip.close()

    text = convert_to_text(audio)
    text = refine_text(text)
    punctuated_text = punctuate_text(text)

    summary = generate_summary(punctuated_text)
    summary = addIndentation(summary)
    compression_ratio = (len(summary) / len(text)) * 100

    try:
        pass
        os.remove(audio)
        os.remove(filename + ".mkv")
    except Exception as exc:
        print("Exception occurred: ", str(exc))
        pass

    original_text = punctuated_text
    save_summary(summary)
    save_original(original_text)
    question_list = generate_questions()
    return [original_text, summary, question_list, compression_ratio]


# get_summary_from_youtube_link("https://youtu.be/pWwMmHVUCZ8")

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
    save_summary(summary)
    save_original(original_text)
    question_list = generate_questions()

    return [original_text, summary, question_list, compression_ratio]
