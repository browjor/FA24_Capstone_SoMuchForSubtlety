import handler from "../../pages/api/traffic";
import { mockTrafficData } from "./mockTrafficData";
import axios from "axios";

// ✅ Ensure axios is properly mocked
jest.mock("axios");

describe("Traffic API Handler", () => {
  const mockRes = {
    status: jest.fn().mockImplementation(() => mockRes),
    json: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("rejects non-GET requests", async () => {
    const mockReq = { method: "POST" };
    await handler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(405);
    expect(mockRes.json).toHaveBeenCalledWith({ error: "Method not allowed" });
  });

  test("returns 500 when server error occurs", async () => {
    const mockReq = { method: "GET" };

    // ✅ Mock the entire axios module, ensuring get returns a rejected Promise
    axios.get = jest.fn().mockRejectedValue(new Error("Server Error"));

    await handler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({ error: "Failed to fetch traffic data" });
  });

  test("returns traffic data successfully for GET request", async () => {
    const mockReq = { method: "GET" };

    // ✅ Mock axios.get to return the expected response
    axios.get = jest.fn().mockResolvedValue({
      data: {
        data: mockTrafficData.data,
        timestamp: mockTrafficData.timestamp
      }
    });

    await handler(mockReq, mockRes);

    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      data: mockTrafficData.data,
      timestamp: mockTrafficData.timestamp
    });
  });
});