<script>
export default {
  name: "ControlsPage_Settings",
  props: {
    flag: {
      type: Boolean,
      required: true
    }
  },
  data: () => {
    return {
      openDialog: false
    }
  },
  mounted() {
    this.openDialog = this.flag
  },
  watch: {
    flag(val) {
      this.openDialog = val
    }
  }
}
</script>

<template>
  <v-dialog width="500px" v-model="openDialog" persistent>
    <v-card>
      <v-card-title>
        机器设置
      </v-card-title>
      <v-card-text>
        Test
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="flag = false">保存并重启</v-btn>
        <v-btn color="error">取消</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>
