const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  chainWebpack: config => {
    config
    .plugin('html')
    .tap(args => {
      args[0].title = '留言板'
      return args
    })
  },
  transpileDependencies: true,
  devServer: {
    host: 'localhost',
    port: 8092,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        pathRewrite: {
          '^/': '/'
        }
      }
    }
  },
  lintOnSave: false
})
