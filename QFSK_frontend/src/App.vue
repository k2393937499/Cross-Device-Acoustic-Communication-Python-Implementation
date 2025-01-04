<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <BButton variant="primary">
      <RouterLink to="/" class="text-light text-decoration-none">发送模块</RouterLink>
    </BButton>
    <BButton variant="primary">
      <RouterLink to="/about" class="text-light text-decoration-none">接收模块</RouterLink>
    </BButton>
  </div>

  <div>
    <RouterView />
  </div>
</template>