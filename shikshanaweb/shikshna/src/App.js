import Header from "./components/Header";
import About from "./components/About";
import Home from "./components/Home"
import Contact from "./components/Contact"
import Adminlogin from "./components/Adminlogin"
import Studentlogin from "./components/Studentlogin"
import Teacherlogin from "./components/Teacherlogin"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Studentregister from "./components/Studentregister";
import Teacherregister from "./components/Teacherregister";
import Front from "./components/Front";
import Uploadtimedata from "./components/Uploadtimedata";
import Headertwo from "./components/Headertwo";
import { useState } from "react";
import Verifyteacher from "./components/Verifyteacher";
import Syllabus from "./components/Syllabus";
import Verifystudent from "./components/Verifystudent";



function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <Router>
      {isLoggedIn ? <Headertwo /> : <Header />}
    <Routes>
      {/* Define routes */}
      <Route path="/" element={<Front />} />
      <Route path="/admin" element={<Adminlogin/>} />
      <Route path="/slogin" element={<Studentlogin />} />
      <Route path="/tlogin" element={<Teacherlogin setIsLoggedIn={setIsLoggedIn} />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/studentregister" element={<Studentregister />} />
      <Route path="/teacherregister" element={<Teacherregister  />} />
      <Route path="/uploadtimedata" element={<Uploadtimedata isLoggedIn={isLoggedIn}/>} />
      <Route path="/verifytedacher" element={<Verifyteacher/>} />
      <Route path="/verifystudent" element={<Verifystudent/>} />
      <Route path="/syllabus" element={<Syllabus />} />
      

     

      
    </Routes>
  </Router>
  );
}


export default App;

