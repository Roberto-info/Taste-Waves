import React, { Component } from "react";
import { axios } from "../axios";

class FileUpload extends Component {
  state = {
      file: null
  };

    handleFile = (e) => {
        let file = e.target.files[0];
        console.log(file);
        this.setState({file: file});
    }

    handleUpload = async () => {
        let file = this.state.file;
        let formData = new FormData();

        formData.append('file', file, file.name);
        
        const res = await axios.post('/upload', formData).catch((err) => {
            console.log(err);
        });
        
        console.log(res.data);
       
    }


  render() {
    return (
      <div>
        <h3>Taste Waves</h3>
        <form>
          <div>
            <label>File Select</label>
            <input type="file" name="file" onChange={this.handleFile}></input>
          </div>
          <button type="button" onClick={this.handleUpload}>Send File</button>
        </form>
      </div>
    );
  }
}

export default FileUpload;
