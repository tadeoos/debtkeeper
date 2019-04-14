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
  pwa: {
    // configure the workbox plugin
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      // swSrc is required in InjectManifest mode.
      swSrc: 'public/service-worker.js',
      // ...other Workbox options...
    }
  }
};
