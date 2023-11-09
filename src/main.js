import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { registerSW } from 'virtual:pwa-register'

const updateSW = registerSW({
  onNeedRefresh() {
    if (confirm("A new update to Eevee is available. Press OK to reload the page.")) {
      updateSW();
    }
  },
});

import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faAnglesRight, faArrowDown, faArrowLeft, faBan, faCheck, faChevronLeft, faChevronRight, faClock, faComputerMouse, faDownload, faFile, faFileArrowDown, faFileImport, faGear, faKeyboard, faPencil, faPencilSquare, faPlus, faQuestion, faRectangleList, faRotate, faSearch, faTrashCan, faTriangleExclamation, faXmark, faMagnifyingGlassArrowRight } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faTrashCan, faPlus, faPencil, faXmark, faTriangleExclamation, faChevronLeft, faChevronRight, faPencilSquare, faArrowDown, faArrowLeft, faDownload, faKeyboard, faComputerMouse, faCheck, faQuestion, faClock, faGear, faFile, faFileArrowDown, faFileImport, faRectangleList, faSearch, faRotate, faBan, faAnglesRight, faMagnifyingGlassArrowRight)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon).mount('#app')