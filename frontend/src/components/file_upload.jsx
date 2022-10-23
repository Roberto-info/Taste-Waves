import React, { Component } from "react";
import { axios } from "../axios";
import './file_upload_style.css'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import wave from "./wave.png"

//Der State wird genutzt um Daten kurzfristig zu speichern und um diese an andere Komponenten weiter zu geben
class FileUpload extends Component {
  state = {
    file: null
  };

  //Hier wird der State auf das File gesetzt 
  handleFile = (e) => {
    let file = e.target.files[0];
    console.log(file);
    this.setState({ file: file });
  }

  //Wenn der Senden Button gedrueckt wird, wird ein File ueber Post an die API gesendet 
  handleUpload = async () => {
    let file = this.state.file;
    let formData = new FormData();

    formData.append('file', file, file.name);

    const res = await axios.post('/upload', formData).catch((err) => {
      console.log(err);
    });

    console.log(res.data);
    //Wenn die Response erhalten wurde wird die Kurve gezeichnet 
    this.createCanvas(res.data);
  }

  //Diese Funktion zeichnet die Kurve
  createCanvas = (data) => {

    const canvas = document.getElementById('canvas')
    //Um die Kurve dem Bildschirm entsprechend gezeichnet wird 
    const dpr = window.devicePixelRatio || 1;
    const padding = 20;
    canvas.width = canvas.offsetWidth * dpr;
    canvas.height = (canvas.offsetHeight + padding * 2) * dpr;
    //Hoehe und Breite wird nach dem Bildschirm Mas gezeichnet
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    //Hiermit wird die Mitte des Canvas auf das optische Zentrum gesetzt 
    ctx.translate(0, canvas.offsetHeight / 2 + padding);
    const width = canvas.offsetWidth / data.length;

    for (let i = 0; i < data.length; i++) {
      const x = width * i;

      let height = data[i];
      if (height < 0) {
        height = 0;
      } else if (height > canvas.offsetHeight / 2) {
        height = height > canvas.offsetHeight / 2;
      }
      //Die Kurve wird hier dann richtig gezeichnet
      this.drawLineSegment(ctx, x, height, width, (i + 1) % 2);
    }
    //Dieser Teil ist fuer den Download verantwortlich
    var link = document.createElement('a');
    link.download = 'filename.png';
    link.href = document.getElementById('canvas').toDataURL()
    link.click();
  }
  //Hier wird gezeichnet
  drawLineSegment = (ctx, x, y, width, isEven) => {
    ctx.lineWidth = 2; //Linien dicke
    ctx.strokeStyle = "#fff"; // Farbe der Kurve
    ctx.beginPath(); 
    y = isEven ? y : -y; //Wenn die Zahl gerade ist geht die Kurve nach Oben ansonsten nach unten 
    ctx.moveTo(x, 0);
    ctx.lineTo(x, y);
    ctx.arc(x + width / 2, y, width / 2, Math.PI, 0, isEven);
    ctx.lineTo(x + width, 0);
    ctx.stroke();
  };
  //HTML Code zur strukturierung der Seite 
  render() {
    return (
      <div className="upload">
        <div className="title">
          <img src={wave} alt="" className="img2" />
          <h2>Taste Waves</h2>
          <img src={wave} alt="" className="img1" />
        </div>
        <div className="text">
          <p>Here you can taste your favorite video's audio, just upload your video here and press send</p>
        </div>
        <form>
          <div className="form">
            <label htmlFor="file-upload" className="custom-file-upload">
              <i className="fa fa-cloud-upload"></i> Upload
            </label>
            <input type="file" name="file" id="file-upload" onChange={this.handleFile}></input>
            <button type="button" onClick={this.handleUpload} className="send">Send File</button>
          </div>
        </form>
        <canvas id="canvas" className="canvas"></canvas>
      </div>
    );
  }
}

export default FileUpload;
