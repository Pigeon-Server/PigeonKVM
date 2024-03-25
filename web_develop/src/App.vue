<template>
  <v-app>
    <LayoutsHeader />
    <v-main>
      <router-view />
    </v-main>
<!--    <LayoutsFooter />-->
  </v-app>
</template>

<script setup>
  import LayoutsHeader from "@/layouts/default/Header.vue";
</script>
