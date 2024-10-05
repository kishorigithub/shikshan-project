import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { ipofserver } from "./Global";
import axios from "axios";
import { Link } from "react-router-dom";


const Teacherregister = () => {
  const [inputfileds, setinputfileds] = useState({
    username: '',
    email: '',
    mobile: '',
    password: '',
    subjects: ''
  });

  const [selectedValue, setSelectedValue] = useState('');

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
    setinputfileds({ ...inputfileds, [name]: value });
  };

  const handleSelectChange = (e) => {
    setSelectedValue(e.target.value);  // Update selected value for the standard
  };

  const submitButton = (e) => {
    e.preventDefault();
    var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (inputfileds.username === '' || inputfileds.email === '' || inputfileds.mobile === '' || inputfileds.password === '' || selectedValue === '') {
      alert("Please fill all the required fields");
    } else if (inputfileds.mobile.length !== 10) {
      alert("Please enter a 10-digit mobile number");
    } else if (!filter.test(inputfileds.email)) {
      alert("Please enter a valid email address");
    } else {
      axios.post(ipofserver + 'teacherRegister', {
        username: inputfileds.username,
        email: inputfileds.email,
        mobile: inputfileds.mobile,
        password: inputfileds.password,
        standard: selectedValue ,// Include the selected standard
        status: "Un-Verified"
        
      })
      
      .then(function (response) {
        if (response.data === "success") {
          alert("Teacher added successfully!");
          window.location.href = '/authentication/adminsign-in';
        } else {
          alert("Teacher already exists!");
        }
      })
      .catch(function (error) {
        return error;
      });
      
      
    }
  };

  

  return (
    <div>
      <center>
        <div className="form-container">
          <form>
            <h2>Teacher SignUp</h2>
            <input placeholder="Username" name="username" onChange={handleInputChange} value={inputfileds.username} />
            <br />
            <br />
            <input placeholder="Email" name="email" onChange={handleInputChange} value={inputfileds.email} />
            <br />
            <br />
            <input placeholder="Mobile" name="mobile" onChange={handleInputChange} value={inputfileds.mobile} />
            <br />
            <br />
            <input placeholder="Password" name="password" onChange={handleInputChange} value={inputfileds.password} />
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
            <Link to="/tlogin">Already User? Login Here</Link>
            <br />
            <br />
            <button onClick={submitButton}>Sign Up</button>
          </form>
        </div>
      </center>
    </div>
  );
};

export default Teacherregister;
