<template>
    <v-app-bar>
        <v-app-bar-nav-icon v-if="useUserStore().id" @click.stop = "menu = !menu" title="展开侧边菜单">
            <v-icon icon="mdi-menu" />
        </v-app-bar-nav-icon>

        <v-app-bar-title>PigeonKVM</v-app-bar-title>
        <template v-slot:append>
          <router-view name="appBarBtn"></router-view>
        </template>
    </v-app-bar>
  <header_sidebar :display="menu"></header_sidebar>
</template>

<script>
import header_sidebar from "@/components/header/sidebar.vue";
import {useUserStore} from "@/store/userInfo";
export default {
  methods: {useUserStore},
  components: {header_sidebar},
  data:()=>{
    return {
      menu: false,
    }
  }
}
</script>
