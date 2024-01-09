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
  }
}
</script>

<template>
  <v-list-item href="/userInfo" :title="username" :subtitle="group" :prepend-avatar="avatar"></v-list-item>
</template>

<style scoped>

</style>
