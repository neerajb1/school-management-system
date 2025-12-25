const path = require('path');

module.exports = {
    webpack: {
        alias: {
            'react-refresh/runtime': path.resolve(__dirname, '../node_modules/react-refresh/runtime.js'),
        },
    },
};
