module.exports = {
  baseUrl: process.env.NODE_ENV === 'production'
      ? '/debtkeeper/'
      : '',
  // devServer: {
  //   proxy: {
  //     '/*': {
  //       target: 'http://localhost:5042',
  //       changeOrigin: true,
  //     },
  //   },
  // }
};
