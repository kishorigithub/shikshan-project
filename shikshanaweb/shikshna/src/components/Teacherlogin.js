import axios from "axios";
import { useState } from "react";
import { Link } from "react-router-dom";
import { ipofserver } from "./Global";
import { useNavigate } from "react-router-dom";
const Teacherlogin=({ setIsLoggedIn })=>{


  const options = [
    { label: "Select standard", value: "" },
    { label: "1st standard", value: "1st" },
    { label: "2nd standard", value: "2nd" },
    { label: "3rd standard", value: "3rd" },
    { label: "4th standard", value: "4th" },
    { label: "5th standard", value: "5th" }
  ];

  const [selectedValue,setselectedValue]=useState('')

  const handleSelectChange=(e)=>{
    setselectedValue(e.target.value)
  }

  const [inputfeild,setinputfeild]=useState({
    username:'kishori',
    password:'yash',
    standard:''

  })

  const inputsHandler=(e)=>{
    const {name,value}= e.target;
    setinputfeild((prevState)=>({
      ...prevState,
      [name]:value,
    }));
    
  }
  function setData(sessionname, standard) {
    localStorage.setItem('teacherloginUsername', sessionname);
    localStorage.setItem('teacherloginstd', standard);
  }

  const navigate = useNavigate();
  const onsubmitButton=()=>{

    

    if(inputfeild.username===''|| inputfeild.password===''|| selectedValue===''){
      alert("Please fill all details")
    }
    else{

      axios.post(ipofserver+'teacherlogin',{
        username: inputfeild.username,
        password: inputfeild.password,
        standard: selectedValue,
        

      })
      .then(function (response){
        if (response.data =="success") {
          setData(inputfeild.username, selectedValue)
          setIsLoggedIn(true);
          navigate('/uploadtimedata');
          
        }
        else {
          alert("Invalid username and password !")
        }
      })
      .catch(function (error) {
        return error;
      });
      
    }
  }


    return(
        <div>
      
      <center>
        <div className="form-container">
        {/* <form> */}
        <div className="form">
        <h2>Teacher SignIn</h2>
          <input placeholder="Username" onChange={inputsHandler} name="username" value={inputfeild.username}></input>
          <br />
          <br />
          <input placeholder="Password" onChange={inputsHandler} name="password" value={inputfeild.password}></input>
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
          <Link to="/teacherregister">You dont Have An Account? Register Here</Link>
          <br>
          </br>
          <br>
          </br>
          <button onClick={onsubmitButton}>Sign In</button>
        {/* </form> */}
        </div>
        </div>
      </center>
    </div>
    )
}

export default Teacherlogin;