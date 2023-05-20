import React from "react";
import { Link } from "react-router-dom";
import "./LinkStackCard.css";

const LinkStackCard = (props) => {
 return (
   <Link to={`/linkstack/${props.stackid}`} className="user-linkstack-card" key={props.stackid}>
     <h3>{props.stacktitle}</h3>
     <p>{props.stackdesc}</p>
   </Link>
 );
};

export default LinkStackCard;
