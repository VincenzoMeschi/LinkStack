import React, { useState, useContext } from "react";
import { useMutation, gql } from "@apollo/client";
import { AuthContext } from "../../App";
import { useNavigate } from "react-router-dom";
import "./login.css";

const USER_LOGIN = gql`
  mutation UserLogin($useremail: String!, $password: String!) {
    userLogin(useremail: $useremail, password: $password) {
      accessToken
      refreshToken
      useremail
    }
  }
`;

const Login = () => {
  const [useremail, setUserEmail] = useState("");
  const [password, setPassword] = useState("");
  const { handleLogin } = useContext(AuthContext);
  const [userLogin] = useMutation(USER_LOGIN);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await userLogin({ variables: { useremail: useremail, password: password } });
      const { accessToken, refreshToken } = response.data.userLogin;
      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);
      handleLogin({ useremail });
      navigate("/");
    } catch (error) {
      console.error("Error logging in:", error);
    }
    setUserEmail("");
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
                <input type="email" placeholder="john@example.com" id="email" value={useremail} onChange={(e) => setUserEmail(e.target.value)} />
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
