<script setup>
import { computed } from 'vue'
import { useData, useRouter } from 'vitepress'

const { page } = useData()
const router = useRouter()

const isHome = computed(() => page.value.relativePath === 'index.md')

function goBack() {
  if (typeof window !== 'undefined' && window.history.length > 1) {
    window.history.back()
    return
  }

  router.go('/')
}
</script>

<template>
  <div v-if="!isHome" class="page-back-wrap">
    <button type="button" class="page-back-button" @click="goBack">
      <span aria-hidden="true">←</span>
      返回上一页
    </button>
  </div>
</template>
