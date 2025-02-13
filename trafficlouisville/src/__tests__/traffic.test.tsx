import handler from '../../pages/api/traffic'

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
})
