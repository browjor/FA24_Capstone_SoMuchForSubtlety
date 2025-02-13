import "leaflet/dist/leaflet.css";
import React from "react";
import "../src/styles/globals.scss"; // Keep your global styles

function MyApp({ Component, pageProps }) {
    return <Component {...pageProps} />;
}

export default MyApp;
