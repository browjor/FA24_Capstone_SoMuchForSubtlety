import { worker } from './mocks/browser';

// Start the mock service worker before tests
beforeAll(() => worker.start());

// Reset handlers after each test to ensure tests are isolated
afterEach(() => worker.resetHandlers());

// Clean up after the tests are finished
afterAll(() => worker.close());
