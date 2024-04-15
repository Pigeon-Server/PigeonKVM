<script>
import userList from "@/components/tables/users/userList.vue";
import axios from "axios";
import message from "@/scripts/utils/message";
import EditUserStatus from "@/components/dialogs/users/editUserStatus.vue";

import user_tools from "@/scripts/admin/users"
import EditUserPermission from "@/components/dialogs/users/editUserPermission.vue";
import NewUser from "@/components/dialogs/users/newUser.vue";

export default {
  name: "users",
  components: {NewUser, EditUserPermission, EditUserStatus, userList},
  data() {
    return {
      search: "",
      userList: [],
      currentPage: 1,
      maxPage: null,
      newUser: {
        flag: false,
      },
      editUserStatus: {
        flag: false,
        uid: null
      },
      editUserPermission: {
        flag: false,
        uid: null
      }
    }
  },
  methods: {
    getUserList(search = "", page = 1, pageSize = 20) {
      axios.post("/admin/api/getUserList", {
        page: page,
        pageSize: pageSize,
        search: search
      }).then(res => {
        const apiStatus = res.data.status
        if (apiStatus === 1) {
          const data = res.data.data
          const PageContent = data.PageContent
          this.userList = []
          this.maxPage = data.maxPage
          this.currentPage = data.currentPage
          for (const item of PageContent) {
            this.userList.push({
              uid: item.id,
              userName: item.userName,
              realName: item.realName,
              email: item.email,
              createdAt: item.createdAt,
              lastLoginTime: item.lastLoginTime,
              lastLoginIP: item.lastLoginIP,
              permission_id: item.permissionGroupID,
              permission_name: item.permissionGroupName,
              disable: item.disable
            })
          }
          console.log(this.userList)
        } else {
          message.showApiErrorMsg(this, res.data.msg, apiStatus)
        }
      }).catch(err => {
        console.error(err)
        message.showApiErrorMsg(this, err.message)
      })
    },
    editUser(uid, action) {
      /**
       * 编辑用户
       */
      switch (action) {
        // // 编辑用户名
        // case "editUsername":
        //   this.getUserInfo(uid).then(res=>{
        //     this.openInputDialog(uid, "更新用户名", "", res.data.data.userName, (uid, input)=>{
        //       this.updateUserInfo(uid,{userName: input})
        //       this.getUserList(this.search, this.currentPage)
        //     }, "text")
        //   })
        //   break
        // // 编辑真实姓名
        // case "editRealName":
        //   this.getUserInfo(uid).then(res=>{
        //     this.openInputDialog(uid, "更新姓名", "", res.data.data.realName, (uid, input)=>{
        //       this.updateUserInfo(uid, {realName: input})
        //       this.getUserList(this.search, this.currentPage)
        //     }, "text")
        //   })
        //   break
        // // 编辑邮箱
        // case "editEmail":
        //   this.getUserInfo(uid).then(res=>{
        //     this.openInputDialog(uid, "更新邮箱", "", res.data.data.email, (uid, input)=>{
        //       this.updateUserInfo(uid, {email: input})
        //       this.getUserList(this.search, this.currentPage)
        //     }, "email")
        //   })
        //   break
        // // 编辑权限
        case "editPermission":
          this.editUserPermission.uid = uid
          this.editUserPermission.flag = true
          break
        case "editStatus":
          this.editUserStatus.uid = uid
          this.editUserStatus.flag = true
          break
        // // 重置密码
        // case "resetPassword":
        //   this.getUserInfo(uid).then(res=>{
        //     this.openInputDialog(uid, "设置新密码", "至少6字符，必须含有数字，小写字母，大写字母，特殊字符", null,(uid, input)=>{
        //       this.updateUserInfo(uid, {password: input})
        //       this.getUserList(this.search, this.currentPage)
        //     }, "password")
        //   })
        //   break
        // // 删除用户
        // case "delUser":
        //   break
      }
    },
    closeEditUserStatusWindow() {
      /**
       * 关闭编辑用户状态窗口
       * @type {null}
       */
      this.editUserStatus.uid = null
      this.editUserStatus.flag = false
      this.getUserList()
    },
    closeEditUserPermissionWindow() {
      /**
       * 关闭编辑用户权限组窗口
       */
      this.editUserPermission.uid = null
      this.editUserPermission.flag = false
      this.getUserList()
    },
    closeNewUserWindow() {
      this.newUser.flag = false
      this.getUserList()
    }
  },
  mounted() {
    this.getUserList()
  },
  watch: {
    currentPage(val) {
      this.getUserList(this.search, val)
    },
    search(val) {
      this.getUserList(val)
      this.currentPage = 1
    },
  }
}
</script>

<template>
  <div class="toolsBar">
    <v-btn
      id="addUser"
      color="success"
      @click="newUser.flag = true">
      新增用户
    </v-btn>
    <v-text-field
      id="searchUser"
      class="search"
      density="compact"
      label="搜索"
      variant="solo-filled"
      single-line
      hide-details
      v-model="search">
    </v-text-field>
  </div>
  <user-List :user-list="userList" @action="editUser"/>
  <v-pagination
    v-model="currentPage"
    v-if="!maxPage <= 1"
    :length="maxPage"
    :total-visible="6"
    prev-icon="mdi:mdi-menu-left"
    next-icon="mdi:mdi-menu-right"
    rounded="circle"
  ></v-pagination>

  <div class="dialogs">
    <edit-user-status
      :uid="editUserStatus.uid"
      :flag="editUserStatus.flag"
      @close="closeEditUserStatusWindow()"/>
    <edit-user-permission
    :uid="editUserPermission.uid"
    :flag="editUserPermission.flag"
    @close="closeEditUserPermissionWindow()"/>
    <new-user
      :flag="newUser.flag"
      @close="closeNewUserWindow()"/>
  </div>

</template>

<style scoped>

</style>
