const path = require('path');

module.exports = function override(config, env) {
    // Ensure react-refresh is resolved correctly
    config.resolve.alias = {
        ...config.resolve.alias,
        'react-refresh/runtime': path.resolve(__dirname, '../node_modules/react-refresh/runtime.js'),
    };

    return config;
};
