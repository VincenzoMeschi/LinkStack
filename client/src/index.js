import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { ApolloProvider } from "@apollo/client";
import client from "./apollo";

const ApolloApp = () => (
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
  );

ReactDOM.render(<ApolloApp />, document.getElementById("root"));
