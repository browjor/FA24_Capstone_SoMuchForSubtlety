import { useState, useEffect } from "react";

interface TrafficData {
  id: string;
  density: number;
  latitude: number;
  longitude: number;
}

const API_URL = "https://192.168.5.25:12357/latest-traffic"; 

export const useTrafficData = () => {
  const [trafficData, setTrafficData] = useState<TrafficData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrafficData = async () => {
      try {
        const response = await fetch(API_URL);
        if (!response.ok) {
          throw new Error(`Error ${response.status}: Failed to fetch traffic data`);
        }
        const data: TrafficData[] = await response.json();
        setTrafficData(data);
        setError(null); // Reset error if successful
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    // Fetch initially and then every 4.8 seconds
    fetchTrafficData();
    const interval = setInterval(fetchTrafficData, 4800);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return { trafficData, loading, error };
};
