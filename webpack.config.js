var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
	context: __dirname,
	entry: ["./habits/static/js/index"],
	output: {
		path: path.resolve("./habits/static/bundles/"),
		filename: "[name]-[hash].js",
	},

	plugins: [new BundleTracker({ filename: "./webpack-stats.json" })],

	module: {
		rules: [
			{
				test: /\.css$/i,
				use: ["style-loader", "css-loader"],
			},
			{
				test: /\.m?js$/,
				exclude: /(node_modules|bower_components)/,
				use: {
					loader: "babel-loader",
					options: {
						presets: ["@babel/preset-env", "@babel/preset-react"],
						plugins: ["@babel/plugin-proposal-object-rest-spread", "@babel/plugin-proposal-class-properties"],
					},
				},
			},
		],
	},
};
