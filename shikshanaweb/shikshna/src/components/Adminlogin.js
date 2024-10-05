import { useState } from "react";

const Admin =()=>{

  const [inputfeilds,setinputfeilds]=useState({
    username:'Admin',
    password:'Admin'
  })

  const submitButton = () => {
if(inputfeilds.username ==='' || inputfeilds.password === ''){
  alert("Please All fields are required")
}
else{
  window.location.href = '/verifytedacher'
}
  }
    return(
        <div>
      
      <center>
        <div className="form-container">
          <div className="form">
        {/* <form> */}
        <h2>Admin Login</h2>
          <input placeholder="Username" name="username" value={inputfeilds.username}></input>
          <br />
          <br />
          <input placeholder="Password" type="password" name="password" value={inputfeilds.password}></input>
          <br />
          <br />
          
          <button onClick={submitButton}>Sign In</button>
        {/* </form> */}
        </div>
        </div>
      </center>
    </div>
    )
}

export default Admin;
