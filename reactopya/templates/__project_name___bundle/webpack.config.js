////////////////////////////////////////////////////////////////////
// This file is automatically generated
// Do not edit manually
////////////////////////////////////////////////////////////////////

var path = require('path');
var version = require('./package.json').version;

let rules = [
    {
        // JavaScript rules.
        test: /\.js$/,
        exclude: [/node_modules/, /.*\.min\.js/],
        use: {
            loader: 'babel-loader',
            options: {
                presets: [
                    ["@babel/preset-env",
                        {
                            "targets": {
                                "chrome": "70"
                            }
                        }],
                    "@babel/preset-react"
                ],
                plugins: [
                    "@babel/plugin-proposal-class-properties"
                ]
            }
        }
    },
    {
        // CSS files
        test: /\.css$/,
        use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' }
        ],
    },
    {
        // Some image formats so you can import images
        test: /\.(png|gif|jpg|svg)$/,
        use: {
            loader: 'url-loader',
            options: {
                limit: 10000000,
            },
        },
    }
];

{% if adjust_webpack_rules is defined %}
{% if adjust_webpack_rules is string %}
{{ adjust_webpack_rules }}
{% else %}
{% for item in adjust_webpack_rules -%}
{{ item }}
{% endfor %}
{% endif %}
{% endif %}

/*
The react alias below is needed because otherwise it could resolve to
the wrong one in a subdirectory. Then I get a react hooks error
because 2 different reacts are being used in the same app.
See:
https://reactjs.org/warnings/invalid-hook-call-warning.html
https://github.com/facebook/react/issues/13991
*/

const resolve = {
    // css causes a problem here
    extensions: ['.js', '.json', '.png', '.gif', '.jpg', '.svg'],
    alias: {
        'reactopya': __dirname + '/reactopya_common',
        'react': __dirname + '/node_modules/react' // See above
    }
};


module.exports = [
    {
        entry: ['./main.js'],
        target: 'web',
        output: {
            filename: 'bundle.js',
            path: path.resolve(__dirname, 'dist'),
            library: '{{ project_name }}',
            libraryTarget: 'window'
        },
        // devtool: 'source-map',
        module: {
            rules: rules
        },
        resolve: resolve
    }
];
