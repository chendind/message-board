import Vue from 'vue'
import App from './App.vue'
import store from './store'
import { CellGroup, Cell, Field, Button, Dialog, Toast, RadioGroup, Radio, Switch, Icon, Popover, Skeleton, Empty } from 'vant'

import '@/assets/styles/index.css'
Vue.config.productionTip = false
Vue.use(CellGroup)
Vue.use(Cell)
Vue.use(Field)
Vue.use(Button)
Vue.use(Dialog)
Vue.use(Toast)
Vue.use(RadioGroup)
Vue.use(Radio)
Vue.use(Switch)
Vue.use(Icon)
Vue.use(Popover)
Vue.use(Skeleton)
Vue.use(Empty)
export default new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
