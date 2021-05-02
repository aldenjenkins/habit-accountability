const scssConfig = require("../scssConfig");
const postcssPlugins = require("../postcssPlugins");

const sassRegex = /\.scss$/;
const sassModulesRegex = /\.module\.scss$/;

function getScssConfig(sassOptions) {
	return [
		{
			test: sassRegex,
			exclude: [sassModulesRegex, /node_modules/],
			sideEffects: true,
			use: [
				"style-loader",
				{
					loader: "css-loader",
					options: {
						importLoaders: 2,
					},
				},
				{
					loader: "postcss-loader",
					options: {
						plugins: postcssPlugins,
					},
				},
				{
					loader: "sass-loader",
					options: {
						sassOptions: {
							...scssConfig,
							...sassOptions,
						},
					},
				},
			],
		},
		{
			test: sassModulesRegex,
			sideEffects: true,
			use: [
				"style-loader",
				{
					loader: "css-loader",
					options: {
						modules: {
							localIdentName: "[name]__[local]___[hash:base64:5]",
						},
						importLoaders: 2,
					},
				},
				{
					loader: "postcss-loader",
					options: {
						plugins: postcssPlugins,
					},
				},
				{
					loader: "sass-loader",
					options: {
						sassOptions: {
							...scssConfig,
							...sassOptions,
						},
					},
				},
			],
			exclude: /node_modules/,
		},
	];
}

module.exports = getScssConfig;
