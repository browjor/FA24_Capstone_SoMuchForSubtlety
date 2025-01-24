import { rest } from 'msw';

export const handlers = [
  // Mock traffic data API call
  rest.get('/api/traffic-data', (req, res, ctx) => {
    return res(
      ctx.json([
        { id: 1, latitude: 37.7749, longitude: -122.4194, density: 0.8 },
        { id: 2, latitude: 37.7750, longitude: -122.4184, density: 0.6 },
      ])
    );
  }),
];
