<script>
import LayoutsFooter from "@/layouts/default/Footer.vue";
import LayoutsHeader from "@/layouts/default/Header.vue";
import Settings from "@/layouts/admin/Settings.vue";

export default {
  name: "Config",
  components: {Settings},
}
</script>

<template>
  <v-card title="IPKVM CORE 设置" class="pageMain-card">
    <v-card-text>
      <settings></settings>
    </v-card-text>
  </v-card>
</template>

<style scoped>
</style>
