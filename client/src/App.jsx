import React, { createContext, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import HomePage from "./pages/homepage/HomePage";
import Dashboard from "./pages/Dashboard";
import LinkStack from "./pages/Linkstack";
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import NotFound from "./pages/NotFound";
import "./global.css";

export const AuthContext = createContext(); // rename to AuthContext

const App = () => {
  const [authState, setAuthState] = useState({
    isLoggedIn: false,
    user: null,
  });

  const handleLogin = (user) => {
    setAuthState({ isLoggedIn: true, user });
  };

  const handleLogout = () => {
    setAuthState({ isLoggedIn: false, user: null });
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
  };

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
