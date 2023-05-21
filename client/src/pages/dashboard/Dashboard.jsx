import React, { useState, useContext, useEffect } from "react";
import { useMutation, gql, useQuery } from "@apollo/client";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../App";
import LinkStackCard from "../../components/linkstack-card/LinkStackCard";
import "./dashboard.css";

const CREATE_LINKSTACK = gql`
  mutation CreateLinkStack($stacktitle: String!, $stackdesc: String!, $stacktheme: String!) {
    createLinkStack(stacktitle: $stacktitle, stackdesc: $stackdesc, stacktheme: $stacktheme) {
      linkstack {
        stacktitle
        stackdesc
        stacktheme
      }
    }
  }
`;

const GET_USER_LINKSTACKS = gql`
  query ViewUserLinkStacks($useremail: String!) {
    viewUserLinkStacks(useremail: $useremail) {
      stacktitle
      stackdesc
      stacktheme
      stackid
    }
  }
`;

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const [stacktitle, setstacktitle] = useState("");
  const [stackdesc, setstackdesc] = useState("");
  const [stacktheme, setstacktheme] = useState("");
  const [formVisible, setFormVisible] = useState(false);

  const { loading, error, data } = useQuery(GET_USER_LINKSTACKS, {
    variables: { useremail: user?.useremail },
    skip: !user,
    fetchPolicy: "network-only",
  });

  const [createLinkStack] = useMutation(CREATE_LINKSTACK, {
    refetchQueries: [{ query: GET_USER_LINKSTACKS, variables: { useremail: user?.useremail } }],
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createLinkStack({ variables: { stacktitle, stackdesc, stacktheme } });
      setstacktitle("");
      setstackdesc("");
      setstacktheme("");
      setFormVisible(false);
    } catch (error) {
      console.error("Error creating LinkStack:", error);
    }
  };

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
  }, [user, navigate]);

  if (loading) return "Loading...";
  if (error) return `Error: ${error.message}`;

  return (
    <div className="dashboard-container">
      <div className="dashboard-grid">
        {data?.viewUserLinkStacks.map((stack) => (
          <LinkStackCard stacktitle={stack.stacktitle} stackdesc={stack.stackdesc} stackid={stack.stackid} />
        ))}
        {formVisible ? (
          <form onSubmit={handleSubmit} className="linkstack-form">
            <input type="text" placeholder="LinkStack Title" value={stacktitle} onChange={(e) => setstacktitle(e.target.value)} />
            <textarea maxLength="150" rows="5" cols="50" placeholder="LinkStack Description" value={stackdesc} onChange={(e) => setstackdesc(e.target.value)} />
            <input type="text" placeholder="LinkStack Theme" value={stacktheme} onChange={(e) => setstacktheme(e.target.value)} />
            <button type="submit">Create</button>
          </form>
        ) : (
          <div className="linkstack-card add-linkstack" onClick={() => setFormVisible(true)}>
            <h3>Create LinkStack</h3>
            <p>+</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
