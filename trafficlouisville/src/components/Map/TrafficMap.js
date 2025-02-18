import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS

const HeatmapLayer = ({ trafficData }) => {
  const map = useMap();
  const [heatLayer, setHeatLayer] = useState(null);

  useEffect(() => {
    console.log("Traffic data for heatmap:", trafficData);  // Log traffic data when it changes

    if (!map || !Array.isArray(trafficData) || trafficData.length === 0) return;  // Safeguard against empty data

    // Remove old heatmap layer if it exists
    if (heatLayer) {
      map.removeLayer(heatLayer);
    }

    // Convert traffic data to heatmap points
    const heatData = trafficData.map(({ latitude, longitude, density }) => [
      latitude,
      longitude,
      density,
    ]);

    // Create new heatmap layer with custom settings
    const newHeatLayer = L.heatLayer(heatData, {
      radius: 30, // Increase radius for larger heat spots
      blur: 20, // Increase blur for smoother transitions
      maxZoom: 15, // Set how zoomed in the heatmap remains visible
      max: 50, // Scale the maximum density for better visibility
      gradient: {
        0.2: "blue",
        0.4: "lime",
        0.6: "yellow",
        0.8: "orange",
        1.0: "red",
      },
    }).addTo(map);

    setHeatLayer(newHeatLayer);

    return () => {
      map.removeLayer(newHeatLayer); // Cleanup old heatmap
    };
  }, [trafficData, map]);

  return null;
};

const TrafficMap = ({ trafficData }) => {
  return (
    <div style={{ width: "100%", height: "500px", position: "relative" }}>
      <MapContainer
        center={[38.2527, -85.7585]}
        zoom={12}
        style={{ width: "100%", height: "100%", position: "relative" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <HeatmapLayer trafficData={trafficData} /> {/* Pass traffic data to heatmap */}
      </MapContainer>
    </div>
  );
};

export default TrafficMap;
