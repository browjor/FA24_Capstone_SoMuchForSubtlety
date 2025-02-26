import handler from "../../pages/api/traffic";
import { mockTrafficData } from "./mockTrafficData";
import axios from "axios";
import crypto from "crypto";

// ✅ Mock axios module
jest.mock("axios");

describe("Traffic API Handler", () => {
  const mockRes = {
    status: jest.fn().mockImplementation(() => mockRes),
    json: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
    process.env.SHARED_SECRET = "test-secret-key"; // ✅ Ensure SECRET_KEY exists
  });

  test("rejects non-GET requests", async () => {
    const mockReq = { method: "POST" };
    await handler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(405);
    expect(mockRes.json).toHaveBeenCalledWith({ error: "Method not allowed" });
  });

  test("returns 500 when server error occurs", async () => {
    const mockReq = { method: "GET" };

    // ✅ Mock axios failure
    axios.get.mockRejectedValueOnce(new Error("Server Error"));

    await handler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({ error: "Failed to fetch traffic data" });
  });

  test("returns traffic data successfully for GET request", async () => {
    const mockReq = {
      method: "GET",
      headers: {
        "X-Timestamp": "1739894801",
        "X-HMAC-Signature": "test-signature"
      }
    };

    // ✅ Compute valid HMAC for mockTrafficData
    const timestamp = mockTrafficData.timestamp.toString();
    const message = JSON.stringify({
      data: mockTrafficData.data,
      timestamp
    });

    const expectedHMAC = crypto.createHmac("sha256", process.env.SHARED_SECRET)
      .update(Buffer.from(message, "utf-8"))
      .digest("hex");

    // ✅ Properly mock axios response
    axios.get.mockResolvedValueOnce({
      data: {
        data: mockTrafficData.data,
        timestamp: mockTrafficData.timestamp,
        hmac: expectedHMAC
      }
    });

    await handler(mockReq, mockRes);

    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      data: mockTrafficData.data.map(entry => ({
        density: entry.density === "0.0" ? 0 : parseFloat(entry.density),
        lat: entry.lat,
        lon: entry.lon
      }))
    });

    // ✅ Validate axios request format
    expect(axios.get).toHaveBeenCalledWith(expect.stringContaining("/latest-traffic"), {
      headers: expect.objectContaining({
        "X-Timestamp": expect.any(String),
        "X-HMAC-Signature": expect.any(String)
      })
    });
  });
});