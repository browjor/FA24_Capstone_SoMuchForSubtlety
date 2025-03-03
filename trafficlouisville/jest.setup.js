require('@testing-library/jest-dom');

process.env = {
    ...process.env,
    SHARED_SECRET: 'test-secret-key',
    BACKEND_SERVER_IPV4: 'localhost',
    BACKEND_SERVER_PORT: '3000'
};
