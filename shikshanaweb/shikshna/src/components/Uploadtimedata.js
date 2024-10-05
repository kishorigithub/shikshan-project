import { useEffect, useState } from "react";
import Headertwo from "./Headertwo";
import docPreview from "../images/docpreview.jpg"; // Adjust the path based on the image location
import browseImage from "../images/browse.jpg";
import axios from "axios";
import { ipofserver } from "./Global";

const Uploadtimedata = () => {
  const options = [
    { label: "Select standard", value: "" },
    { label: "1st standard", value: "1st" },
    { label: "2nd standard", value: "2nd" },
    { label: "3rd standard", value: "3rd" },
    { label: "4th standard", value: "4th" },
    { label: "5th standard", value: "5th" },
  ];
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const username = localStorage.getItem("teacherloginusername");
    if (username) {
      setIsLoggedIn(true);
    }
    document.body.style.backgroundImage = "none";
    document.body.style.backgroundSize = "none";
    document.body.classList.add("remove-before-style");

    // Cleanup the effect when the component unmounts to restore the style for other pages
    return () => {
      document.body.classList.remove("remove-before-style");
    };
  }, []);

  const [inputField, setInputField] = useState({
    name: "",
  });

  const [selectedValue, setSelectedValue] = useState("");

  function clearInput() {
    setInputField({
      name: "",
    });
    setFile(null);
    setSelectedFile("");
    setSelectedValue("");
  }

  const inputsHandler = (e) => {
    const { name, value } = e.target;
    setInputField((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const [file, setFile] = useState();
  const [selectedFile, setSelectedFile] = useState();

  function handleChange(e) {
    var file = e.target.files[0];
    var fileName = file.name;
    var fileExtension = fileName.split(".").pop();
    console.log("File extension:", fileExtension);

    if (
      fileExtension == "jpg" ||
      fileExtension == "png" ||
      fileExtension == "jpeg"
    ) {
      setFile(URL.createObjectURL(e.target.files[0]));
      setSelectedFile(e.target.files[0]);
    } else {
      setFile(docPreview);
      setSelectedFile(e.target.files[0]);
    }
  }

  const handleSelectChange = (e) => {
    setSelectedValue(e.target.value);
  };

  const handleSubmission = async () => {
    // console.log(isFilePicked);
    if (selectedFile == undefined || inputField.name == '' || selectedValue == '') {
      alert("Please fill all details !") // eslint-disable-line no-alert
    }
    else {

      const formData = new FormData();

      formData.append('File', selectedFile);
      formData.append('title', inputField.name);
      formData.append('standard', selectedValue);

      const res = await axios.post(`${ipofserver}uploadTimeTable`, formData);

      if (res.data == "success") {
        alert("Timetable uploaded sucessfully !")
        clearInput()
      }
      else if(res.data == "exist") {
        alert("Timetable already uploaded!")
      }
      else {
        alert("Timetable not uploaded !")
      }

    }
  };


  return (
    <div>
      <div className="background-image"></div>
      {isLoggedIn && <Headertwo />}
      <div className="content">
        <center>
          <h2>UPLOAD TIME TABLE DATA</h2>
        </center>
        <div className="App">
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              marginBottom: 20,
            }}
          >
            <label htmlFor="file1">
              <img src={file == null ? browseImage : file} />
            </label>
          </div>
          <input type="file" id="file1" onChange={handleChange} hidden />
        </div>
        <center>
          <input
            placeholder="Title of Timetable"
            name="name"
            value={inputField.name}
            onChange={inputsHandler}
          ></input>
        </center>
        <br></br>

        <center>
          <select
            name="standard"
            value={selectedValue}
            onChange={handleSelectChange}
          >
            {options.map((option, index) => (
              <option key={index} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </center>

        <br></br>

        <center><button onClick={handleSubmission}>Upload TimeTable</button></center>
      </div>
    </div>
  );
};

export default Uploadtimedata;
