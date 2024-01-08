<script>

import base_settings from "@/layouts/admin/Settings/Base_Settings.vue";
import display_settings from "@/layouts/admin/Settings/Display_Settings.vue";
import gpio_settings from "@/layouts/admin/Settings/GPIO_Settings.vue";

export default {
  name: "Settings",
  components: {gpio_settings, display_settings, base_settings},
  data: ()=>{
    return {
      openWindow: null
    }
  }
}
</script>

<template>
  <div class="workspace">
    <v-window v-model="openWindow">
      <v-window-item value="Base_Settings">
        <base_settings/>
      </v-window-item>
      <v-window-item value="Display_Settings">
        <display_settings/>
      </v-window-item>
      <v-window-item value="GPIO_Settings">
        <gpio_settings/>
      </v-window-item>
    </v-window>
    <div class="actionButton">
      <v-btn>取消</v-btn>
      <v-btn>保存</v-btn>
    </div>
  </div>
  <v-list>
    <v-list-subheader>设置项</v-list-subheader>
    <v-list-item
      color="primary"
      value="baseSettings"
      @click="openWindow = 'Base_Settings'"
    >基础设置</v-list-item>
    <v-list-item
      color="primary"
      value="displaySettings"
      @click="openWindow = 'Display_Settings'"
    >录制与显示</v-list-item>
    <v-list-item
      color="primary"
      value="GPIO_Settings"
      @click="openWindow = 'GPIO_Settings'"
    >GPIO</v-list-item>
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
  border: rgba(0,0,0,0.3) solid 0.3px;
  border-radius: 10px;
  margin-right: 15px;
  margin-top: 15px;
}
.v-list .v-list-item {
  white-space:nowrap
}
</style>
