import React from "react";

function Error({ statusCode }) {
  if (statusCode >= 500 && statusCode < 600) {
    return (
      <div style={{ padding: "40px", textAlign: "center", fontFamily: "sans-serif" }}>
        <h1>{statusCode} - Server Error</h1>
        <p>Looks like our server is down, try again later :)</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "40px", textAlign: "center", fontFamily: "sans-serif" }}>
      <h1>{statusCode} Error</h1>
      <p>
        {statusCode
          ? `An error ${statusCode} occurred on server`
          : "An error occurred on client"}
      </p>
    </div>
  );
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error;
