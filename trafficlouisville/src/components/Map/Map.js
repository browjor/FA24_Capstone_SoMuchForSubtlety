import dynamic from "next/dynamic";
import React from "react";

// Dynamically import Leaflet components to avoid SSR issues
const MapContainer = dynamic(() => import("react-leaflet").then(mod => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import("react-leaflet").then(mod => mod.TileLayer), { ssr: false });
const CircleMarker = dynamic(() => import("react-leaflet").then(mod => mod.CircleMarker), { ssr: false });

export default function Map({ center, zoom, trafficData = [] }) {
    // Function to determine color based on density
    const getColor = (density) => {
        if (density < 0.2) return "green";
        if (density < 0.4) return "lime";
        if (density < 0.6) return "yellow";
        if (density < 0.8) return "orange";
        return "red";
    };

    // Handle the case where trafficData might not be in the correct format
    if (!Array.isArray(trafficData.data)) {
        console.error("Invalid traffic data format:", trafficData);
        return <div>Error: Invalid traffic data</div>;
    }

    return (
        <div className="flex" style={{ height: "75vh", width: "70vw" }}>
            <MapContainer className="flex" center={center} zoom={zoom} style={{ height: "100%", width: "100%" }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                {/* Render markers if trafficData is valid */}
                {trafficData.map(({ density, latitude, longitude }, index) => (
                <CircleMarker
                    key={`${index}-${density}`} // Ensures re-render when density changes
                    center={[parseFloat(latitude), parseFloat(longitude)]}
                    radius={Math.max(density * 10, 5)}
                    fillOpacity={0.6}
                    color={getColor(density)}
                />
            ))}
            </MapContainer>
        </div>
    );
}
