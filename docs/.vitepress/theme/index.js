import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import BackButton from './BackButton.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'doc-before': () => h(BackButton)
    })
  }
}
