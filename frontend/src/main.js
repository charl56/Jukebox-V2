import { createApp } from 'vue'
import App from '@/App.vue'



// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App)

app.config.globalProperties.$backendPort = import.meta.env.VITE_BACK_URL || "http://127.0.0.1:5025/"
console.log(import.meta.env)
app.use(vuetify).mount('#app')
