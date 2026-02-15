const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    entry: {
        home: "./src/js/pages/home/main.js",
        homeStyles: "./src/css/3-bem/pages/home.css",
        globalStyles: "./src/css/1-global/global.css"
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].[contenthash].js',
        clean: true,
    },

    module: {
        rules: [
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            }
        ]
    },

    plugins: [
        new HtmlWebpackPlugin({
            filename: "home.html",
            template: "./src/html/pages/home.html",
            chunks: ["home", "homeStyles", "globalStyles"]
        })
    ]
};
