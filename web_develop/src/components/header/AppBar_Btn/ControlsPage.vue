<script>
export default {
  name: "appbar_ControlsPage",
  data: () => {
    return {
      tools_dialog: false,
      tab: null,
      inputString: "",
      deviceConnects: {
        UsbDisk: false
      }
    }
  },
  methods: {
    powerAction(action) {
      switch (action) {
        case "power": {
          this.$dialog.create({
            title: "请确认你的操作",
            text: "你确定要关闭设备吗",
            buttons: [
              { title: '是的，我要执行该操作', key: 'yes', color: "success" },
              { title: '不，我点错了', key: 'no', color: "error" },
            ],
            cardOptions: {},
            dialogOptions: {
              width: "500px",
              persistent: true
            }
          }).then((anwser) => {
            //Do something with the anwser corresponding to the key of the clicked button
            console.log(anwser)
          })
          break
        }
        case "restart": {
          this.$dialog.create({
            title: "请确认你的操作",
            text: "你确定要重启设备吗",
            buttons: [
              { title: '是的，我要执行该操作', key: 'yes', color: "success" },
              { title: '不，我点错了', key: 'no', color: "error" },
            ],
            cardOptions: {},
            dialogOptions: {
              width: "500px",
              persistent: true
            }
          }).then((anwser) => {
            //Do something with the anwser corresponding to the key of the clicked button
            console.log(anwser)
          })
          break
        }
      }
    }
  }
}
</script>

<template>
  <v-btn icon="mdi:mdi-dots-horizontal" title="快捷控制菜单" @click="tools_dialog = true"></v-btn>

  <v-dialog
    transition="dialog-bottom-transition"
    width="auto"
    v-model="tools_dialog"
  >
    <v-card>
      <v-card-title>快捷控制器</v-card-title>
      <v-tabs v-model="tab">
        <v-tab value="powerControls">设备电源控制</v-tab>
        <v-tab value="inputString">快速输入文本</v-tab>
        <v-tab value="deviceConnect">设备连接</v-tab>
      </v-tabs>
      <v-card-text>
        <v-window v-model="tab" class="pa-3">
          <v-window-item value="powerControls">
            <v-container>
              <v-row justify="center">
                <v-col cols="auto">
                  <v-btn title="电源" prepend-icon="mdi:mdi-power" variant="text" id="powerBtn" stacked @click="powerAction('power')">电源</v-btn>
                </v-col>
                <v-col cols="auto">
                  <v-btn title="重启" prepend-icon="mdi:mdi-restart" variant="text" id="restartBtn" stacked @click="powerAction('restart')">重启</v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-window-item>
            <v-window-item value="inputString">
            <v-textarea label="请输入要发送的文本(仅英文和半角字符)" variant="solo" clearable v-model="inputString"></v-textarea>
            <v-btn block color="green-darken-2" prepend-icon="mdi:mdi-send">将文本发送到设备</v-btn>
          </v-window-item>
          <v-window-item value="deviceConnect">
            <v-alert
              density="compact"
              type="warning"
              text="当U盘处于连接状态时，文件管理器将不可用"
              v-if="deviceConnects.UsbDisk"
            ></v-alert>
            <v-switch label="将U盘连接到设备" color="primary" v-model="deviceConnects.UsbDisk"></v-switch>
          </v-window-item>
      </v-window>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
  #powerBtn {
    color: #B71C1C;
  }
  #restartBtn {
    color: #FFA000;
  }
</style>
