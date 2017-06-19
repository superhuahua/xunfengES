// Learn more on how to config.
// - https://github.com/ant-tool/atool-build#配置扩展
var path = require('path');

module.exports = function(webpackConfig) {
  webpackConfig.babel.plugins.push('transform-runtime');
  webpackConfig.babel.plugins.push(['import', {
    libraryName: 'antd',
    style: 'css',
  }]);
  // webpackConfig.output.path = path.join(__dirname, '/server/templates');
  return webpackConfig;
};
