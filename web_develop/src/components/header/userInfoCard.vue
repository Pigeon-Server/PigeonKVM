<script>
import {useUserStore} from "@/store/userInfo";
import axios from "axios";

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
    this.getUserInfo()
    // const UserStore = useUserStore()
    // if(!UserStore.userName) {
    //   UserStore.getUserInfo()
    // }
    // this.username = UserStore.userName
    // this.group = UserStore.group
  },
  methods: {
    getUserInfo() {
      axios.get("/userInfo/api/getInfo").then(res=>{
        console.debug(res.data)
        if (res.data.status === 1) {
          this.username = res.data.data.userName
          this.group = res.data.data.group
        } else {
          this.username = "获取失败"
        }

      }).catch(err=>{
        console.error(err)
        this.username = "获取失败"
      })
    }
  }
}
</script>

<template>
  <v-list-item to="/userInfo" :title="username" :subtitle="group" :prepend-avatar="avatar"></v-list-item>
</template>

<style scoped>

</style>
