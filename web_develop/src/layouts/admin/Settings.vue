<script>
import Main_settings from "@/components/ConfigPage/main_settings.vue";
import Camera_settings from "@/components/ConfigPage/camera_settings.vue";
import Record_settings from "@/components/ConfigPage/record_settings.vue";
import hid_settings from "@/components/ConfigPage/HID_settings.vue";
import Usb_settings from "@/components/ConfigPage/usb_settings.vue";
import Gpio_settings from "@/components/ConfigPage/gpio_settings.vue";

export default {
  name: "Settings",
  components: {Gpio_settings, Usb_settings, hid_settings, Record_settings, Camera_settings, Main_settings}
}
</script>

<template>
  <v-row>
    <v-col>
      <main_settings></main_settings>
    </v-col>
    <v-col>
      <camera_settings></camera_settings>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <record_settings></record_settings>
    </v-col>
    <v-col>
      <hid_settings></hid_settings>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <usb_settings></usb_settings>
    </v-col>
    <v-col>
      <gpio_settings></gpio_settings>
    </v-col>
  </v-row>
</template>

<style scoped>

</style>
