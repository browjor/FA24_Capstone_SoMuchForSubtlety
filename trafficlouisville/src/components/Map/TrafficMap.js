import React, { useEffect, useState } from "react";
import fetchTrafficData from "@/lib/fetchTrafficData"; // Import API function
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

const HeatmapLayer = ({ trafficData }) => {
  const map = useMap(); // Get reference to the Leaflet map

  useEffect(() => {
    if (trafficData.length > 0) {
      // Convert traffic data to heatmap format
      const formattedData = trafficData.map(({ latitude, longitude, density }) => [
        latitude,
        longitude,
        density
      ]);

      // Create or update heatmap layer
      const heatLayer = L.heatLayer(formattedData, {
        radius: 25,
        blur: 15,
        maxZoom: 17
      }).addTo(map);

      return () => {
        map.removeLayer(heatLayer); // Cleanup old heatmap layer when data updates
      };
    }
  }, [trafficData, map]);

  return null; // This component doesn't render anything itself
};

const TrafficMap = () => {
  const [trafficData, setTrafficData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchTrafficData();
        if (data) {
          setTrafficData(data);
        }
      } catch (error) {
        console.error("Error fetching traffic data:", error);
      }
    };

    fetchData(); // Fetch immediately on mount

    const interval = setInterval(fetchData, 4800); // Fetch every 4.8 seconds

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  return (
    <div style={{ width: "100%", height: "500px" }}>
      <MapContainer center={[37.7749, -122.4194]} zoom={12} style={{ width: "100%", height: "100%" }}>
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
