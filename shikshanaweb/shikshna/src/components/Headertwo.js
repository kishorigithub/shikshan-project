import { Link } from "react-router-dom";
const Headertwo = () => {
  return (
    <div className="header">
      <div className="logo-container">
        <img className="logo" src=".\logo.png" alt="logo.png"></img>
      </div>
      <div className="menu">
        <ul>
          <li><Link to="/verifystudent">Verify Student</Link></li>
          <li><Link to="/contact">Contact Us</Link></li>
          <li><Link to="/">Logout</Link></li>
        </ul>
      </div>
    </div>
  );
};

export default Headertwo;
