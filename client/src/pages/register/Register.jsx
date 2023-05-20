// src/components/Register.js
import React, { useState } from "react";
import { useMutation, gql } from "@apollo/client";
import "./register.css";

const CREATE_USER = gql`
  mutation CreateUser($useremail: String!, $userfirst: String!, $userlast: String!, $password: String!) {
    createUser(useremail: $useremail, userfirst: $userfirst, userlast: $userlast, password: $password) {
      ok
      user {
        useremail
      }
    }
  }
`;

const Register = () => {
  const [useremail, setUseremail] = useState("");
  const [userfirst, setUserfirst] = useState("");
  const [userlast, setUserlast] = useState("");
  const [password, setPassword] = useState("");
  const [createUser] = useMutation(CREATE_USER);

  const handleSubmit = (e) => {
    e.preventDefault();
    createUser({
      variables: { useremail, userfirst, userlast, password },
    });
    setUseremail("");
    setUserfirst("");
    setUserlast("");
    setPassword("");
  };

  return (
    <main>
      <div className="center-form-wrapper">
        <div className="register-container">
          <h1>Register</h1>
          <h4>Sign up for a free account</h4>
          <form onSubmit={handleSubmit}>
            <div className="register-form-inputs">
              <div className="fname-container input-field">
                <label htmlFor="fname">First Name</label>
                <input type="text" placeholder="John" id="fname" value={userfirst} onChange={(e) => setUserfirst(e.target.value)} />
              </div>

              <div className="lname-container input-field">
                <label htmlFor="lname">Last Name</label>
                <input type="text" placeholder="Doe" id="lname" value={userlast} onChange={(e) => setUserlast(e.target.value)} />
              </div>

              <div className="email-container input-field">
                <label htmlFor="email">Email</label>
                <input type="email" placeholder="john@example.com" id="email" value={useremail} onChange={(e) => setUseremail(e.target.value)} />
              </div>

              <div className="password-container input-field">
                <label htmlFor="password">Password</label>
                <input type="password" placeholder="********" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
              </div>

              <button type="submit">Register</button>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
};

export default Register;
