import sys,os
import tensorflow as tf
from flasker import app
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g,json
from google.cloud import translate
import six

@app.route('/', methods=['GET', 'POST'])
def compose_page():
    trans_entries = []
    translate_trans = []
    if request.method == 'POST':
        path = request.form['gcs_uri']
        trans_entries = transcribe_gcs('gs://hackthenorth-text/'+path+".wav")
        if request.form['language'] != "None":
            translate_trans = translate_gcs(trans_entries, request.form['language'])
        else:
            translate_trans = ""

    return render_template('compose.html', entries = trans_entries, translate = translate_trans)


# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    trans = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
        trans.append(result.alternatives[0].transcript)

    return trans
# [END speech_transcribe_async_gcs]


def translate_gcs(texts, target):
    translate_client = translate.Client()
    texts_decode = []
    for text in texts:
        text = text.encode('utf-8')
        if isinstance(text, six.binary_type):
            texts_decode += [text.decode('utf-8')]

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = []
    for text in texts_decode:
        result.append(translate_client.translate(
            text, target_language=target)['translatedText'])
    return result