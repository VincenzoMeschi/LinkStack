import React, { useState, useContext } from "react";
import { useMutation, gql } from "@apollo/client";
import { AuthContext } from "../../context/auth";
import "./login.css";

const USER_LOGIN = gql`
  mutation UserLogin($useremail: String!, $password: String!) {
    userLogin(useremail: $useremail, password: $password) {
      accessToken
      refreshToken
    }
  }
`;

  const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userLogin, { data }] = useMutation(USER_LOGIN);

  const handleSubmit = (e) => {
    e.preventDefault();
    userLogin({ variables: { useremail: email, password: password } }).then((response) => {
      localStorage.setItem("accessToken", response.data.userLogin.accessToken);
      localStorage.setItem("refreshToken", response.data.userLogin.refreshToken);
    });
    setEmail("");
    setPassword("");
  };

  return (
    <main>
      <div className="center-form-wrapper">
        <div className="login-container">
          <h1>Login</h1>
          <form onSubmit={handleSubmit}>
            <div className="login-form-inputs">
              <div className="input-field">
                <label htmlFor="email">Email</label>
                <input type="email" placeholder="john@example.com" id="email" value={email} onChange={(e) => setEmail(e.target.value)} />
              </div>

              <div className="input-field">
                <label htmlFor="password">Password</label>
                <input type="password" placeholder="********" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
              </div>
              <button type="submit">Login</button>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
};

export default Login;
