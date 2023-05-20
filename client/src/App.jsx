import React, { createContext, useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import HomePage from "./pages/homepage/HomePage";
import Dashboard from "./pages/dashboard/Dashboard";
import LinkStack from "./pages/linkstack/Linkstack";
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import NotFound from "./pages/NotFound";
import "./global.css";

export const AuthContext = createContext();

const App = () => {
  const existingUser = localStorage.getItem("user") && localStorage.getItem("user") !== "undefined" ? JSON.parse(localStorage.getItem("user")) : null;

  const [authState, setAuthState] = useState({
    user: existingUser,
  });
  const [isLoggedIn, setIsLoggedIn] = useState(!!existingUser);

  const handleLogin = (user) => {
    localStorage.setItem("user", JSON.stringify(user));
    setAuthState({ user });
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setAuthState({ user: null });
    setIsLoggedIn(false);
  };

  useEffect(() => {
    setIsLoggedIn(!!authState.user);
  }, [authState]);

  return (
    <Router>
      <AuthContext.Provider value={{ ...authState, handleLogin, handleLogout }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/linkstack/:id" element={<LinkStack />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthContext.Provider>
    </Router>
  );
};

export default App;
