import axios from "axios";
import { useEffect } from "react";
import { useState } from "react";
import { ipofserver } from "./Global";

const Verifyteacher = () => {

    const [verifydata,setverifydata]=useState([]);

    useEffect(()=>{
        axios.get(`${ipofserver}getAllTeacher`)
        .then(data => {
            // alert(data.data)
            setverifydata(data.data);
          })
          .catch(err => {
            console.log(err);
          })

    },[])

    function submitButton(userid) {
        axios.post(ipofserver + 'verifyUser', {
          userid: userid,
          typeofuser: "teacher"
        })
          .then(function (response) {
            if (response.data === "success") {
              alert("Teacher verified successfully !")
              window.location.href = '/verifytedacher'
            }
            else {
              alert("Something wrong !")
            }
          })
          .catch(function (error) {
            return error;
          });
      }

  return (
    <div>
    <center>  <table>
        <thead>
          <tr>
            <th>Teacher Id</th>
            <th>Teacher Details</th>
            <th>Standard</th>
            <th>Verify</th>
          </tr>
        </thead>
        <tbody>
            {verifydata.map((vdata,index)=>(
                <tr key={index}>
                    <td>{vdata[0]}</td>
                <td>
                  <p style={{ marginBottom: '1px' }}><strong>{vdata[2]}</strong></p>
                  <p>{vdata[3]}</p>
                </td>
                <td>{vdata[5]}</td>
                <td>
                  {vdata[8] == "Verified" ? (
                    <h1 mr={1} style={{ color: 'Green', fontWeight: 'bold' }}>
                      Verified
                    </h1>
                  ) : (
                    <button color="info" size="large" onClick={() => submitButton(vdata[0])} fullWidth>
                      Verify
                    </button>
                  )}
                </td>
                </tr>

                

            ))}

        </tbody>
      </table>
      </center>
    </div>
  );
};

export default Verifyteacher;
