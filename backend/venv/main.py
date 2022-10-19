
from asyncio.windows_events import NULL
from flask import Flask, flash, request, json, jsonify, send_file, send_from_directory  #Basis API Importe
from werkzeug.utils import secure_filename  #Import um das File auch richtig abzuspeichern
from flask_cors import CORS #Inportiert CORS um Cross-Origin Resource Sharing zu erlauben
from moviepy.editor import * #Import um das Audio aus dem Video zu extrahieren
from pydub import AudioSegment
import math
import os #Um das File welches eintrift zu speichern

#Einstieg in die API 
app = Flask(__name__)
CORS(app)


ALLOWED_EXTENSIONS = set(['mp4', 'mov', 'wmv', 'avi', 'avchd', 'webm', 'flv', 'f4v']) #Liste der erlaubten Files

#Funktion welche die Fileextension abfragt
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Main Route um zu testen, ob die API ueberhaupt funktioniert
@app.route('/')
def main():
    return 'penis'
#Upload Route um das File auch hochzuladen
@app.route('/upload', methods=['POST'])

#Funktion welche den Upload handled
def upload():
    file = request.files['file']

    if file:

        filename = secure_filename(file.filename)

        file.save(os.path.join('static/uploads', filename))

        vid = VideoFileClip('static/uploads/'+filename)
        audio = vid.audio

        defName = filename.split('.')[0]
        audio.write_audiofile('mat/audio/'+defName+'.wav')



        audio_file = AudioSegment.from_wav(open("mat/audio/"+defName+".wav", "rb"))
        audio_file = audio_file.split_to_mono()
        data = audio_file[0]._data
        data_values = []

        for sample_index in range(len(data) // 2):
            sample = int.from_bytes(data[sample_index * 2: sample_index * 2 + 2], 'little', signed=True) 
            data_values.append(sample)

        sample_size = 70
        

        print (len(data_values))

        return data_values
    else:
        return 'No file attached'

#def extract_audio(file):
 #   clip = mp.VideoFileClip(file)
  #  clip.audio.write_audiofile('test.mp3')
  
if __name__ == '__main__':
    app.run(debug=True)