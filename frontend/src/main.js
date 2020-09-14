import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import CoreuiVue from "@coreui/vue";
import vSelect from "vue-select";
import * as VeeValidate from 'vee-validate';
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { freeSet as icons } from "@coreui/icons"


Vue.use(CoreuiVue);
Vue.use(VeeValidate);
Vue.component("v-select", vSelect)
Vue.component("ValidationProvider", ValidationProvider);
Vue.component("ValidationObserver", ValidationObserver);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  icons,
  render: h => h(App)
}).$mount("#app");
