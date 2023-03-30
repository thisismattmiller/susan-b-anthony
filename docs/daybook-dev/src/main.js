import { createApp } from 'vue'
import App from './App.vue'
import { createVfm } from 'vue-final-modal'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import vue3Spinner from 'vue3-spinner'

import './index.css'
import 'vue-final-modal/style.css'

const app = createApp(App);

const vfm = createVfm()
app.use(vfm)

app.use(vue3Spinner)

app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true
});


app.mount("#app");
