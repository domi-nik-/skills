<script setup lang="ts">
const { t } = useI18n()
const { signInWithOtp } = useAuth()
</script>
<template>
  <p class="text-lg" @click="signInWithOtp('a@b.c')">{{ t('hello') }}</p>
</template>
