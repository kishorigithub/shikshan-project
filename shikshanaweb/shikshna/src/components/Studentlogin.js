import { Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { ipofserver } from "./Global";

const Studentlogin = () => {
  const [inputField, setInputField] = useState({
    userid: "",
    username: "",
    password: "",
  });

  const inputsHandler = (e) => {
    const { name, value } = e.target;
    setInputField((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const [selectedValue, setSelectedValue] = useState("1st");

  const handleSelectChange = (e) => {
    setSelectedValue(e.target.value);
  };

  const options = [
    { label: "Select standard", value: "" },
    { label: "1st standard", value: "1st" },
    { label: "2nd standard", value: "2nd" },
    { label: "3rd standard", value: "3rd" },
    { label: "4th standard", value: "4th" },
    { label: "5th standard", value: "5th" },
  ];

  function setData(sessionname,standard) {
    localStorage.setItem('LoginUsername', sessionname);
    localStorage.setItem('LoginUserstd', standard);
  }

  const submitButton = () => {
    // alert(inputField.password)
    if (
      inputField.username == "" ||
      inputField.password == "" ||
      selectedValue == "" ||
      inputField.userid == ""
    ) {
      alert("Please enter all details !");
      // clearInput()
    } else {
      axios
        .post(ipofserver + "studentlogin", {
          userid: inputField.userid,
          username: inputField.username,
          password: inputField.password,
          standard: selectedValue,
          typeofuser: "User",
        })
        .then(function (response) {
          if (response.data == "success") {
            setData(inputField.username, selectedValue);
            window.location.href = "/syllabus";
          } else {
            alert("Invalid username and password !");
          }
        })
        .catch(function (error) {
          return error;
        });
    }
  };
  return (
    <div>
      <br></br>
      <center>
        <div className="form-container">
          {/* <form> */}
          <div className="form">
            <h2>Student SignIn</h2>
            <input
              placeholder="User Id"
              name="userid"
              value={inputField.userid}
              onChange={inputsHandler}
            ></input>
            <br />
            <br />
            <input
              placeholder="Username"
              name="username"
              value={inputField.username}
              onChange={inputsHandler}
            ></input>
            <br />
            <br />
            <input
              placeholder="Password"
              name="password"
              value={inputField.password}
              onChange={inputsHandler}
            ></input>
            <br />
            <br />
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
            <br />
            <br />

            <Link to="/studentregister">
              You dont Have An Account? Register Here
            </Link>
            <br></br>
            <br></br>
            <button onClick={submitButton}>Sign In</button>
          {/* </form> */}
          </div>
        </div>
      </center>
    </div>
  );
};

export default Studentlogin;
