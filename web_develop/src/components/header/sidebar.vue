<script>
import axios from 'axios'
import UserInfoCard from "@/components/header/userInfoCard.vue";
import {useUserStore} from "@/store/userInfo";
import permission from "@/views/admin/Permission.vue";
import message from "@/scripts/utils/message";

export default {
  name: "header_sidebar",
  computed: {
    permission() {
      return permission
    }
  },
  components: {UserInfoCard},
  props: {
    display: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      UserPermissions: useUserStore().permissions
    }
  },
  methods: {
    logout() {
      axios.get("/auth/logout").then(res=>{
        let data = res.data
        switch (data.status) {
          case 1:
            message.showSuccess(this, data.msg)
            this.$router.push({name: "login"})
            break;
          case 0:
            message.showError(this, data.msg)
            break
        }
      }).catch(err=>{
        console.error(err)
        message.showApiErrorMsg(this, err.message)
      })
    }
  }
}
</script>

<template>
  <v-navigation-drawer
    :width="330"
    :model-value="display">
    <user-info-card></user-info-card>
    <v-divider></v-divider>
    <v-list-item subtitle="控制"></v-list-item>
    <v-list-item :to="{name: 'control'}" title="主机控制" prepend-icon="mdi:mdi-monitor" v-if="UserPermissions.all || UserPermissions.viewDevice"></v-list-item>
    <v-list-item :to="{name: 'files'}" title="USB文件管理" prepend-icon="mdi:mdi-file-multiple-outline" v-if="UserPermissions.all || UserPermissions.controllingDevice"></v-list-item>
    <v-divider></v-divider>
    <v-list-item subtitle="管理"></v-list-item>
    <v-list-item :to="{name: 'userManagement'}" title="用户管理" prepend-icon="mdi:mdi-account-details-outline" v-if="UserPermissions.all || UserPermissions.manageUsers"></v-list-item>
    <v-list-item :to="{name: 'permissionManagement'}" title="权限管理" prepend-icon="mdi:mdi-account-cog-outline" v-if="UserPermissions.all || UserPermissions.managePermissionGroups"></v-list-item>
    <v-list-item :to="{name: 'audit'}" title="审计与日志" prepend-icon="mdi:mdi-chart-timeline" v-if="UserPermissions.all || UserPermissions.viewAudit"></v-list-item>
    <v-list-item :to="{name: 'settings'}" title="设置" prepend-icon="mdi:mdi-cogs" v-if="UserPermissions.all || UserPermissions.changeSettings"></v-list-item>
    <v-divider></v-divider>
    <v-list-item subtitle="浏览"></v-list-item>
    <v-list-item :to="{name: 'about'}" title="关于PigeonKVM" prepend-icon="mdi:mdi-copyright"></v-list-item>
    <template v-slot:append>
      <div class="pa-2">
        <v-btn block prepend-icon="mdi:mdi-logout" @click="logout()">
          登出
        </v-btn>
      </div>
    </template>
    </v-navigation-drawer>
</template>

<style scoped>

</style>
