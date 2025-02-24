// import React from 'react';

// async function fetchTrafficData() {
//     if (process.env.SEND_REQUESTS && process.env.SEND_REQUESTS !== "TRUE") {
//       console.log("Requests are disabled. Skipping data fetch."); 
//       return null; 
//     }
  
//     const sharedSecret = process.env.SHARED_SECRET;
//     const apiPath = "/latest-traffic";
//     const endpoint = `http://${process.env.BACKEND_SERVER_IPV4}:${process.env.BACKEND_SERVER_PORT}${apiPath}`;
  
//     const method = "GET";
//     const timestamp = Math.floor(Date.now() / 1000).toString();
//     const message = `${method} ${timestamp}`;
  
//     const encoder = new TextEncoder();
//     const key = await crypto.subtle.importKey(
//       "raw",
//       encoder.encode(sharedSecret),
//       { name: "HMAC", hash: "SHA-256" },
//       false,
//       ["sign"]
//     );
  
//     const signatureBuffer = await crypto.subtle.sign("HMAC", key, encoder.encode(message));
//     const signature = Array.from(new Uint8Array(signatureBuffer))
//       .map((b) => b.toString(16).padStart(2, "0"))
//       .join("");
//     console.log("Generated Signature:", signature);
  
//     try {
//       console.log("Making fetch request to endpoint:", endpoint);
  
//       const response = await fetch(endpoint, {
//         method: "GET",
//         headers: {
//           "X-Signature": signature,
//           "X-Message": message
//         }
//       });
  
//       if (!response) {
//         throw new Error("No response received from server (response is undefined). Possible network failure.");
//       }
  
//       if (!response.ok) {
//         throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
//       }
  
//       const data = await response.json(); // Convert response to JSON
//       console.log("Received traffic data:", data);
  
//       return data; // Return the data instead of just logging it
  
//     } catch (error) {
//       console.error("Error fetching traffic data:", error.message);
  
//       return null; // Return null on failure
//     }
//   }
  
//   setInterval(() => {
//     console.log("Triggering fetchTrafficData()...");
//     fetchTrafficData();
//   }, 4800);
  
//   export default fetchTrafficData;
  