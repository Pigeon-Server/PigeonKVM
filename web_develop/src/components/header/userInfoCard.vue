<script>
import axios from "axios";
import {useUserStore} from "@/store/userInfo";

export default {
  name: "userInfoCard",
  data: ()=>{
    return {
      username: "UserName",
      group: "未知",
      avatar: "/userInfo/api/getAvatar"
    }
  },
  created() {
    const UserStore = useUserStore()
    this.username = UserStore.userName
    this.group = UserStore.group
    // axios.get("/userInfo/api/getInfo").then(res=>{
    //   const apiStatus = res.data.status
    //   const data = res.data.data
    //   if (apiStatus === 1) {
    //     this.username = data.userName
    //     this.group = data.group
    //   } else {
    //     this.$notify.create({
    //       text: `API错误：${res.data.msg}(status:${apiStatus})`,
    //       level: 'error',
    //       location: 'bottom right',
    //       notifyOptions: {
    //         "close-delay": 3000
    //       }
    //     })
    //   }
    //
    // }).catch(err=>{
    //   this.$notify.create({
    //     text: `API错误：${err.message}`,
    //     level: 'error',
    //     location: 'bottom right',
    //     notifyOptions: {
    //       "close-delay": 3000
    //     }
    //   })
    // })
  }
}
</script>

<template>
  <v-list-item href="/userInfo" :title="username" :subtitle="group" :prepend-avatar="avatar"></v-list-item>
</template>

<style scoped>

</style>
