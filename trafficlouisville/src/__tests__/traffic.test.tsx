import handler from '../../pages/api/traffic'
import { mockTrafficData } from './mockTrafficData'
import axios from 'axios'
import crypto from 'crypto'

jest.mock('axios');
const mockedAxios = jest.mocked(axios);

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

  test('returns 500 when server error occurs', async () => {
    const mockReq = { method: 'GET' }
    mockedAxios.get.mockRejectedValueOnce(new Error('Server error'))
    await handler(mockReq, mockRes)
    expect(mockRes.status).toHaveBeenCalledWith(500)
    expect(mockRes.json).toHaveBeenCalledWith({ error: 'Failed to fetch traffic data' })
  })

test('returns traffic data successfully for GET request', async () => {
  const mockReq = { method: 'GET' }
    
  const timestamp = "1740525559"
  const data = mockTrafficData.data.map(entry => ({
      density: entry.density === "0.0" ? "0.0" : parseFloat(entry.density),
      lat: entry.lat,
      lon: entry.lon
  }))
    
  const message = JSON.stringify({ data, timestamp })
  const hmac = crypto
      .createHmac("sha256", process.env.SHARED_SECRET)
      .update(Buffer.from(message, "utf-8"))
      .digest("hex")
    
  mockedAxios.get.mockResolvedValueOnce({
      data: {
          data: data,
          timestamp: timestamp,
          hmac: hmac
      }
  })
  
  await handler(mockReq, mockRes)
  
  const expectedData = data.map(entry => ({
      ...entry,
      density: entry.density === "0.0" ? 0 : entry.density
  }))
  
  expect(mockRes.status).toHaveBeenCalledWith(200)
  expect(mockRes.json).toHaveBeenCalledWith({
      data: expectedData
  })
})
})
