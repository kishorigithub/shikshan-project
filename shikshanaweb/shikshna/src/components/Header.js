import { useState } from "react";
import { logoimg } from "../utils/constants";
import { Link } from "react-router-dom";

const Header = () => {

  const [showSignUpDropdown,setshowSignUpDropdown]=useState(false);
  const [showSignInDropdown,setshowSignInDropdown]=useState(false);

  const toggelsignupDropdown=()=>{
    setshowSignUpDropdown(!showSignUpDropdown)

  }

  const toggelsigninDropdown=()=>{
    setshowSignInDropdown(!showSignInDropdown)
  }


  return (
    <div className="header">
      <div className="logo-container">
        <img className="logo" src=".\logo.png" alt="logo.png"></img>
      </div>
      <div className="menu">
      <ul >
      {/* <li><Link to="/">Home</Link></li>
      <li><Link to="/admin">Admin Login</Link></li>
      <li><Link to="/slogin">Student Login</Link></li>
      <li><Link to="/tlogin">Teacher Login</Link></li>
      <li><Link to="/about">About Us</Link></li>
      <li><Link to="/contact">Contact Us</Link></li> */}

      <div className="dropdown">


          <button onClick={toggelsignupDropdown}>Sign Up</button>
          {showSignUpDropdown && (
          <div className="dropdown-menu">
            <a href="/teacherregister">Teacher</a>
            <a href="/studentregister">Student</a>
            
          </div>
        )}

</div>
<div className="dropdown">
          
          <button onClick={toggelsigninDropdown}>Sign In</button>
          {showSignInDropdown && (
          <div className="dropdown-menu">
            <a href="/tlogin">Teacher</a>
            <a href="/slogin">Student</a>
            <a href="/admin">Admin</a>
          </div>
        )}

        </div>
        </ul>

      </div>
      
       
      </div>
    
  );
};

export default Header;
