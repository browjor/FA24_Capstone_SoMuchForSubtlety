async function fetchTrafficData() {

    if (process.env.SEND_REQUESTS !== "true") {
        console.log("Requests are disabled. Skipping data fetch.");
        return null;  // Do not fetch if SEND_REQUESTS is not "true"
    }
    
    const sharedSecret = "SHARED_KEY";
    const endpoint = "https://your-backend-domain.com/latest-traffic";

    const method = "GET";
    const apiPath = "/latest-traffic";
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const message = `${method} ${apiPath} ${timestamp}`;

    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
        "raw",
        encoder.encode(sharedSecret),
        { name: "HMAC", hash: "SHA-256" },
        false,
        ["sign"]
    );

    const signatureBuffer = await crypto.subtle.sign("HMAC", key, encoder.encode(message));
    const signature = Array.from(new Uint8Array(signatureBuffer))
        .map((b) => b.toString(16).padStart(2, "0"))
        .join("");

    try {
        const response = await fetch(endpoint, {
            method: "GET",
            headers: {
                "X-Signature": signature,
                "X-Message": message
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.status}`);
        }

        const data = await response.json(); // Convert response to JSON
        return data; // ✅ Return the data instead of just logging it
    } catch (error) {
        console.error("Error fetching traffic data:", error);
        return null; // Return null on failure so the component can handle it
    }
}

export default fetchTrafficData;
