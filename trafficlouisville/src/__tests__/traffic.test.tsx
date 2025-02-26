import handler from '../../pages/api/traffic'
import { mockTrafficData } from './mockTrafficData'

describe('Traffic API Handler', () => {
  const mockRes = {
    status: jest.fn(() => mockRes),
    json: jest.fn(() => mockRes)
  }

  beforeEach(() => {
    jest.clearAllMocks()
  })

  test('rejects non-GET requests', async () => {
    const mockReq = { method: 'POST' }
    await handler(mockReq, mockRes)
    expect(mockRes.status).toHaveBeenCalledWith(405)
    expect(mockRes.json).toHaveBeenCalledWith({ error: 'Method not allowed' })
  })

  test('returns 500 when server error occurs', async () => {
    const mockReq = { method: 'GET' }
    await handler(mockReq, mockRes)
    expect(mockRes.status).toHaveBeenCalledWith(500)
    expect(mockRes.json).toHaveBeenCalledWith({ error: 'Failed to fetch traffic data' })
  })

  test('returns traffic data successfully for GET request', async () => {
    const mockReq = { method: 'GET' }
    
    // Mock the fetch response directly with the structure we expect
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        data: mockTrafficData.data,
        timestamp: mockTrafficData.timestamp
      })
    })
  
    await handler(mockReq, mockRes)
    
    expect(mockRes.status).toHaveBeenCalledWith(200)
    expect(mockRes.json).toHaveBeenCalledWith({
      data: mockTrafficData.data,
      timestamp: mockTrafficData.timestamp
    })
  })
  
    })
