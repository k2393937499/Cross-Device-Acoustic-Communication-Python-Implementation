<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="d-flex flex-column justify-content-center">
    <p class="m-5 fs-1 fw-bold">跨设备水声通信工具</p>
    <div class="d-flex justify-content-around">
      <BButton variant="primary">
        <RouterLink to="/" class="text-light text-decoration-none">发送模块</RouterLink>
      </BButton>
      <BButton variant="primary">
        <RouterLink to="/about" class="text-light text-decoration-none">接收模块</RouterLink>
      </BButton>
    </div>
  </div>


  <div class="d-flex flex-column justify-content-center">
    <RouterView />
  </div>
</template>