<script>
import axios from 'axios'
import UserInfoCard from "@/components/header/userInfoCard.vue";
import {useUserStore} from "@/store/userInfo";
import permission from "@/views/admin/Permission.vue";
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
  data: ()=> {
    return {
      UserPermissions: useUserStore().permissions,
      displayMenu: false,
    }
  },
  // created() {
  //   this.UserPermissions = useUserStore().permissions
  // },
  mounted() {
    this.displayMenu = this.display
  },
  watch: { // 监听到数据然后赋值
      display(val){    //message即为父组件的值，val参数为值
        this.displayMenu = val    //将父组件的值赋给childrenMessage 子组件的值
        console.debug(`update:(displayMenu:${val})`)
      }
  },
  methods: {
    logout() {
      axios.get("/auth/logout").then(res=>{
        let data = res.data
        switch (data.status) {
          case 1:
            this.$notify.create({
              text: data.msg,
              level: 'success',
              location: 'bottom right',
              notifyOptions: {
                "close-delay": 3000
              }
            })
            location.href = "/login"
            break;
          case 0:
            this.$notify.create({
              text: data.msg,
              level: 'error',
              location: 'bottom right',
              notifyOptions: {
                "close-delay": 3000
              }
            })
            break
        }
      }).catch(err=>{
        console.error(err)
        this.$notify.create({
          text: err.message,
          level: 'error',
          location: 'bottom right',
          notifyOptions: {
            "close-delay": 3000
          }
        })
      })
    }
  }
}
</script>

<template>
  <v-navigation-drawer :width="290" v-model="displayMenu" disable-resize-watcher>
    <user-info-card></user-info-card>
    <v-divider></v-divider>
<!--     <v-list-item href="/" title="机器列表" prepend-icon="mdi:mdi-view-dashboard"></v-list-item>-->
    <v-list-item href="/" title="控制" prepend-icon="mdi:mdi-monitor" v-if="UserPermissions.all || UserPermissions.viewDevice"></v-list-item>
    <v-list-item href="/files" title="USB文件管理" prepend-icon="mdi:mdi-file-multiple-outline" v-if="UserPermissions.all || UserPermissions.controllingDevice"></v-list-item>
    <v-divider></v-divider>
    <v-list-item href="/admin/users" title="用户管理" prepend-icon="mdi:mdi-account-details-outline" v-if="UserPermissions.all || UserPermissions.manageUsers"></v-list-item>
    <v-list-item href="/admin/permission" title="权限管理" prepend-icon="mdi:mdi-account-cog-outline" v-if="UserPermissions.all || UserPermissions.managePermissionGroups"></v-list-item>
    <v-list-item href="/admin/audit" title="审计与日志" prepend-icon="mdi:mdi-chart-timeline" v-if="UserPermissions.all || UserPermissions.viewAudit"></v-list-item>
    <v-list-item href="/admin/settings" title="设置" prepend-icon="mdi:mdi-cogs" v-if="UserPermissions.all || UserPermissions.changeSettings"></v-list-item>
    <v-divider></v-divider>
    <v-list-item href="/about" title="关于IPKVM Core" prepend-icon="mdi:mdi-copyright"></v-list-item>
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
