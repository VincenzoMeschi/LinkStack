import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { IsLoggedInContext } from "../../App";
import "./Navbar.css";

const Navbar = ({ onLogin, onLogout }) => {
  const isLoggedIn = useContext(IsLoggedInContext);

  const handleLogin = (event) => {
    event.preventDefault();
    onLogin();
  };

  const handleLogout = (event) => {
    event.preventDefault();
    onLogout();
  };

  return (
    <nav>
      <h1>LinkStack</h1>
      <ul>
        <li>
          <Link to="/" className="nav-item">
            Home
          </Link>
        </li>
        {isLoggedIn ? (
          <>
            <li>
              <Link to="/dashboard" className="nav-item">
                Dashboard
              </Link>
            </li>
            <li>
              <Link to="/" className="nav-item" onClick={handleLogout}>
                Logout
              </Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/dashboard" className="nav-item" onClick={handleLogin}>
                Login
              </Link>
            </li>
            <li>
              <Link to="/register" className="nav-item">
                Register
              </Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
