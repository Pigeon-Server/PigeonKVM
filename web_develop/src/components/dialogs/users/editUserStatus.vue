<script>
import user from "@/scripts/admin/users"
import message from "@/scripts/utils/message";

export default {
  name: "editUserStatus",
  data() {
    return {
      value: null
    }
  },
  emits: ['close'],
  props: {
    flag: {
      type: Boolean,
      required: true
    },
    uid: {
      type: Number,
      required: true
    }
  },
  methods: {
    submitForm() {
      user.updateUserInfo(this, this.uid, {disable: this.value}).then(()=>{
        this.handleClose()
      })
    },
    handleClose() {
      this.$emit('close')
    }
  },
  watch: {
    flag(val) {
      if (val) {
        user.getUserInfo(this, this.uid).then(res => {
          const apiStatus = res.data.status
          if (apiStatus != 1) {
            message.showApiErrorMsg(this, res.data.msg)
            return
          }
          this.value = res.data.data.disable
        })
      } else {
        this.value = null
      }
    }
  }
}
</script>

<template>
  <v-dialog
    :model-value="flag"
    activator="parent"
    min-width="400px"
    width="auto"
    persistent
  >
    <v-card>
      <v-card-title>编辑用户状态</v-card-title>
      <v-card-text>
        <input type="radio" name="userStatus" value="false" v-model="value"><span>启用</span>
        <input type="radio" name="userStatus" value="true" v-model="value"><span>禁用</span>
      </v-card-text>
      <v-card-actions>
        <v-btn color="error" @click="handleClose()">取消</v-btn>
        <v-btn color="success" @click="submitForm()">确定</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>
