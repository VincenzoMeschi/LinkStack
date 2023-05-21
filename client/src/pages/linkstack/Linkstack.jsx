import React, { useState, useContext } from "react";
import { useMutation, gql, useQuery } from "@apollo/client";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../App";
import "./linkstack.css";

const VIEWLINKSTACK = gql`
  query ViewLinkStack($stackid: String!) {
    viewLinkStack(stackid: $stackid) {
      stackid
      stacktitle
      stackdesc
      stacktheme
      useremail
      links {
        linkid
        linktitle
        linkdesc
        linkplatform
        linknickname
        linkhttp
      }
    }
  }
`;

const CREATELINK = gql`
  mutation CreateLink($stackid: String!, $linktitle: String!, $linkdesc: String!, $linkhttp: String!, $linkplatform: String!, $linknickname: String!) {
    createLink(stackid: $stackid, linktitle: $linktitle, linkdesc: $linkdesc, linkhttp: $linkhttp, linkplatform: $linkplatform, linknickname: $linknickname) {
      link {
        linktitle
        linkdesc
        linkhttp
        linkplatform
        linknickname
      }
    }
  }
`;

const UPDATELINK = gql`
  mutation UpdateLink($linkid: String!, $linktitle: String!, $linkdesc: String!, $linkhttp: String!, $linkplatform: String!, $linknickname: String!) {
    updateLink(linkid: $linkid, linktitle: $linktitle, linkdesc: $linkdesc, linkhttp: $linkhttp, linkplatform: $linkplatform, linknickname: $linknickname) {
      link {
        linktitle
        linkdesc
        linkhttp
        linkplatform
        linknickname
      }
    }
  }
`;

const DELETELINK = gql`
  mutation DeleteLink($linkid: String!) {
    deleteLink(linkid: $linkid) {
      ok
    }
  }
`;

const DELETELINKSTACK = gql`
  mutation DeleteLinkStack($stackid: String!) {
    deleteLinkStack(stackid: $stackid) {
      ok
    }
  }
`;

