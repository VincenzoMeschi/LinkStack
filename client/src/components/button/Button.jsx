import React from "react";
import { Link } from "react-router-dom";
import "./button.css";

const Button = (props) => {
  return (
    <Link className={props.theme} to={props.link}>
      {props.text}
    </Link>
  );
};

export default Button;
