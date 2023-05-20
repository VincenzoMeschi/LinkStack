import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../../App";
import "./Navbar.css";

const Navbar = () => {
  const { user, handleLogout } = useContext(AuthContext);

  return (
    <nav>
      <h1>LinkStack</h1>
      <ul>
        <li>
          <Link to="/" className="nav-item">
            Home
          </Link>
        </li>
        {!!user ? (
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
              <Link to="/login" className="nav-item">
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