// pages/_error.js
function Error({ statusCode }) {
    if (statusCode === 504) {
      return (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h1>504 Gateway Timeout</h1>
          <p>Looks like our server is down, try again later :)</p>
        </div>
      );
    }
    
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <h1>{statusCode} Error</h1>
        <p>An unexpected error has occurred.</p>
      </div>
    );
  }
  
  Error.getInitialProps = ({ res, err }) => {
    const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
    return { statusCode };
  };
  
  export default Error;