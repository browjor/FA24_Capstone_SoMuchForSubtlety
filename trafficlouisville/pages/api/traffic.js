import crypto from "crypto";
import axios from "axios";

const SECRET_KEY = process.env.SHARED_SECRET;
const apiPath = "/latest-traffic";
const BACKEND_URL = `http://${process.env.BACKEND_SERVER_IPV4}:${process.env.BACKEND_SERVER_PORT}${apiPath}`;

function verifyResponseHMAC(data, timestamp, receivedHMAC) {
    const message = JSON.stringify({ data, timestamp: timestamp.toString() });  // Ensure timestamp is inside JSON
    const expectedHMAC = crypto.createHmac("sha256", SECRET_KEY)
        .update(Buffer.from(message, "utf-8"))  // Ensure proper encoding
        .digest("hex");

    return crypto.timingSafeEqual(Buffer.from(receivedHMAC, "utf-8"), Buffer.from(expectedHMAC, "utf-8"));
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

        const { data, timestamp: responseTimestamp, hmac: receivedHMAC } = response.data;

        if (!verifyResponseHMAC(data, responseTimestamp.toString(), receivedHMAC)) {
            return res.status(403).json({ error: "Invalid HMAC signature" });
        }

        res.status(200).json({ data, timestamp: responseTimestamp });
    } catch (error) {
        console.error("Error fetching traffic data:", error.message);
        res.status(500).json({ error: "Failed to fetch traffic data" });
    }
}
