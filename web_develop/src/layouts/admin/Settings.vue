<script>

import base_settings from "@/layouts/admin/Settings/Base_Settings.vue";
import display_settings from "@/layouts/admin/Settings/Display_Settings.vue";
import gpio_settings from "@/layouts/admin/Settings/GPIO_Settings.vue";
import {useSettingsStore} from "@/store/settings";
import axios from "axios";

export default {
  name: "Settings",
  components: {gpio_settings, display_settings, base_settings},
  data: () => {
    return {
      openWindow: "Base_Settings",
      settings: {},
    }
  },
  created() {
    this.getSettings()
  },
  methods: {
    bindData(val) {
      /**
       * 绑定数据
       */
      switch (val) {
        case "Base_Settings":
          this.$nextTick(() => {
            this.$refs.Base_Settings.settings_base = this.settings.base
            this.$refs.Base_Settings.settings_record = this.settings.record
          })
          break
        case "Display_Settings":
          this.$nextTick(() => {
            this.$refs.Display_Settings.settings_camera = this.settings.camera
            this.$refs.Display_Settings.settings_record = this.settings.record
          })
          break
        case "GPIO_Settings":
          this.$nextTick(() => {
            this.$refs.GPIO_Settings.settings_GPIO = this.settings.gpio
          })
          break
      }
    },
    getSettings() {
      /**
       * 获取设置数据
       */
      axios.get('/admin/api/settings/getSettings').then(res=>{
          this.settings = res.data
          this.bindData(this.openWindow)
        }).catch(err=>{
          console.error(err)
        })
    },
    save() {
      /**
       * 保存设置信息
       */
      axios.post('/admin/api/settings/editSettings', this.settings).then(res => {
        this.$notify.create({
          text: '配置保存成功',
          level: 'success',
          location: 'bottom right',
          notifyOptions: {
            "close-delay": 3000
          }
        })
      }).catch(err => {
        console.error(err)
        this.$notify.create({
          text: `保存配置失败：${err.message}`,
          level: 'error',
          location: 'bottom right',
          notifyOptions: {
            "close-delay": 3000
          }
        })
      })
    }
  },
  watch: {
    openWindow(val) {
      this.bindData(val)
    }
  }
}
</script>

<template>
  <div class="workspace">
    <v-window v-model="openWindow">
      <v-window-item value="Base_Settings">
        <base_settings ref="Base_Settings"/>
      </v-window-item>
      <v-window-item value="Display_Settings">
        <display_settings ref="Display_Settings"/>
      </v-window-item>
      <v-window-item value="GPIO_Settings">
        <gpio_settings ref="GPIO_Settings"/>
      </v-window-item>
    </v-window>
    <div class="actionButton">
      <!--      <v-btn>取消</v-btn>-->
      <v-btn @click="save()" color="green">保存</v-btn>
    </div>
  </div>
  <v-list>
    <v-list-subheader>设置项</v-list-subheader>
    <v-list-item
      color="primary"
      value="baseSettings"
      @click="openWindow = 'Base_Settings'"
    >基础设置
    </v-list-item>
    <v-list-item
      color="primary"
      value="displaySettings"
      @click="openWindow = 'Display_Settings'"
    >录制与显示
    </v-list-item>
    <v-list-item
      color="primary"
      value="GPIO_Settings"
      @click="openWindow = 'GPIO_Settings'"
    >GPIO
    </v-list-item>
  </v-list>
</template>

<style scoped>
.v-main {
  padding: 15px;
}

.workspace {
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.workspace .v-window {
  padding: 15px 35px 0 15px;
}

.workspace .actionButton {
  padding: 15px 0 15px 15px
}

.workspace .actionButton .v-btn {
  margin-right: 15px;
}

.v-list {
  width: 30%;
  min-width: 150px;
  height: min-content;
  border: rgba(0, 0, 0, 0.3) solid 0.3px;
  border-radius: 10px;
  margin-right: 15px;
  margin-top: 15px;
}

.v-list .v-list-item {
  white-space: nowrap
}
</style>
