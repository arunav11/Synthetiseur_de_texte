import requests
from summa.summarizer import summarize

import speech_recognition as sr
import moviepy.editor as mp


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

    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        # add appropriate spaces in between the text
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
        print(text + "\n" + "before")

        text2 = text

        # summarize the lecture using summa library
        text = summarize(text2, ratio=0.9)
        print(text)
        # write the file to summary.txt
        f = open("upload//Summary.txt", "a")

        f.write(text)

        f.close()
        print("function called")
