import React, { Component } from "react";
import { axios } from "../axios";

class FileUpload extends Component {
  state = {
      file: null
  };

    handleFile = (e) => {
        let file = e.target.file[0];
        this.setState({file: file});
    }

    handleUpload = () => {
        let file = this.state.file;
        let formData = new FormData();

        formData.append('video', file);
        
        const res = await axios.post('/uploads', formData).catch((err) => {
            console.log(err);
        })
    }


  render() {
    return (
      <div>
        <h3>Taste Waves</h3>
        <form>
          <div>
            <label>File Select</label>
            <input type="file" name="file" onChange={(e) => this.handleFile(e)}></input>
          </div>
          <button type="button">Send File</button>
        </form>
      </div>
    );
  }
}

export default FileUpload;
