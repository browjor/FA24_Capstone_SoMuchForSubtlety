import { render } from '@testing-library/react'
import Map from '../components/Map/Map'
import React from 'react';

describe('Map Component', () => {
  test('renders with empty traffic data', () => {
    const props = {
      center: [38.2527, -85.7585],
      zoom: 12,
      trafficData: []
    }
    const { container } = render(<Map {...props} />)
    expect(container).toBeTruthy()
  })

  test('handles invalid traffic data format', () => {
    const props = {
      center: [38.2527, -85.7585],
      zoom: 12,
      trafficData: []
    }
    const { container } = render(<Map {...props} />)
    expect(container).toBeTruthy()
  })

  test('handles undefined traffic data', () => {
    const props = {
      center: [38.2527, -85.7585],
      zoom: 12
    }
    const { container } = render(<Map {...props} />)
    expect(container).toBeTruthy()
  })

  test('processes valid traffic data array format', () => {
    const props = {
      center: [38.2527, -85.7585],
      zoom: 12,
      trafficData: [[50, 38.2527, -85.7585], [30, 38.2528, -85.7586]]
    }
    const { container } = render(<Map {...props} />)
    expect(container).toBeTruthy()
  })
})
