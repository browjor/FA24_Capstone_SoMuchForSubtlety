import crypto from "crypto";
import axios from "axios";

const SECRET_KEY = process.env.SHARED_KEY;
const BACKEND_URL = `${process.env.DOMAIN_NAME}/${process.env.API_ENDPOINT}`;

function verifyResponseHMAC(unformatted, timestamp, receivedHMAC) {
    const data = unformatted.map(entry => ({
        density: entry.density === '0.0' ? '0.0' : parseFloat(entry.density),  // Ensures density is always a float
        lat: entry.lat,
        lon: entry.lon
    }));
    const message = JSON.stringify({ data, timestamp: timestamp.toString() });
    console.log(message)// Ensure timestamp is inside JSON
    const expectedHMAC = crypto.createHmac("sha256", SECRET_KEY)
        .update(Buffer.from(message, "utf-8"))  // Ensure proper encoding
        .digest("hex");
    return crypto.timingSafeEqual(Buffer.from(receivedHMAC, "utf-8"), Buffer.from(expectedHMAC, "utf-8"));
}

function returnValidZeroArray(formatted) {
    return formatted.map(entry => ({
        density: entry.density === '0.0' ? 0 : parseFloat(entry.density),
        lat: entry.lat,
        lon: entry.lon
    }))
}

export default async function handler(req, res) {
    if (req.method !== "GET") {
        return res.status(405).json({ error: "Method not allowed" });
    }

    try {
        let timeStamp = Math.floor(Date.now() / 1000);  // Ensure a fresh timestamp
        timeStamp = timeStamp.toString();  // Convert to string immediately

        const hmac = crypto.createHmac("sha256", SECRET_KEY)
            .update(Buffer.from(timeStamp, "utf-8"))  // Ensure it is a Buffer
            .digest("hex");

        const response = await axios.get(BACKEND_URL, {
            headers: {
                "X-Timestamp": timeStamp,  // Send timestamp as a string
                "X-HMAC-Signature": hmac,
            },
        });

        let { data, timestamp: responseTimestamp, hmac: receivedHMAC } = response.data;

        if (!verifyResponseHMAC(data, responseTimestamp.toString(), receivedHMAC)) {
            return res.status(403).json({ error: "Invalid HMAC signature" });
        }

        data = returnValidZeroArray(data)

        if (!Array.isArray(data)) {
            console.warn("Received non-array traffic data, converting:", data);
            data = data ? [data] : [];  // Convert non-array to array
        }

        res.status(200).json({data});
    } catch (error) {
        console.error("Error fetching traffic data:", error.message);
        res.status(500).json({ error: "Failed to fetch traffic data" });
    }
}
