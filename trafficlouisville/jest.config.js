module.exports = {
    testEnvironment: 'jsdom',
    moduleNameMapper: {
      '\\.(css|scss)$': 'identity-obj-proxy',
    },
    transform: {
      '^.+\\.[t|j]sx?$': 'babel-jest',
    },
  };
  