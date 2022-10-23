import FileUpload from "./components/file_upload";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import "./app_style.css"

function App() {
  return <div className="App">
    <FileUpload className="file_upload"></FileUpload>
    </div>;
}

export default App;
