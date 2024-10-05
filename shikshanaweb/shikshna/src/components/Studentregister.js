import { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { ipofserver } from "./Global";
const Studentregister = () => {

  const [inputField,setinputField]=useState({
    userid:'',
    username:'',
    email:'',
    mobile:'',
    password:''

  })

  const [selectedValue, setSelectedValue] = useState('');

  const handleSelectChange = (e) => {
    setSelectedValue(e.target.value);  // Update selected value for the standard
  };

  const options = [
    { label: "Select standard", value: "" },
    { label: "1st standard", value: "1st" },
    { label: "2nd standard", value: "2nd" },
    { label: "3rd standard", value: "3rd" },
    { label: "4th standard", value: "4th" },
    { label: "5th standard", value: "5th" }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setinputField({ ...inputField, [name]: value });
  };

  const submitButton=(e)=>{
    e.preventDefault();
    var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    if(inputField.userid==='' || inputField.username===''|| inputField.email===''|| inputField.mobile===''|| inputField.password===''|| selectedValue==='' ){
      alert("Please fill all the required fields")
    }
    else if (inputField.userid.length != 6) {
      alert("Please enter valid userid !")
      // clearInput()
    }
    else if (inputField.mobile.length != 10) {
      alert("Please enter valid mobile number !")
      // clearInput()
    }
    else if (!filter.test(inputField.email)) {
      alert("Please enter valid email !")
      // clearInput()
    }
    else {
      // alert(inputField.username + " " + inputField.email + " " + inputField.mobile + " " + inputField.password + " " + inputField.email + " " + selectedValue)
      axios.post(ipofserver + 'studentRegister', {
        userid: inputField.userid,
        username: inputField.username,
        email: inputField.email,
        mobile: inputField.mobile,
        password: inputField.password,
        standard: selectedValue,
        status: "Un-Verified"
      })
        .then(function (response) {
          // alert(typeof(response.data))
          if (response.data === "success") {
            alert("Student added successfully !")
            window.location.href = '/authentication/sign-in'
          }
          else {
            alert("Student already exist !")
          }
        })
        .catch(function (error) {
          return error;
        });
    }

  }
  return (
    <div>
      
      <center>
        <div className="form-container"> 
        <form>
        <h2>Student SignUp</h2>
          <input placeholder="User Id" onChange={handleInputChange} name="userid" value={inputField.userid}></input>
          <br />
          <br />
          <input placeholder="Username" onChange={handleInputChange} name="username" value={inputField.username}></input>
          <br />
          <br />
          <input placeholder="Email" onChange={handleInputChange} name="email" value={inputField.email}></input>
          <br />
          <br />
          <input placeholder="Mobile" onChange={handleInputChange} name="mobile" value={inputField.mobile}></input>
          <br />
          <br />
          <input placeholder="Password" onChange={handleInputChange} name="password" value={inputField.password}></input>
          <br />
          <br />
           {/* Native HTML select element */}
           <select name="standard" value={selectedValue} onChange={handleSelectChange}>
              {options.map((option, index) => (
                <option  key={index} value={option.value}>{option.label}</option>
              ))}
            </select>
            <br />
            <br />

          <Link to="/slogin">Allready User? Login Here</Link>
          <br></br>
          <br></br>
          <button onClick={submitButton}> Sign Up</button>
        </form>
        </div>
      </center>
    </div>
  );
};

export default Studentregister;
