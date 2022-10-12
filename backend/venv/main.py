
from flask import Flask, flash, request, json, jsonify  #Basis API Importe
from werkzeug.utils import secure_filename  #Import um das File auch richtig abzuspeichern
import moviepy.editor as mp #Import um das Audio aus dem Video zu extrahieren
import glob2 as glb #Import um zu pruefen, welches File das neuste ist
import os #Um das File welches eintrift zu speichern

#Einstieg in die API 
app = Flask(__name__)


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
    #Wenn kein File gesendet wird
    if 'files[]' not in request.files:
        #Response Text wird gesetzt
        resp = jsonify({'message' : 'No file found sucker'})
        #Status Code wird gesetzt
        resp.status_code = 400
        #Response wird zurueck gegeben
        return resp
    #Files repraesentiert die gesendeten Files
    files = request.files.getlist('files[]')
    
    #Error wird vorbereitet
    errors = {}
    #Je nach Ergebnis muss ein anderer Fall abgedekt werden dafuer gibt es einen Boolischen Wert zur ueberpruefung
    success = False
  
    #Geht die alle gesendeten Files durch
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/uploads', filename))  
            getLatestFile()
            success = True
        else:
            errors[file.filename] = 'file is not allowed'
    
    if success and errors:
        errors['message'] = 'Files uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files uploaded'})
        resp.status_code = 201

        return resp
    else: 
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

#def extract_audio(file):
 #   clip = mp.VideoFileClip(file)
  #  clip.audio.write_audiofile('test.mp3')

def getLatestFile():
    list_of_files = glb.glob('static/uploads/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file.split('\\')[1])

if __name__ == '__main__':
    app.run(debug=True)