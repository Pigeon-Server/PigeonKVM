<script>
import axios from "axios";

export default {
  name: "changePassword",
  data: () => {
    return {
      oldPassword: "",
      newPassword: "",
      newPassword2: "",
      PasswordRules: [
        value => {
          if (value?.length >= 6) return true
          return "密码必须大于或等于6个字符"
        }
      ],
      newPasswordRules: [
        value => {
          if (value?.length >= 6 && value === this.newPassword) {
            return true
          } else if (value !== this.newPassword) {
            return "两次输入的密码不一致"
          } else {
            return "密码必须大于或等于6个字符"
          }
        }
      ]
    }
  },
  methods: {
    changePassword() {
      axios.post("userInfo/api/setPassword",{
        data: {
          oldPassword: this.oldPassword,
          newPassword: this.newPassword2
        }
      }).then(res=>{
        const apiStatus = res.data.status
        if (apiStatus === 1) {
          this.$notify.create({
            text: `密码修改成功~`,
            level: 'success',
            location: 'bottom right',
            notifyOptions: {
              "close-delay": 3000
            }
          })
          this.oldPassword = ""
          this.newPassword = ""
          this.newPassword2 = ""
        } else {
          this.$notify.create({
            text: `${res.data.msg}`,
            level: 'error',
            location: 'bottom right',
            notifyOptions: {
              "close-delay": 3000
            }
          })
        }
      }).catch(err=>{
        this.$notify.create({
          text: `API错误：${err.message}`,
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
  <v-card title="修改密码">
    <v-card-text>
      <v-container>
        <v-row>
          <div>
            <div class="text-caption">
              原密码
            </div>
            <v-text-field type="password" v-model="oldPassword" :rules="PasswordRules"></v-text-field>
          </div>
        </v-row>
        <v-row>
          <div>
            <div class="text-caption">
              新密码
            </div>
            <v-text-field type="password" v-model="newPassword" :rules="PasswordRules"></v-text-field>
          </div>
        </v-row>
        <v-row>
          <div>
            <div class="text-caption">
              重复一次新密码
            </div>
            <v-text-field type="password" v-model="newPassword2" :rules="newPasswordRules"></v-text-field>
          </div>
        </v-row>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-btn block color="success" @click="changePassword()">保存修改</v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
  .v-row > div {
    width: 100%;
  }
</style>
