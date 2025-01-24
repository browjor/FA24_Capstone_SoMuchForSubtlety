import { render, screen, waitFor } from '@testing-library/react';
import TrafficMap from './components/Map/TrafficMap';
import { server } from './mocks/browser'; // Import mock server
import { rest } from 'msw';

describe('TrafficMap', () => {
  test('renders loading state initially', () => {
    render(<TrafficMap />);

    expect(screen.getByText(/Loading traffic data.../i)).toBeInTheDocument();
  });

  test('renders traffic data after fetching', async () => {
    render(<TrafficMap />);

    // Wait for the mock traffic data to be rendered
    await waitFor(() => screen.getByText(/Lat: 37.7749, Lng: -122.4194, Density: 0.8/));

    // Check that traffic data appears in the list
    expect(screen.getByText(/Lat: 37.7749, Lng: -122.4194, Density: 0.8/)).toBeInTheDocument();
    expect(screen.getByText(/Lat: 37.775, Lng: -122.4184, Density: 0.6/)).toBeInTheDocument();
  });

  test('handles API errors gracefully', async () => {
    // Simulate an error response from the API
    server.use(
      rest.get('/api/traffic-data', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ message: 'Server Error' }));
      })
    );

    render(<TrafficMap />);

    // Wait for the error message to appear
    await waitFor(() => screen.getByText(/Error: Server Error/));

    // Check that the error message is displayed
    expect(screen.getByText(/Error: Server Error/)).toBeInTheDocument();
  });
});
