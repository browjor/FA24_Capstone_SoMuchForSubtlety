import React, { useEffect, useState } from "react";
import { useTrafficData } from "src/hooks/useTrafficData";
import { MapContainer, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet.heat';

const TrafficMap = () => {
  const { trafficData, loading, error } = useTrafficData();
  const [heatmapData, setHeatmapData] = useState([]);

  useEffect(() => {
    if (trafficData) {
      // Convert traffic data into the format that leaflet.heat expects
      const formattedData = trafficData.map(({ latitude, longitude, density }) => [
        latitude, // Latitude
        longitude, // Longitude
        density // Density (this is used for heatmap intensity)
      ]);
      setHeatmapData(formattedData);
    }
  }, [trafficData]);

  if (loading) return <p>Loading traffic data...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div style={{ width: "100%", height: "500px" }}>
      <MapContainer center={[37.7749, -122.4194]} zoom={12} style={{ width: "100%", height: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* Add Leaflet Heatmap Layer */}
        {heatmapData.length > 0 && (
          <L.heatLayer
            points={heatmapData}
            radius={25}  // Adjust the radius for heatmap coverage
            blur={15}    // Set the blur for smoothness
            maxZoom={17} // Limit zoom level for heatmap intensity
          />
        )}
      </MapContainer>
    </div>
  );
};

export default TrafficMap;
