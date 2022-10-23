
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

#Main Route um zu testen, ob die API ueberhaupt funktioniert
@app.route('/')
def main():
    return 'penis'
#Upload Route um das File auch hochzuladen
@app.route('/upload', methods=['POST'])

#Funktion welche den Upload handled
def upload():
    file = request.files['file']#Das file wird entgegen genommen 

    if file: #Falls das File gesetzt ist wird es abgelegt 

        filename = secure_filename(file.filename) #Der Name wird sicher abgespeichert 

        file.save(os.path.join('static/uploads', filename)) #Das File wird gespeichert

        vid = VideoFileClip('static/uploads/'+filename) #Das File wird nochmals geholt 
        audio = vid.audio

        defName = filename.split('.')[0]
        audio.write_audiofile('mat/audio/'+defName+'.wav') #Das Audio File wird erstellt 



        audio_file = AudioSegment.from_wav(open("mat/audio/"+defName+".wav", "rb")) #Ein bearbeitbare Form des Audios wird erstellt 
        audio_file = audio_file.split_to_mono() #Es wird nur ein Kanal benoetigt deswegen werden die Mono Daten genommen
        data = audio_file[0]._data
        data_values = []

        #Die Daten welche wir aus dem Audio File erhalten haben werden nun in Integers verwandelt 
        for sample_index in range(len(data) // 2):
            sample = int.from_bytes(data[sample_index * 2: sample_index * 2 + 2], 'little', signed=True) 
            data_values.append(sample)
        
        
        sample_size = 70
        
        #Aus der gesamt Laenge des Integer Array wird benoetigt um die Block laenge zu ermitteln 
        block_size = math.floor(len(data_values) / sample_size)

        half_filtered_data = []
        filtered_data = []
        
        #Die Block laenge wird genutzt um einen kleineren Datensatzt zu erhalten
        for i in range(sample_size):
            half_filtered_data.append(data_values[i * block_size])

        #Die Daten werden nun verkleinert 
        for j in range(sample_size):
            filtered_data.append(abs(math.ceil(half_filtered_data[j] / 10)))
        
        print (len(filtered_data))
        print (filtered_data)

        #Die Daten werden nun zurueck an den Client gesendet
        return filtered_data
    else:
        return 'No file attached'

if __name__ == '__main__':
    app.run(debug=True)