import dynamic from "next/dynamic";
import React from "react";

// Dynamically import Leaflet components to avoid SSR issues
const MapContainer = dynamic(() => import("react-leaflet").then(mod => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import("react-leaflet").then(mod => mod.TileLayer), { ssr: false });
const CircleMarker = dynamic(() => import("react-leaflet").then(mod => mod.CircleMarker), { ssr: false });

export default function Map({ center, zoom, trafficData = [] }) {
    // Log trafficData to ensure it's coming through correctly
    console.log("trafficData:", trafficData);

    // Handle the case where trafficData might not be in the correct format
    if (!Array.isArray(trafficData)) {
        console.error("Invalid traffic data format:", trafficData);
        return <div>Error: Invalid traffic data</div>;
    }

    return (
        <div style={{ height: "100vh", width: "100vw" }}>
            <MapContainer center={center} zoom={zoom} style={{ height: "100%", width: "100%" }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                {/* Render markers if trafficData is valid */}
                {trafficData.map(({density, lat, lon}, index) => (
                    <CircleMarker
                        key={index}
                        center={[lat, lon]}
                        radius={Math.max(density / 10, 5)} // Prevents markers from being too small
                        fillOpacity={0.6}
                        color="red"
                    />
                ))}
            </MapContainer>
        </div>
    );
}