const LinkStack = () => {
  const linkStackId = window.location.pathname.split("/")[2];
  const [linktitle, setlinktitle] = useState("");
  const [linkdesc, setlinkdesc] = useState("");
  const [linkhttp, setlinkhttp] = useState("");
  const [linkplatform, setlinkplatform] = useState("");
  const [linknickname, setlinknickname] = useState("");
  const [linkToEdit, setLinkToEdit] = useState(null);
  const [formMode, setFormMode] = useState("create");
  const [showForm, setShowForm] = useState(false);
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const { loading, error, data } = useQuery(VIEWLINKSTACK, {
    variables: { stackid: linkStackId },
  });

  const [updateLink] = useMutation(UPDATELINK, {
    refetchQueries: [{ query: VIEWLINKSTACK, variables: { stackid: linkStackId } }],
  });

  const [createLink] = useMutation(CREATELINK, {
    refetchQueries: [{ query: VIEWLINKSTACK, variables: { stackid: linkStackId } }],
  });

  const [deleteLink] = useMutation(DELETELINK, {
    refetchQueries: [{ query: VIEWLINKSTACK, variables: { stackid: linkStackId } }],
  });

  const [deleteLinkStack] = useMutation(DELETELINKSTACK, {
    refetchQueries: [{ query: VIEWLINKSTACK, variables: { stackid: linkStackId } }],
  });

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    try {
      await createLink({ variables: { stackid: linkStackId, linktitle, linkdesc, linkhttp, linkplatform, linknickname } });
      setlinktitle("");
      setLinkToEdit(null);
      setlinkdesc("");
      setlinkhttp("");
      setlinkplatform("");
      setlinknickname("");
      setShowForm(false);
    } catch (error) {
      console.error("Error creating Link:", error);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateLink({ variables: { linkid: linkToEdit.linkid, linktitle, linkdesc, linkhttp, linkplatform, linknickname } });
      setlinktitle("");
      setlinkdesc("");
      setlinkhttp("");
      setlinkplatform("");
      setlinknickname("");
      setLinkToEdit(null);
      setShowForm(false);
    } catch (error) {
      console.error("Error updating Link:", error);
    }
  };

  const handleEditLink = (link) => {
    setLinkToEdit(link);
    setlinktitle(link.linktitle);
    setlinkdesc(link.linkdesc);
    setlinkhttp(link.linkhttp);
    setlinkplatform(link.linkplatform);
    setlinknickname(link.linknickname);
    setFormMode("edit");
    setShowForm(true);
  };

  const handleDeleteLink = async (link) => {
    try {
      await deleteLink({ variables: { linkid: link.linkid } });
    } catch (error) {
      console.error("Error deleting Link:", error);
    }
  };

  const handleDeleteLinkStack = async (stack) => {
    try {
      await deleteLinkStack({ variables: { stackid: stack.stackid } });
      navigate("/dashboard");
    } catch (error) {
      console.error("Error deleting Link Stack:", error);
    }
  };

  const handleCreate = () => {
    setlinktitle("");
    setlinkdesc("");
    setlinkhttp("");
    setlinkplatform("");
    setlinknickname("");
    setLinkToEdit(null);
    setFormMode("create");
    setShowForm(true);
  };

  const handleClose = () => {
    setShowForm(false);
    setLinkToEdit(null);
    setlinktitle("");
    setlinkdesc("");
    setlinkhttp("");
    setlinkplatform("");
    setlinknickname("");
  };

  if (loading) return "Loading...";
  if (error) return `Error: ${error.message}`;

  return (
    <div className="linkstack-background">
      <div className="linkstack-container">
        <h1>{data.viewLinkStack.stacktitle}</h1>
        <p className="linkstack-description">{data.viewLinkStack.stackdesc}</p>

        <div className="linkstack-links">
          {data?.viewLinkStack.links.map((link) => (
            <div className="linkstack-link">
              <a href={link.linkhttp} target="_blank" rel="noreferrer" key={link.linkid}>
                <div className="link-row-1">
                  <h3>{link.linktitle}</h3>
                  <h6>{link.linknickname}</h6>
                </div>
                <p>{link.linkdesc}</p>
              </a>
              <div className="link-right">
                <h5>{link.linkplatform}</h5>
                {user?.useremail === data?.viewLinkStack.useremail ? (
                  <div className="modify-buttons">
                    <button className="editLinkButton" onClick={() => handleEditLink(link)}>
                      Edit
                    </button>
                    <button className="deleteLinkButton" onClick={() => handleDeleteLink(link)}>
                      Delete
                    </button>
                  </div>
                ) : null}
              </div>
            </div>
          ))}
          {user?.useremail === data?.viewLinkStack.useremail && (
            <>
              {showForm ? (
                <form onSubmit={formMode === "create" ? handleCreateSubmit : handleEditSubmit} className="link-form">
                  <div className="link-form-inputs">
                    <div className="input-field">
                      <label htmlFor="linktitle">Link Title</label>
                      <input type="text" id="linktitle" value={linktitle} onChange={(e) => setlinktitle(e.target.value)} />
                    </div>
                    <div className="input-field">
                      <label htmlFor="linknickname">Link Nickname</label>
                      <input type="text" id="linknickname" value={linknickname} onChange={(e) => setlinknickname(e.target.value)} />
                    </div>
                    <div className="input-field">
                      <label htmlFor="linkdesc">Link Description</label>
                      <input type="text" id="linkdesc" value={linkdesc} maxLength={150} onChange={(e) => setlinkdesc(e.target.value)} />
                    </div>
                    <div className="input-field">
                      <label htmlFor="linkhttp">Link URL</label>
                      <input type="text" id="linkhttp" value={linkhttp} onChange={(e) => setlinkhttp(e.target.value)} />
                    </div>
                    <div className="input-field">
                      <label htmlFor="linkplatform">Link Platform</label>
                      <input type="text" id="linkplatform" value={linkplatform} onChange={(e) => setlinkplatform(e.target.value)} />
                    </div>
                    <div className="form-buttons">
                      <button type="submit" className="link-form-submit">Submit</button>
                      <button className="link-form-close" type="button" onClick={handleClose}>
                        Close
                      </button>
                    </div>
                  </div>
                </form>
              ) : (
                <button className="create-link" onClick={handleCreate}>
                  Create Link
                </button>
              )}
            </>
          )}
        </div>
      </div>

      {user?.useremail === data?.viewLinkStack.useremail && (
        <div className="linkstack-options">
          <button className="delete-linkstack-button" onClick={() => handleDeleteLinkStack(data?.viewLinkStack)}>
            Delete Link Stack
          </button>
        </div>
      )}
    </div>
  );
};

export default LinkStack;
