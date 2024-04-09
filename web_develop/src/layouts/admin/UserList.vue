<script>
import message from "@/scripts/utils/message.js"
import axios from "axios";

import('@/styles/Admin/UserList.scss')
export default {
  name: "UserList",
  data: () => {
    return {
      maxPage: null,
      currentPage: null,
      search: "",
      userList: [],
      permissionGroupsList: [],
      inputDialog: {
        flag: false,
        input: null,
        uid: null,
        title: null,
        label: null,
        type: null,
        callback: null
      },
      newUserDialog: {
        flag: false,
        userName: null,
        realName: null,
        email: null,
        password: null,
        disable: false
      },
      editUserPermission: {
        flag: false,
        userId: null,
        maxPage: null,
        currentPage: 1,
        search: "",
        selected: null
      },
      editUserStatus: {
        flag: false,
        userId: null,
        value: null
      }
    }
  },
  methods: {
    // 获取用户列表
    getUserList(search="", page=1, pageSize=20) {
      axios.post("/admin/api/getUserList",{
        page: page,
        pageSize: pageSize,
        search: search
      }).then(res=>{
        const apiStatus = res.data.status
          if (apiStatus === 1) {
            const data = res.data.data
            const PageContent = data.PageContent
            this.userList = []
            this.maxPage = data.maxPage
            this.currentPage = data.currentPage
            for (const item of PageContent) {
              console.log(item)
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
            message.showApiErrorMsg(this, res.data.msg,apiStatus)
          }
      }).catch(err=>{
        console.error(err)
        message.showApiErrorMsg(this, err.message)
      })
    },
    // 打开输入框
    openInputDialog(uid, title, label, defaultValue, callback=null, type="text") {
      if (!this.inputDialog.flag) {
        this.inputDialog.flag = true
        this.inputDialog.uid = uid
        this.inputDialog.title = title
        this.inputDialog.label = label
        this.inputDialog.input = defaultValue
        this.inputDialog.type = type
        this.inputDialog.callback = callback
      } else {
        console.warn("当前已有开启中的输入框")
      }
    },
    // 获取用户信息
    getUserInfo(uid) {
      return axios.post("/admin/api/getUserInfo",{id:uid}).catch(err=>{
        message.showApiErrorMsg(this, err.message)
      })
    },
    // 更新用户信息
    updateUserInfo(uid, data) {
      data = {id: uid, data: data}
      axios.post("/admin/api/setUserInfo",data).then(res=>{
        const status = res.data.status
        if (status !== 1) {
         message.showApiErrorMsg(this, res.data.msg, status)
         return false
        } else {
          return true
        }
      }).catch(err=>{
        console.error(err)
        message.showApiErrorMsg(this, err.message)
        return false
      })
    },
    // 新增用户
    newUser() {
      axios.post("/admin/api/addUser", {
        userName: this.newUserDialog.userName,
        realName: this.newUserDialog.realName,
        email: this.newUserDialog.email,
        password: this.newUserDialog.password,
        disable: this.newUserDialog.disable
      }).then(res=>{
        const status = res.data.status
        if (status !== 1) {
          message.showApiErrorMsg(this, res.data.msg, status)
        } else {
          this.getUserList("", this.maxPage)
        }
        this.newUserDialog.flag = false
      }).catch(err=>{
        message.showApiErrorMsg(this, err.message)
      })
    },
    // 删除用户
    delUser(uid) {
      this.$dialog.confirm("操作确认", "确定要删除这个用户吗", 'warning', '否', '是')
      .then((anwser) => {
        if (anwser) {
          axios.post("/admin/api/delUser", {id:uid}).then(res=>{
            const status = res.data.status
            if (status !== 1) {
              message.showApiErrorMsg(this, res.data.msg, status)
            } else {
              this.getUserList("", this.maxPage)
            }
          }).catch(err=>{
            message.showApiErrorMsg(this, err.message)
          })
        }
        this.newUserDialog.flag = false
      })
    },
    editPermission(uid) {
      this.updateUserInfo(uid,{permission: this.editUserPermission.selected})
      this.editUserPermission.flag = false
      this.getUserList(this.search, this.maxPage)
    },
    loadPermissionGroups(search, page, pageSize=20) {
      axios.post("/admin/api/getPermissionGroups", {search:search, page: page, pageSize: pageSize}).then(res=>{
        const apiStatus = res.data.status
        if (apiStatus === 1) {
          this.editUserPermission.maxPage = res.data.data.maxPage
          this.editUserPermission.currentPage = res.data.data.currentPage
          this.permissionGroupsList = []
          for (let i = 0; i < res.data.data.PageContent.length; i++) {
            const item = res.data.data.PageContent[i]
            this.permissionGroupsList.push({
              id: item.id,
              name: item.name
            })
          }
        } else {
          message.showApiErrorMsg(this, res.data.msg,apiStatus)
        }
      }).catch(err=>{
        console.error(err)
        message.showApiErrorMsg(this, err.message)
      })
    },
    // 编辑用户
    editUser(uid ,action) {
      switch (action) {
        // 编辑用户名
        case "editUsername":
          this.getUserInfo(uid).then(res=>{
            this.openInputDialog(uid, "更新用户名", "", res.data.data.userName, (uid, input)=>{
              this.updateUserInfo(uid,{userName: input})
              this.getUserList(this.search, this.currentPage)
            }, "text")
          })
          break
        // 编辑真实姓名
        case "editRealName":
          this.getUserInfo(uid).then(res=>{
            this.openInputDialog(uid, "更新姓名", "", res.data.data.realName, (uid, input)=>{
              this.updateUserInfo(uid, {realName: input})
              this.getUserList(this.search, this.currentPage)
            }, "text")
          })
          break
        // 编辑邮箱
        case "editEmail":
          this.getUserInfo(uid).then(res=>{
            this.openInputDialog(uid, "更新邮箱", "", res.data.data.email, (uid, input)=>{
              this.updateUserInfo(uid, {email: input})
              this.getUserList(this.search, this.currentPage)
            }, "email")
          })
          break
        // 编辑权限
        case "editPermission":
          this.editUserPermission.selected = null
          this.editUserPermission.search = ""
          this.editUserPermission.maxPage = null
          this.editUserPermission.currentPage = 1
          this.editUserPermission.userId = uid
          this.editUserPermission.flag = true
          this.loadPermissionGroups("", 1)
          break
        case "editStatus":
          this.getUserInfo(uid).then(res=>{
            this.editUserStatus.value = String(res.data.data.disable)
            this.editUserStatus.userId = uid
            this.editUserStatus.flag = true
          })
          break
        // 重置密码
        case "resetPassword":
          this.getUserInfo(uid).then(res=>{
            this.openInputDialog(uid, "设置新密码", "至少6字符，必须含有数字，小写字母，大写字母，特殊字符", null,(uid, input)=>{
              this.updateUserInfo(uid, {password: input})
              this.getUserList(this.search, this.currentPage)
            }, "password")
          })
          break
        // 删除用户
        case "delUser":
          break
      }
    }
  },
  watch: {
    currentPage(val) {
      this.getUserList(this.search ,val)
    },
    search(val) {
      this.getUserList(val)
      this.currentPage = 1
    },
    "editUserPermission.currentPage"(val) {
      this.loadPermissionGroups(this.editUserPermission.search, val)
    },
    "editUserPermission.search"(val) {
      this.loadPermissionGroups(val, 1)
      this.editUserPermission.currentPage = 1
    }
  },
  created() {
    this.getUserList()
  },
}
</script>

<template>
  <div class="toolsBar">
    <v-btn id="addUser" color="success" @click="newUserDialog.flag = true">新增用户</v-btn>
    <v-text-field id="searchUser" class="search" density="compact" label="搜索" variant="solo-filled" single-line hide-details v-model="search"></v-text-field>
  </div>
  <v-table>
    <thead>
      <tr>
        <th class="text-left">
          UID
        </th>
        <th class="text-left">
          用户名
        </th>
        <th class="text-left">
          真实姓名
        </th>
        <th class="text-left">
          邮箱
        </th>
        <th class="text-left">
          权限
        </th>
        <th class="text-left">
          状态
        </th>
        <th class="text-left">
          创建时间
        </th>
        <th class="text-left">
          上次登录时间
        </th>
        <th class="text-left">
          操作
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="item in userList"
        :key="item.name"
      >
        <td>{{ item.uid }}</td>
        <td>{{ item.userName }}<v-icon icon="mdi:mdi-square-edit-outline" size="x-small" @click="editUser(item.uid, 'editUsername')"></v-icon></td>
        <td>{{ item.realName ? item.realName : "未设置" }}<v-icon icon="mdi:mdi-square-edit-outline" size="x-small" @click="editUser(item.uid, 'editRealName')"></v-icon></td>
        <td>{{item.email ? item.email : "未设置"}}<v-icon icon="mdi:mdi-square-edit-outline" size="x-small" @click="editUser(item.uid, 'editEmail')"></v-icon></td>
        <td>{{ item.permission_name ? item.permission_name : "无权限" }}<v-icon icon="mdi:mdi-square-edit-outline" size="x-small" @click="editUser(item.uid, 'editPermission')"></v-icon></td>
        <td>{{ item.disable ? "已禁用" : "已启用" }}<v-icon icon="mdi:mdi-square-edit-outline" size="x-small" @click="editUser(item.uid, 'editStatus')"></v-icon></td>
        <td>{{ item.createdAt ? item.createdAt : "未知" }}</td>
        <td>{{ item.lastLoginTime ? `${item.lastLoginTime}（ip:${item.lastLoginIP}）` : "未登录" }} </td>
        <td>
          <v-btn size="small" @click="editUser(item.uid, 'resetPassword')">重置密码</v-btn>
          <v-btn size="small" color="error" @click="delUser(item.uid)">删除</v-btn>
        </td>
      </tr>
    </tbody>
  </v-table>
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
<!--    通用输入框-->
    <v-dialog
      id="inputDialog"
      v-model="inputDialog.flag"
      activator="parent"
      min-width="400px"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>{{ inputDialog.title }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="inputDialog.input" :label="inputDialog.label" :type="inputDialog.type"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="inputDialog.flag = false;inputDialog.input = null">取消</v-btn>
          <v-btn color="success" @click="inputDialog.callback ? inputDialog.callback(inputDialog.uid, inputDialog.input) : null;inputDialog.flag = false;inputDialog.input = null">确定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
<!--    新增用户-->
    <v-dialog
      id="inputDialog"
      v-model="newUserDialog.flag"
      activator="parent"
      min-width="400px"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>新增用户</v-card-title>
        <v-card-text>
          <div>
            <div class="text-caption">
              用户名
            </div>
            <v-text-field type="text" v-model="newUserDialog.userName"></v-text-field>
          </div>
          <div>
            <div class="text-caption">
              真实姓名
            </div>
            <v-text-field type="text" v-model="newUserDialog.realName"></v-text-field>
          </div>
          <div>
            <div class="text-caption">
              邮箱
            </div>
            <v-text-field type="email" v-model="newUserDialog.email"></v-text-field>
          </div>
          <div>
            <div class="text-caption">
              密码
            </div>
            <v-text-field type="password" v-model="newUserDialog.password"></v-text-field>
          </div>
          <v-switch color="primary" label="禁用用户" v-model="newUserDialog.disable"></v-switch>
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="newUserDialog.flag = false">取消</v-btn>
          <v-btn color="success" @click="newUser()">确定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
<!--    修改权限-->
    <v-dialog
      id="inputDialog"
      v-model="editUserPermission.flag"
      activator="parent"
      min-width="400px"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>修改用户权限</v-card-title>
        <v-card-text>
          <div class="toolsBar">
            <v-text-field id="searchUser" class="search" density="compact" label="搜索" variant="solo-filled" single-line hide-details v-model="editUserPermission.search"></v-text-field>
          </div>
          <v-table>
            <thead>
              <tr>
                <th class="text-left">
                  选择
                </th>
                <th class="text-left">
                  权限ID
                </th>
                <th class="text-left">
                  权限组名
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in permissionGroupsList"
                :key="item.id"
              >
                <td><input type="radio" name="editUserPermission" :value="item.id" v-model="editUserPermission.selected"></td>
                <td>{{ item.id }}</td>
                <td>{{ item.name }}</td>
              </tr>
            </tbody>
          </v-table>
          <v-pagination
            v-model="editUserPermission.currentPage"
            v-if="!editUserPermission.maxPage <= 1"
            :length="editUserPermission.maxPage"
            :total-visible="6"
            prev-icon="mdi:mdi-menu-left"
            next-icon="mdi:mdi-menu-right"
            rounded="circle"
          ></v-pagination>
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="editUserPermission.flag = false">取消</v-btn>
          <v-btn color="success" @click="editPermission(editUserPermission.userId)">确定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
<!--    修改状态-->
        <v-dialog
      id="inputDialog"
      v-model="editUserStatus.flag"
      activator="parent"
      min-width="400px"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>编辑用户状态</v-card-title>
        <v-card-text>
          <input type="radio" name="userStatus" value="false" v-model="editUserStatus.value"><span>已启用</span>
          <input type="radio" name="userStatus" value="true" v-model="editUserStatus.value"><span>禁用</span>
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="editUserStatus.flag = false">取消</v-btn>
          <v-btn color="success" @click="this.updateUserInfo(editUserStatus.userId,{disable: editUserStatus.value});editUserStatus.flag = false">确定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>

</style>
