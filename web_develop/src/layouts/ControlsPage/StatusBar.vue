<template>
<!--  <ControlsPage_Settings :flag="Setting_Dialog"></ControlsPage_Settings>-->
  <div class="StatusBar">
    <div class="StatusBar-Content">
      <!--电源-->
      <div id="power-led" class="led-status">
        <v-icon icon="mdi:mdi-power" title="电源灯"/><span>电源</span>
      </div>
      <div class="divider"></div>
      <!--硬盘-->
      <div id="harddisk-led" class="led-status">
        <v-icon icon="mdi:mdi-harddisk" title="硬盘灯"/><span>硬盘</span>
      </div>

      <div class="divider"></div>
      <!--设置-->
      <div id="machine-settings" class="led-status" @click="Setting_Dialog = true">
        <v-icon icon="mdi:mdi-cog-outline" title="设置"/><span>设置</span>
      </div>
    </div>
  </div>
  <div class="dialogs">
    <v-dialog width="700px" v-model="Setting_Dialog" persistent>
    <v-card>
      <v-card-title>
        机器设置
      </v-card-title>
      <v-card-text>
        <v-tabs v-model="tab">
          <v-tab value="graphics">图像设置</v-tab>
          <v-tab value="gpio">GPIO设置</v-tab>
        </v-tabs>
        <v-window v-model="tab" class="pa-3">
          <v-window-item value="graphics">
            <div class="text-caption">
            屏幕分辨率
          </div>
          <v-row>
            <v-col
              cols="12"
              md="6"
            >
              <v-text-field
              label="宽"
              hint="例如：1920"
              type="number"
              v-model="configs.graphics.width"
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              md="6"
            >
              <v-text-field
              label="高"
              hint="例如：1080"
              type="number"
              v-model="configs.graphics.height"
              ></v-text-field>
            </v-col>
          </v-row>

          <div>
            <div class="text-caption">
              帧率
            </div>
            <v-slider
              v-model="configs.graphics.fps"
              thumb-label="always"
              max="60"
              min="24"
              step="1"
            >
              <template v-slot:append>
                <v-text-field
                  v-model="configs.graphics.fps"
                  type="number"
                  style="width: 80px"
                  density="compact"
                  hide-details
                  variant="outlined"
                ></v-text-field>
              </template>
            </v-slider>
          </div>

          <div>
            <div class="text-caption">
              图像更新阈值
            </div>
            <v-slider
              v-model="configs.graphics.updateDisplayChange"
              thumb-label="always"
              max="5"
              min="0.01"
              step="0.01"
            >
              <template v-slot:append>
                <v-text-field
                  v-model="configs.graphics.updateDisplayChange"
                  type="number"
                  style="width: 80px"
                  density="compact"
                  hide-details
                  variant="outlined"
                ></v-text-field>
              </template>
            </v-slider>
          </div>
          <v-checkbox label="显示高级设置" v-model="configs.showAdvanced"></v-checkbox>
          <div v-if="configs.showAdvanced">
            <h3>高级设置</h3>
              <v-alert
                type="warning"
                title="警告"
                text="如果不知道这些配置项的含义，请勿随意更改这些设置"
              ></v-alert>
            <div>
              <div class="text-caption">
                亮度
              </div>
              <v-text-field type="number" v-model="configs.graphics.brightness"></v-text-field>
            </div>
            <div>
              <div class="text-caption">
                曝光
              </div>
              <v-text-field type="number" v-model="configs.graphics.exposure"></v-text-field>
            </div>
            <div>
              <div class="text-caption">
                饱和度
              </div>
              <v-text-field type="number" v-model="configs.graphics.colorfulness"></v-text-field>
            </div>
            <div>
              <div class="text-caption">
                色调
              </div>
              <v-text-field type="number" v-model="configs.graphics.tonal"></v-text-field>
            </div>
          </div>

          </v-window-item>
          <v-window-item value="gpio">
            <div>
               <div class="text-caption">
                轮询率（秒）
              </div>
              <v-text-field type="number" v-model="configs.gpio.pollingRate"></v-text-field>
            </div>
            <v-checkbox label="显示高级设置" v-model="configs.showAdvanced"></v-checkbox>
            <div v-if="configs.showAdvanced">

              <v-alert
                type="error"
                title="警告"
                text="如果不知道这些配置项的含义，请勿随意更改这些设置"
              ></v-alert>
              <v-alert
                type="warning"
                title="提示"
                text="这里的GPIO指的是wiringOP-Python中的wPi序号，请勿填写linux中的gpio子系统序号；具体详情请见OrangePi用户手册"
              ></v-alert>

              <div>
               <div class="text-caption">
                  电源LED-GPIO
                </div>
                <v-text-field type="number" v-model="configs.gpio.GPIO_IdSettings.Power_LED"></v-text-field>
              </div>

              <div>
               <div class="text-caption">
                  硬盘LED-GPIO
                </div>
                <v-text-field type="number" v-model="configs.gpio.GPIO_IdSettings.HDD_LED"></v-text-field>
              </div>

              <div>
               <div class="text-caption">
                  电源键-GPIO
                </div>
                <v-text-field type="number" v-model="configs.gpio.GPIO_IdSettings.Power_Btn"></v-text-field>
              </div>

              <div>
               <div class="text-caption">
                  重启键-GPIO
                </div>
                <v-text-field type="number" v-model="configs.gpio.GPIO_IdSettings.Restart_Btn"></v-text-field>
              </div>

              <div>
               <div class="text-caption">
                  使能U盘-GPIO
                </div>
                <v-text-field type="number" v-model="configs.gpio.GPIO_IdSettings.UsbDisk_EN"></v-text-field>
              </div>

              <div>
               <div class="text-caption">
                  切换U盘-GPIO
                </div>
                <v-text-field type="number" v-model="configs.gpio.GPIO_IdSettings.UsbDisk_Switch"></v-text-field>
              </div>
            </div>
          </v-window-item>
        </v-window>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="warning" @click="Setting_Dialog = false">复位</v-btn>
        <v-btn color="success" @click="Setting_Dialog = false">保存并重启IPKVM Core</v-btn>
        <v-btn color="error" @click="Setting_Dialog = false">取消</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  </div>
</template>

<script>

import ControlsPage_Settings from "@/components/ControlsPage/Settings.vue";
import("@/styles/ControlPage/StatusBar.scss")
export default {
  name: "StatusBar",
  // components: {ControlsPage_Settings},
  data: ()=> {
    return {
      Setting_Dialog: false,
      fps: 30,
      tab: null,
      configs: {
        showAdvanced: false,
        graphics: {
          width: 1920,
          height: 1080,
          fps: 30,
          brightness: -14,
          exposure: -4,
          colorfulness: 164,
          tonal: -4,
          updateDisplayChange: 0.01,
        },
        gpio: {
          pollingRate: 0.5,
          GPIO_IdSettings: {
            Power_LED: 9,
            HDD_LED: 8,
            Power_Btn: 6,
            Restart_Btn: 5,
            UsbDisk_EN: 18,
            UsbDisk_Switch: 17
          }
        }
      }
    }
  }
}
</script>

