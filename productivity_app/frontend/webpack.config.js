const fs = require('fs');
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


const config = {
    entry: {
        globalStyles: "./src/css/1-global/global.css",
        earlyUtilityStyles: "./src/css/2-early-utility/early-utility.css",
        customBootstrapStyles: "./src/css/4-custom-bootstrap/custom-bootstrap.css",
        lateUtilityStyles: "./src/css/5-late-utility/late-utility.css"
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
        })
    ]
};

// dynamically add page js and css
(() => {
    const files = fs.readdirSync('./src/html/pages');

    files
        .filter(file => path.extname(file).toLowerCase() === '.html')
        .forEach(htmlFile => {
            const page = path.basename(htmlFile, '.html');

            if (config.hasOwnProperty(page)) {
                throw new Error("Duplicate page name: "+ page);
            }

            const pageStyles = page + "Styles";
            const jsPath = `./src/js/pages/${page}/main.js`;
            const cssPath = `./src/css/3-bem/pages/${page}.css`;
            const jsPathExists = fs.existsSync(jsPath);
            const cssPathExists = fs.existsSync(cssPath);


            const chunks = [];
            if (jsPathExists) {
                config.entry[page] = jsPath;
                chunks.push(page);
            }
            const chunksCssPrefix = ["globalStyles", "earlyUtilityStyles"];
            const chunksCssSuffix = ["customBootstrapStyles", "lateUtilityStyles"];
            chunks.push(...chunksCssPrefix);
            if (cssPathExists) {
                config.entry[pageStyles] = cssPath;
                chunks.push(pageStyles)
            }
            chunks.push(...chunksCssSuffix);

            config.plugins.push(
                new HtmlWebpackPlugin({
                    template: `./src/html/pages/${page}.html`,
                    filename: `${page}.html`,
                    chunks: [page, "homeStyles", "globalStyles"]
                })
            );
        });

})();



module.exports = config;