<template>
  <div class="display">
    <img id="displayImage" draggable="false" alt="">
  </div>
  <v-snackbar
    v-model="error.display"
    color="red-darken-1"
  >
    {{ error.msg }}
    <template v-slot:actions>
      <v-btn
        color="white"
        variant="text"
        @click="error.display = false"
      >
        关闭
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import("@/styles/ControlPage/DisplaySpace.scss")
export default {
  name: "displaySpace",
  data:()=>{
    return {
      // WebSocket对象
      ws: null,
      // 错误消息显示用
      error: {
        display:false,
        msg:""
      },
      // HID 设备状态（待实现）
      HIDStatus: {
        // 是否连接
        LinkStatus: false,
        // 小键盘
        NUM_LOCK: false,
        // 大写锁定
        CAPS_LOOK: false,
        // 复写模式
        SCROLL_LOOK: false
      },
      // 显示图片大小
      displayImageSize: {
        // 原始值
        original: {
          width: null,
          height: null
        },
        // 缩放后
        scaled: {
          width: null,
          height: null,
          // 比例
          ratio: {
            width: 1,
            height: 1,
            zoomRatio: 1
          }
        }
      },
      // 鼠标是否在控制台上
      mouseOnConsole: false
    }
  },
  methods: {
    // 刷新图像
    refreshDisplayImage() {
      const displayImage = document.querySelector("#displayImage")
      displayImage.src = "/api/screen?"+Math.random()
    },
    // 显示错误消息
    displayErrorMsg(msg,timeout) {
      /*
      * msg: 要显示的消息
      * timeout: 消失时间
      * */
      this.error.msg = msg
      this.error.display = true
      let that = this
      setTimeout(()=>{
        that.error.msg = ""
        that.error.display = false
      },timeout)
    },
    // 连接WebSocket
    connectWebSocket() {
      this.ws = new WebSocket(`ws://${location.host}/api/websocket/control`)
      this.ws.binaryType = "arraybuffer"
    },
    // 将WebSocket返回的二进制图像转换为Base64
    arrayBufferToBase64(buffer) {
      /*
      * buffer: 二进制数组(arrayBuffer)
      * */
      let binary = '';
      let bytes = new Uint8Array(buffer);
      for (let i = 0; i < bytes.byteLength; i++) {
          binary += String.fromCharCode(bytes[i]);
      }
      return window.btoa(binary);
    },
    // 计算缩放比例
    calculateScaleRatio(originalWidth, originalHeight, scaledWidth, scaledHeight) {
      /*
      * originalWidth: 原始宽度
      * originalHeight: 原始高度
      * scaledWidth: 缩放后宽度
      * scaledHeight: 缩放后高度
      * */
      const widthScale = scaledWidth / originalWidth;
      const heightScale = scaledHeight / originalHeight;
      return { widthScale, heightScale };
    },
    // // 转换等比例缩放后的点击坐标
    // scaleCoordinates(x, y, scale) {
    //   /*
    //   * x: 点击的x坐标值
    //   * y: 点击的y坐标值
    //   * scale: 缩放比例
    //   * */
    //   const scaledX = x * scale;
    //   const scaledY = y * scale;
    //   return { scaledX, scaledY };
    // }
    // 坐标转换
    coordinateTransformation(coordinates, scale) {
      return  Math.trunc(coordinates / scale)
    }
  },
  created() {
    let that = this
    this.connectWebSocket()
    this.ws.addEventListener("error",event => {
      console.log("WebSocket Error:"+event.message)
      that.$notify.create({
        text: `连接发送错误：${event.message}`,
        level: 'error',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 3000
        }
      })
    })
    this.ws.addEventListener("open", () => {
      console.log("Link WebSocket")
      that.$notify.create({
        text: `连接服务器成功`,
        level: 'success',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 3000
        }
      })
    });
    this.ws.addEventListener("close", event => {
      that.$notify.create({
        text: `连接已断开：${event.code}`,
        level: 'error',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 3000
        }
      })
    })
    this.ws.addEventListener("message", event => {
      const displayImage = document.querySelector("#displayImage")
      if (event.data instanceof ArrayBuffer) {
        displayImage.src='data:image/jpeg;base64,'+that.arrayBufferToBase64(event.data);
      } else {
        const data = JSON.parse(event.data)
        console.log(data)
        switch (data.method) {
          // 初始化页面配置
          case "init":
            console.log("页面配置：\n",data.data)
            that.displayImageSize.original.width = data.data.display.width
            that.displayImageSize.original.height = data.data.display.height
            console.log("初始化页面配置成功")
            break
          // 更新HID设备状态
          case "updateHIDStatus":
            break
          // 更新图像显示
          case "updateDisplayImage":
            this.refreshDisplayImage()
            break
          // 更新LED状态
          case "updateLedStatus":
            break
          // 输入成功
          case "inputSucceed":
            break
          default:
            console.error("服务端返回了未知的方法："+data.method)
            break
        }
        // if (data.status) {
        // } else {
        //   console.error(`服务端返回了错误的状态：${data.msg}(status code:${data.status})`)
        // }
      }
    })
  },
  mounted() {
    const displayImage = document.querySelector("#displayImage");
    displayImage.src = "/api/screen"
    let onMouseMoveEvent,onMouseLeaveEvent = false
    let that = this

    function SendWsData(JsonData) {
      if (that.ws.readyState === WebSocket.OPEN) {
        that.ws.send(JSON.stringify(JsonData))
      } else {
        that.$notify.create({
          text: "未连接到服务器，请刷新页面",
          level: 'error',
          location: 'bottom right',
          notifyOptions: {
            "close-delay": 3000
          }
        })
        that.connectWebSocket()
      }
    }
    // 禁用右键菜单
    displayImage.addEventListener("contextmenu",(event)=>{
      event.preventDefault();
    })
    // 鼠标移动
    displayImage.addEventListener("mousemove", (event) => {
      if (onMouseMoveEvent && (event.movementX !== 0 && event.movementY !== 0)) {
        // console.log(`鼠标移动\nX:${event.offsetX}\tY:${event.offsetY}`)
        let sendData = {
          method:"mousemove",
          data: {
            button: event.button,
            x: that.coordinateTransformation(event.offsetX, that.displayImageSize.scaled.ratio.width),
            y: that.coordinateTransformation(event.offsetY, that.displayImageSize.scaled.ratio.height)
          }
        }
        SendWsData(sendData)
        that.refreshDisplayImage()
      }
    });
    // 鼠标按下
    displayImage.addEventListener("mousedown", (event) => {
      // console.log(`mousedown:\nbutton:${event.button}`)
      onMouseMoveEvent = true
      onMouseLeaveEvent = true
      const sendData = {
        method:"mousedown",
        data: {
          button: event.button,
          x: that.coordinateTransformation(event.offsetX, that.displayImageSize.scaled.ratio.width),
          y: that.coordinateTransformation(event.offsetY, that.displayImageSize.scaled.ratio.height)
        }
      }
      SendWsData(sendData)
      that.refreshDisplayImage()
    });
    // 鼠标抬起
    displayImage.addEventListener("mouseup", (event) => {
      // console.log("mouseup")
      onMouseMoveEvent = false
      onMouseLeaveEvent = false
      const sendData = {
        method:"mouseup",
        data: {
          button: event.button,
          x: that.coordinateTransformation(event.offsetX, that.displayImageSize.scaled.ratio.width),
          y: that.coordinateTransformation(event.offsetY, that.displayImageSize.scaled.ratio.height)
        }
      }
      SendWsData(sendData)
      that.refreshDisplayImage()
    });
    // 鼠标移出
    displayImage.addEventListener("mouseleave", (event) => {
      if (onMouseLeaveEvent) {
        // console.log("鼠标已移出检测区域")
        onMouseMoveEvent = false
        onMouseLeaveEvent = false
        const sendData = {
          method:"mouseup",
          data: {
            button: event.button,
            x: that.coordinateTransformation(event.offsetX, that.displayImageSize.scaled.ratio.width),
            y: that.coordinateTransformation(event.offsetY, that.displayImageSize.scaled.ratio.height)
          }
        }
        SendWsData(sendData)
        that.refreshDisplayImage()
      }
    });
    // 滚轮滚动
    displayImage.addEventListener("wheel", (event)=>{
      if (event.wheelDelta > 0) {
        console.log("正向滚动")
        SendWsData({
          method:"mouseScroll",
          data: {
            direction: "upper",
            x: that.coordinateTransformation(event.offsetX, that.displayImageSize.scaled.ratio.width),
            y: that.coordinateTransformation(event.offsetY, that.displayImageSize.scaled.ratio.height)
          }
        })
      } else if (event.wheelDelta < 0) {
        console.log("反向滚动")
        SendWsData({
          method:"mouseScroll",
          data: {
            direction: "down",
            x: that.coordinateTransformation(event.offsetX, that.displayImageSize.scaled.ratio.width),
            y: that.coordinateTransformation(event.offsetY, that.displayImageSize.scaled.ratio.height)
          }
        })
      }
    })
    // 键盘按下
    window.addEventListener("keydown",event=>{
      if (that.mouseOnConsole) {
        event.preventDefault()
        console.log(event)
        console.log(`
          KeyDown\n
          key:${event.key}\n
          Code:${event.code}\n
          AltKey:${event.altKey}\n
          CtrlKey:${event.ctrlKey}\n
          ShiftKey:${event.shiftKey}\n
          MetaKey:${event.metaKey}
        `)
        const sendData = {
          method: "keydown",
          data: {
            key: event.key,
            code: event.code,
            controlKey: {
              alt: event.altKey,
              ctrl: event.ctrlKey,
              shift: event.shiftKey,
              meta: event.metaKey
            }
          }
        }
        SendWsData(sendData)
        that.refreshDisplayImage()
      }
    })
    // 键盘抬起
    window.addEventListener("keyup",event=>{
      if (that.mouseOnConsole) {
        console.log(`KeyUp\nkey:${event.key}\nCode:${event.code}\nAltKey:${event.altKey}\nCtrlKey:${event.ctrlKey}\nShiftKey:${event.shiftKey}\nMetaKey:${event.metaKey}`)
        const sendData = {
          method: "keyup",
          data: {
            key: event.key,
            code: event.code,
            controlKey: {
              alt: event.altKey,
              ctrl: event.ctrlKey,
              shift: event.shiftKey,
              meta: event.metaKey
            }
          }
        }
        SendWsData(sendData)
        that.refreshDisplayImage()
      }
    })
    // 监听图像大小变化
    const resizeObserver = new ResizeObserver((entries) => {
      entries.forEach(entry => {
        const { target, contentRect } = entry;
        that.displayImageSize.scaled.width = contentRect.width
        that.displayImageSize.scaled.height = contentRect.height
        console.log(target,contentRect.width,contentRect.height)
        const {widthScale, heightScale} = that.calculateScaleRatio(
          that.displayImageSize.original.width,
          that.displayImageSize.original.height,
          that.displayImageSize.scaled.width,
          that.displayImageSize.scaled.height
        )
        that.displayImageSize.scaled.ratio.width = widthScale
        that.displayImageSize.scaled.ratio.height = heightScale
      });
    })
    resizeObserver.observe(displayImage)
    // 监听鼠标位置，判断鼠标是否在控制台上
    window.document.body.onmouseover =  function (event){
      that.mouseOnConsole = (event.target?.id === displayImage.id)
    }
  }
}
</script>
