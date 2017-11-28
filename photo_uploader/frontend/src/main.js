// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

// element ui
import Element from 'element-ui'
import 'element-ui/packages/theme-chalk/src/index.scss'

import App from './App'
import router from './router'

Vue.config.productionTip = false

Vue.use(Element)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
