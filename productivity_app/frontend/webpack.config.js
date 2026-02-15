const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


module.exports = {
    entry: {
        home: "./src/js/pages/home/main.js",
        homeStyles: "./src/css/3-bem/pages/home.css",
        globalStyles: "./src/css/1-global/global.css"
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'js/[name].[contenthash].js',
        clean: true,
    },

    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ]
            }
        ]
    },

    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/[name].[contenthash].css'
        }),
        new HtmlWebpackPlugin({
            filename: "home.html",
            template: "./src/html/pages/home.html",
            chunks: ["home", "homeStyles", "globalStyles"]
        })
    ]
};
