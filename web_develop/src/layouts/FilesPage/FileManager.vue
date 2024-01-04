<script>
import AceEdit from "@/components/AceEdit.vue";
import SparkMD5 from "spark-md5"
// import query from "queue"

import('@/styles/FilesPage/FileManager.scss')
export default {
  name: "FileManager",
  components: {AceEdit},
  data:()=>{
    return {
      websocket: null,
      dialogs: {
        newDir: {
          flag: false,
          input: null
        },
        newFile: {
          flag: false,
          input: null
        },
        reName: {
          flag: false,
          filename: null,
          input: null
        },
        info:{
          flag: false,
          msg: null
        },
        edit:{
          flag: false,
          value: null,
          change: null,
          fileId: null,
          language: null
        },
        uploadFile: {
          flag: false,
          uploading: false,
          preload: false,
          inputFile: [],
          fileInfoList: [],
          uploadProgress: {}
        },
        inputDialog: {
          flag: false,
          input: null,
          title: "",
          label: "",
          type: "text",
          confirmationCallback: null,
          cancelCallback: null
        }
      },
      currentPath: [],
      fileList: [],
      pathBar: [],
      requestDownloadFile: [],
      clipboard: {
        selectedFile: null,
        selectedDir: null,
        mode: null
      }
    }
  },
  methods: {
    // 获取选中的文件列表
    getSelectFileList() {
      let list = []
      const tableRow = document.querySelectorAll(".v-table tbody tr")
      const checks = document.querySelectorAll(".v-table tbody .check .v-checkbox input")
      for (let i = 0; i < checks.length; i++) {
        if (checks[i].checked) {
          list.push(tableRow[i].dataset.filename)
        }
      }
      console.log(list)
      return list
    },
    // 显示信息弹窗
    showInfoMsg(msg) {
      if (!this.dialogs.info.flag) {
        this.dialogs.info.flag = true
        this.dialogs.info.msg = msg
      }
    },
    // 显示输入框
    showInputDialog(title, label, confirmationCallback, cancelCallback=null, type="text") {
      /*
      * title: 输入框标题
      * label: 输入框介绍
      * confirmationCallback: 成功回调
      * cancelCallback: 用户取消回调
      * type: input类型
      * */
      if (!this.dialogs.inputDialog.flag) {
        this.dialogs.inputDialog.input = ""
        this.dialogs.inputDialog.title = title
        this.dialogs.inputDialog.label = label
        this.dialogs.inputDialog.type = type
        this.dialogs.inputDialog.confirmationCallback = confirmationCallback
        this.dialogs.inputDialog.cancelCallback = cancelCallback
        this.dialogs.inputDialog.flag = true
      }
    },
    // 发送Json信息到WebSocket
    sendJsonToWebSocket(data) {
      if (this.websocket != null && this.websocket.readyState === WebSocket.OPEN) {
        try {
          this.websocket.send(JSON.stringify(data))
          return true
        } catch (e) {
          console.error(e.message)
          return false
        }
      } else {
        this.$notify.create({
          text: `服务器未连接，请刷新页面`,
          level: 'error',
          location: 'bottom right',
          notifyOptions: {
            "close-delay": 3000
          }
        })
      }
      return false
    },
    // 新建文件夹
    newDir() {
      let input = this.dialogs.newDir.input
      this.dialogs.newDir.input = null
      this.dialogs.newDir.flag = false
      if (!input || input.length <= 0) {
        this.showInfoMsg("请输入要创建的文件夹名")
        return
      }
      this.sendJsonToWebSocket({
        action: "newDir",
        data: {
          path: this.currentPath,
          dirName: input
        }
      })
    },
    // 新建文件
    newFile() {
      let input = this.dialogs.newFile.input
      this.dialogs.newFile.input = null
      this.dialogs.newFile.flag = false
      if (!input || input.length <= 0) {
        this.showInfoMsg("请输入要创建的文件名")
        return
      }
      this.sendJsonToWebSocket({
        action: "newFile",
        data: {
          path: this.currentPath,
          fileName: input
        }
      })
    },
    // 重命名
    reName(filename) {
      let input = this.dialogs.reName.input
      this.dialogs.reName.input = null
      this.dialogs.reName.flag = false
      if (!input || input.length <= 0) {
        this.showInfoMsg("请输入修改后的文件名")
        return
      }
      this.sendJsonToWebSocket({
        action: "reName",
        data: {
          path: this.currentPath,
          oldFileName: filename,
          newFileName: input
        }
      })
    },
    // 文件操作
    fileAction(filename, action) {
      console.log("action:"+action,"filename:"+filename)
      switch (action) {
        // 编辑
        case "edit":
          this.dialogs.edit.value = ""
          this.sendJsonToWebSocket({
            action: "editFile",
            data: {
              path: this.currentPath,
              filename: filename,
            }
          })
          this.dialogs.edit.language = "text"
          break
        // 下载
        case "download":
          this.requestDownloadFile.push(filename)
          this.newTemporaryLink(filename)
          break
        // 重命名
        case "reName":
          if (this.dialogs.reName.flag === false) {
            this.dialogs.reName.filename = filename
            this.dialogs.reName.input = null
            this.dialogs.reName.flag = true
          }
          break
        // 删除
        case "del":
          this.sendJsonToWebSocket({
            action: "del",
            data: {
              path: this.currentPath,
              filename: filename,
            }
          })
          break
        // 其他
        default:
          break
      }
    },
    // 加载文件列表
    loadFileList(data) {
      console.log("收到后端返回的文件列表")
      this.fileList = []
      this.currentPath = data.path
      console.log("更新当前所在目录:"+this.currentPath)
      this.updatePathBar(this.currentPath)
      let index = 0
      for (let i = 0; i < data.dirs.length; i++) {
        index++
        this.fileList.push({
          fileId:index,
          fileName: data.dirs[i].dirName,
          fileType: "文件夹",
          fileSize: this.formatBytes(data.dirs[i].dirSize),
          uploadTime: data.dirs[i].ctime,
          fileUploader: "未实现",
          fileModifyTime: data.dirs[i].mtime,
          fileModifyUser: "未实现"
        })
      }

      for (let i = 0; i < data.files.length; i++) {
        index++
        this.fileList.push({
          fileId:index,
          fileName: data.files[i].fileName,
          fileType: "文件",
          fileSize: this.formatBytes(data.files[i].fileSize),
          uploadTime: data.files[i].ctime,
          fileUploader: "未实现",
          fileModifyTime: data.files[i].mtime,
          fileModifyUser: "未实现"
        })
      }
      console.log(this.fileList)
    },
    // 更新地址栏
    updatePathBar(path) {
      this.pathBar = []
      for (let i = 0; i < path.length; i++) {
        this.pathBar.push({
          title: path[i],
          disabled: false
        })
      }
    },
    // 发送打开文件夹请求
    openDir(dir) {
      // console.log(`请求打开文件夹：${dir}`)
      let getPath = this.currentPath
      getPath[getPath.length] = dir
      this.sendJsonToWebSocket({
        action: "getFileList",
        data: {
          path: getPath,
        }
      })
    },
    // 返回上级目录
    navigateUpOneDirectory() {
      let pathBuilder = []

      for (let i = 0; i < this.currentPath.length - 1; i++) {
        pathBuilder.push(this.currentPath[i])
      }

      // console.log(pathBuilder)
      this.sendJsonToWebSocket({
        action: "getFileList",
        data: {
          path: pathBuilder,
        }
      })
    },
    // 刷新当前目录
    refresh() {
      this.sendJsonToWebSocket({
        action: "getFileList",
        data: {
          path: this.currentPath,
        }
      })
      this.$notify.create({
        text: `目录已刷新`,
        level: 'success',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 1500
        }
      })
    },
    // 格式化文件大小
    formatBytes(bytes) {
      if (bytes === 0) return '0 字节';
      const k = 1024;
      const sizes = ['字节', 'KB', 'MB', 'GB', 'TB'];

      const i = parseInt(Math.floor(Math.log(bytes) / Math.log(k)));

      return Math.round(100 * (bytes / Math.pow(k, i))) / 100 + ' ' + sizes[i];
    },
    // 上传文件
    async uploadFile() {
      if (!this.dialogs.uploadFile.uploading){
        this.dialogs.uploadFile.uploading = true
        this.dialogs.uploadFile.preload = true
        const file = document.querySelector("#uploadFileDialog .v-card-text .v-file-input input")
        this.dialogs.uploadFile.fileInfoList = []
        this.dialogs.uploadFile.uploadProgress = []
        let chunksList = []
        const uploadToPath = this.currentPath
        // 算出所有文件的md5值并切片
        for (let i = 0; i < file.files.length; i++) {
          const item = file.files[i]
          const chunkSize = 10*1024*1024
          const fileChunks = this.createChunks(item, chunkSize)
          chunksList.push(fileChunks)
          const {fullFileHash, chunkHashList} = await this.hash(fileChunks)
          this.dialogs.uploadFile.fileInfoList.push({
            index: i,  // 文件序号
            filename: item.name,  // 文件名
            filesize: file.size,  // 文件大小
            fileHash: fullFileHash,  // 文件哈希
            chunk: {  // 块
              size: chunkSize,  // 块大小
              List: fileChunks,  // 块列表
              HashList: chunkHashList  // 块哈希列表
            }
          })
          this.dialogs.uploadFile.uploadProgress[item.name] = {value: 0,uploaded: false}
        }

        this.dialogs.uploadFile.preload = false

        // 上传文件到服务器
        for (let i = 0; i < this.dialogs.uploadFile.fileInfoList.length; i++) {
          await awaitBuffered(this)
          const fileInfo = this.dialogs.uploadFile.fileInfoList[i]
          const chunks = fileInfo.chunk.List
          // 分块上传到服务器
          for (let j = 0; j < chunks.length; j++) {
            const chunk = chunks[j]
            await awaitBuffered(this,fileInfo.chunk.size * 4 - fileInfo.chunk.size)
            const loadChunk = new FileReader()
            loadChunk.readAsArrayBuffer(chunk)
            loadChunk.onload = event => {
              // this.sendJsonToWebSocket({
              //   action: "uploadFile",
              //   data: {
              //     filehash: fileInfo.fileHash,
              //     index: j,
              //     length: fileInfo.chunk.List.length,
              //     chunkHash: fileInfo.chunk.HashList[j],
              //     base64: event.target.result
              //   }
              // })
              // 添加MD5到文件头中
              const fileData = appendDataToArrayBuffer(event.target.result,stringToASCII(fileInfo.chunk.HashList[j]+"   IPKVM-Core_FileUploadData   "))
              this.websocket.send(fileData)
              // this.websocket.send(event.target.result)
              console.log(`upload:${fileInfo.filename}-index${j}...`)
              // 更新进度条
              this.dialogs.uploadFile.uploadProgress[fileInfo.filename].value = (j+1) / fileInfo.chunk.List.length * 100
            }
          }
          await awaitBuffered(this)
          // 发送合并请求
          this.sendJsonToWebSocket({
            action: "mergeFile",
            data: {
              path: uploadToPath,
              filename: fileInfo.filename,
              fileHash: fileInfo.fileHash,
              chunksHash: fileInfo.chunk.HashList
            }
          })
          // 更新进度条
          this.dialogs.uploadFile.uploadProgress[fileInfo.filename].uploaded = true
        }
        await awaitBuffered(this)
        // 清除正在上传标志
        this.dialogs.uploadFile.uploading = false
        // 清除文件信息
        this.dialogs.uploadFile.fileInfoList = []
        // 清空文件输入
        this.dialogs.uploadFile.inputFile = []
        this.showInfoMsg("上传完成")
      } else {
        this.showInfoMsg("当前有任务正在上传中")
      }

      // 方法-等待ws队列清空
      async function awaitBuffered(that,threshold = 0) {
        return new Promise((resolve, reject) => {
          const Interval = setInterval(function (){
            if (that.websocket.readyState !== WebSocket.OPEN) {
              reject()
            }
            if (that.websocket.bufferedAmount <= threshold) {
              clearInterval(Interval)
              resolve()
            }
          },100)
        })
      }
      // 将字符串转换成ASCII
      function stringToASCII(String) {
        const encoder = new TextEncoder();
        const asciiBytes = encoder.encode(String);
        return asciiBytes.buffer
      }
      // 将数据附加到ArrayBuffer中
      function appendDataToArrayBuffer(dataArrayBuffer, appendData) {
        let view1 = new Uint8Array(appendData);
        let view2 = new Uint8Array(dataArrayBuffer);
        // 创建一个新的ArrayBuffer，大小为两个ArrayBuffer之和
        let combinedBuffer = new ArrayBuffer(dataArrayBuffer.byteLength + appendData.byteLength);
        // 创建一个新的TypedArray，将buffer1的内容复制到combinedBuffer
        let combinedView = new Uint8Array(combinedBuffer);
        combinedView.set(view1);
        // 创建一个新的TypedArray，将buffer2的内容附加到combinedBuffer
        combinedView.set(view2, view1.length);
        return combinedBuffer
      }
    },
    // 创建分块
    createChunks(file, chunkSize) {
      let res = []
      for (let i = 0; i < file.size; i+=chunkSize) {
        res.push(file.slice(i,i+chunkSize))
      }
      return res
    },
    // 用分块计算哈希
    hash(chunks) {
      return new Promise(resolve => {
        const fullHash = new SparkMD5.ArrayBuffer()
        let chunkHashList = []
        function _read(i) {
          if (i>=chunks.length) {
            const fullFileHash = fullHash.end()
            resolve({fullFileHash, chunkHashList})
            return
          }
          const chunk = chunks[i]
          const file = new FileReader()
          const chunkHash = new SparkMD5.ArrayBuffer()
          file.addEventListener("load",event=>{
            fullHash.append(event.target.result)
            chunkHash.append(event.target.result)
            chunkHashList.push(chunkHash.end())
            _read(i+1)
          })
          file.readAsArrayBuffer(chunk)
        }
        _read(0)
        })
    },
    // 新建临时链接
    newTemporaryLink(filename) {
      this.sendJsonToWebSocket({
        action: "newTemporaryLink",
        data: {
          path: this.currentPath,
          filename: filename
        }
      })
    },
    // 下载临时链接
    tokenDownloadFile(token,filename) {
      if (this.requestDownloadFile.includes(filename)) {
        window.open(`${location.origin}/files/download/${token}`)
      }
    },
    // 编辑文件操作
    editFile(action) {
      switch (action) {
        case "cancelEdit":
          this.sendJsonToWebSocket({
            action: "cancelEdit",
            data: {}
          })
          this.dialogs.edit.value = null
          this.dialogs.edit.change = null
          this.dialogs.edit.flag = false
         break
        case "saveFile":
          this.sendJsonToWebSocket({
            action: "saveFile",
            data: {value:this.dialogs.edit.change}
          })
          break
        default:
          console.error("未知的操作")
          break
      }
    },
    // 压缩文件请求
    compress(filename) {
      console.log(filename)
      this.sendJsonToWebSocket({
        action: "compress",
        data: {
          path: this.currentPath,
          files: this.getSelectFileList(),
          outputName: filename
        }
      })
      this.$notify.create({
        text: `正在压缩文件`,
        level: 'success',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 3000
        }
      })
    },
    // 解压文件请求
    decompress(toPath) {
      console.log(toPath)
      this.sendJsonToWebSocket({
        action: "decompress",
        data: {
          path: this.currentPath,
          files: this.getSelectFileList(),
          decompressToPath: toPath
        }
      })
      this.$notify.create({
        text: `正在解压文件`,
        level: 'success',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 3000
        }
      })
    }
  },
  created() {
    const that = this
    try {
      this.websocket = new WebSocket(`ws://${location.host}/api/websocket/fileManager`)
      this.websocket.addEventListener("open",()=>{
        console.log("Connect WebSocket To FileManager")
        that.$notify.create({
        text: '服务器连接成功',
        level: 'success',
        location: 'bottom right',
        notifyOptions: {
          "close-delay": 3000
        }
      })
        this.sendJsonToWebSocket({action: "getFileList", data: {}})
      })
      this.websocket.addEventListener("error",event=>{
        console.error("WebSocket Error!\n"+event.message)
        that.$notify.create({
          text: `连接发生错误：${event.message}`,
          level: 'error',
          location: 'bottom right',
          notifyOptions: {
            "close-delay": 3000
          }
        })
      })
      this.websocket.addEventListener("close",event=>{
        console.warn(`Connect Close: ${event.code}`)
        that.$notify.create({
            text: `连接已断开：${event.code}`,
            level: 'error',
            location: 'bottom right',
            notifyOptions: {
              "close-delay": 3000
          }
        })
      })
      this.websocket.addEventListener("message",event=>{
        console.log(JSON.parse(event.data))
        const JsonData = JSON.parse(event.data)
        const data = JsonData.data
        switch (JsonData.action) {
          // 返回文件列表
          case "returnFileList":
            that.loadFileList(data)
            break
          // 返回一次性下载链接
          case "returnTemporaryLink": {
            const filename = data.filename
            const token = data.token
            this.tokenDownloadFile(token,filename)
            break
          }
          case "returnEditFileValue": {
            this.dialogs.edit.value = data.value
            this.dialogs.edit.change = data.value
            this.dialogs.edit.flag = true
            break
          }
          case "info": {
            this.$notify.create({
              text: data.msg,
              level: 'info',
              location: 'bottom right',
              notifyOptions: {
                "close-delay": 3000
              }
            })
            break
          }
          case "success": {
            this.$notify.create({
              text: data.msg,
              level: 'success',
              location: 'bottom right',
              notifyOptions: {
                "close-delay": 3000
              }
            })
            break
          }
          case "warning": {
            this.$notify.create({
              text: data.msg,
              level: 'warning',
              location: 'bottom right',
              notifyOptions: {
                "close-delay": 3000
              }
            })
            break
          }
          case "error": {
            this.$notify.create({
              text: data.msg,
              level: 'error',
              location: 'bottom right',
              notifyOptions: {
                "close-delay": 3000
              }
            })
            break
          }
          default:
            break
        }
      })
    } catch (e) {
      console.error(e.message)
    }
  },
  mounted() {
    const that = this
    // 左侧操作栏
    document.querySelector("#fileList .header .bottom .left").addEventListener("click",event=>{
      if (event.target.tagName === 'BUTTON') {
        console.log(event.target.id)
        switch (event.target.id) {
          case "back":
            that.navigateUpOneDirectory()
            break
          case "upload":
            if (that.websocket != null && that.websocket.readyState === WebSocket.OPEN) {
              this.dialogs.uploadFile.flag = true
            } else {
              that.$notify.create({
                text: `服务器未连接，请刷新页面`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          case "refresh":
            that.refresh()
            break
          default:
            console.error("未知操作"+event.target)
        }
      }
    })
    // 右侧操作栏
    document.querySelector("#fileList .header .bottom .right").addEventListener("click",event=>{
      if (event.target.tagName === 'BUTTON') {
        const action = event.target.id
        switch (action){
          case "newDir":
            if (!that.dialogs.newDir.flag) {
              that.dialogs.newDir.flag = true
            }
            break
          case "newFile":
            if (!that.dialogs.newFile.flag) {
              that.dialogs.newFile.flag = true
            }
            break
          case "reName":
            if (!that.dialogs.reName.flag && that.getSelectFileList().length === 1) {
              that.dialogs.reName.flag = true
            } else if (that.getSelectFileList().length > 1) {
              that.showInfoMsg("不能多选文件")
            } else if (that.getSelectFileList().length < 1) {
              that.showInfoMsg("未选择文件")
            }
            break
          case "del":
            if (this.getSelectFileList().length > 0) {
              this.sendJsonToWebSocket({
                action: "del",
                data: {
                  path: this.currentPath,
                  filename: this.getSelectFileList(),
                }
              })
              that.$notify.create({
                text: `正在删除文件`,
                level: 'success',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            } else if (this.getSelectFileList().length >= 0 ) {
              that.$notify.create({
                text: `未选择要删除的文件`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          case "copy":
            if (!this.clipboard.mode && this.getSelectFileList().length > 0) {
              this.clipboard.mode = "copy"
              this.clipboard.selectedDir = this.currentPath.map((x) => x)
              this.clipboard.selectedFile = this.getSelectFileList()
              that.$notify.create({
                text: `已将要复制的文件记录至剪贴板，请前往目标文件夹粘贴`,
                level: 'success',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            } else if (this.getSelectFileList().length <= 0) {
              that.$notify.create({
                text: `未选择要复制的文件`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          case "move":
            if (!this.clipboard.mode && this.getSelectFileList().length > 0) {
              this.clipboard.mode = "move"
              this.clipboard.selectedDir = this.currentPath.map((x) => x)
              this.clipboard.selectedFile = this.getSelectFileList()
              that.$notify.create({
                text: `已将要移动的文件记录至剪贴板，请前往目标文件夹粘贴`,
                level: 'success',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            } else if (this.getSelectFileList().length <= 0) {
              that.$notify.create({
                text: `未选择要移动的文件`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          case "paste":
            if (this.clipboard.mode && this.clipboard.selectedDir !== this.currentPath) {
              this.sendJsonToWebSocket({
                action: this.clipboard.mode,
                data: {
                  sourceFileDirectory: this.clipboard.selectedDir,
                  selectFiles: this.clipboard.selectedFile,
                  toDirectory: this.currentPath
                }
              })
              this.clipboard.mode = null
              this.clipboard.selectedDir = null
              this.clipboard.selectedFile = null
            } else if (this.clipboard.selectedDir === this.currentPath) {
              that.$notify.create({
                text: `不能在源文件夹粘贴`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            } else {
              that.$notify.create({
                text: `剪贴板中没有文件`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          case "compress":
            if (this.getSelectFileList().length > 0) {
              this.showInputDialog("新建压缩包","请输入压缩包名称", this.compress)
            } else {
              that.$notify.create({
                text: `未选择要压缩的文件`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          case "decompress":
            if (this.getSelectFileList().length > 0) {
              this.showInputDialog("将文件解压到","请输入要解压到的目录", this.decompress)
            } else if (this.getSelectFileList().length >= 0 ) {
              that.$notify.create({
                text: `未选择要解压的文件`,
                level: 'error',
                location: 'bottom right',
                notifyOptions: {
                  "close-delay": 3000
                }
              })
            }
            break
          default:
            break
        }
      }
    })
    // 全选文件
    document.querySelector("#allCheck").addEventListener("click",event=>{
      const flag = event.target.checked
      const checks = document.querySelectorAll(".v-table tbody .check .v-checkbox input")
      for (let i = 0; i < checks.length; i++) {
        if (checks[i].checked !== flag) {
          checks[i].click()
        }
      }
    })
    // 点击地址栏
    document.querySelector(".v-breadcrumbs").addEventListener("click", event => {
      if (event.target.classList && event.target.classList[0] === "v-breadcrumbs-item") {
        console.log(event.target.innerHTML)
      }
    })
  }
}
</script>

<template>
  <div id="fileList">
    <div class="header">
      <div class="top">
          <v-breadcrumbs
          :items="pathBar"
          divider=">"
        >
            <template v-slot:prepend>
              <v-icon size="small" icon="mdi:mdi-home-outline"></v-icon>
            </template>
        </v-breadcrumbs>
      </div>
      <div class="bottom">
        <div class="left">
          <v-btn size="x-small" id="refresh" title="刷新" icon="mdi:mdi-refresh">
            <v-icon icon="mdi:mdi-refresh"></v-icon>
<!--            <template v-slot:prepend>-->
<!--              <v-icon icon="mdi:mdi-refresh"></v-icon>-->
<!--            </template>-->
<!--            刷新页面-->
          </v-btn>
          <v-btn size="small" id="upload" title="上传文件">
<!--            <v-icon icon="mdi:mdi-upload"></v-icon>-->
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-upload"></v-icon>
            </template>
            上传文件
          </v-btn>
          <v-btn size="small" id="back" title="返回上级">
<!--            <v-icon icon="mdi:mdi-chevron-up"></v-icon>-->
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-chevron-up"></v-icon>
            </template>
            返回上级
          </v-btn>
        </div>
        <div class="right">
          <v-btn size="small" color="success" id="newDir">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-folder-plus-outline"></v-icon>
            </template>
            新建目录
          </v-btn>
          <v-btn size="small" color="success" id="newFile">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-file-plus-outline"></v-icon>
            </template>
            新建文件
          </v-btn>
          <v-btn size="small" id="copy" :disabled="clipboard.mode !== null">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-file-multiple-outline"></v-icon>
            </template>
            复制
          </v-btn>
          <v-btn size="small" id="move" :disabled="clipboard.mode !== null">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-file-move-outline"></v-icon>
            </template>
            移动
          </v-btn>
          <v-btn size="small" id="paste" :disabled="clipboard.mode === null">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-file-import-outline"></v-icon>
            </template>
            粘贴
          </v-btn>
          <v-btn size="small" id="compress">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-package-variant-closed"></v-icon>
            </template>
            压缩
          </v-btn>
          <v-btn size="small" id="decompress">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-package-variant"></v-icon>
            </template>
            解压
          </v-btn>
          <v-btn size="small" color="error" id="del">
            <template v-slot:prepend>
              <v-icon icon="mdi:mdi-file-remove-outline"></v-icon>
            </template>
            删除
          </v-btn>
        </div>
      </div>
  </div>
    <v-table fixed-header hover>
    <thead>
      <tr>
        <th class="check">
          <v-checkbox id="allCheck" center-affix></v-checkbox>
        </th>
        <th class="text-left">名称</th>
        <th class="text-left">类型</th>
        <th class="text-left">大小</th>
        <th class="text-left">上传时间(上传者)</th>
        <th class="text-left">最后修改(修改人)</th>
        <th class="text-left">操作</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="item in fileList"
        :key="item.name"
        :data-id="item.fileId"
        :data-filename="item.fileName"
      >
        <td class="check"><v-checkbox></v-checkbox></td>
        <td v-if="item.fileType !== '文件夹'" class="file">{{ item.fileName }}</td>
        <td v-if="item.fileType === '文件夹'" class="dir" @click="openDir(item.fileName)">{{ item.fileName }}</td>
        <td>{{ item.fileType }}</td>
        <td>{{ item.fileSize }}</td>
        <td>{{item.uploadTime}}({{ item.fileUploader}})</td>
        <td>{{ item.fileModifyTime }}({{item.fileModifyUser}})</td>
        <td class="action">
          <v-btn class="openEdit" :disabled="item.fileType === '文件夹'" size="small" @click="fileAction(item.fileName, 'edit')">编辑</v-btn>
          <v-btn class="reName" size="small" @click="fileAction(item.fileName, 'reName')">重命名</v-btn>
          <v-btn class="download" size="small" :disabled="item.fileType === '文件夹'" @click="fileAction(item.fileName, 'download')">下载</v-btn>
          <v-btn class="deleteFile" size="small" color="error" @click="fileAction(item.fileName, 'del')">删除</v-btn>
        </td>
      </tr>
    </tbody>
  </v-table>
  </div>
  <div id="dialogs">
<!--    新建文件夹-->
    <v-dialog
        id="newDirDialog"
        v-model="dialogs.newDir.flag"
        activator="parent"
        min-width="400px"
        width="auto"
        persistent
      >
        <v-card>
          <v-card-title>新建文件夹</v-card-title>
          <v-card-text>
            <v-text-field placeholder="请输入要创建的文件夹名称" v-model="dialogs.newDir.input"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="dialogs.newDir.flag = false;dialogs.newDir.input = null">取消</v-btn>
            <v-btn color="success" @click="newDir()">确定</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
<!--    新建文件-->
    <v-dialog
        id="newFileDialog"
        v-model="dialogs.newFile.flag"
        activator="parent"
        min-width="400px"
        width="auto"
        persistent
      >
        <v-card>
          <v-card-title>新建文件</v-card-title>
          <v-card-text>
            <v-text-field placeholder="请输入要创建的文件名称" v-model="dialogs.newFile.input"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="dialogs.newFile.flag = false;dialogs.newFile.input = null">取消</v-btn>
            <v-btn color="success" @click="newFile()">确定</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
<!--    重命名文件-->
    <v-dialog
        id="reNameDialog"
        v-model="dialogs.reName.flag"
        activator="parent"
        min-width="400px"
        width="auto"
        persistent
      >
        <v-card>
          <v-card-title>重命名 {{dialogs.reName.filename}}-->???</v-card-title>
          <v-card-text>
            <v-text-field placeholder="请输入新的名称" v-model="dialogs.reName.input"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="dialogs.reName.flag = false;dialogs.reName.input = null;dialogs.reName.filename = null">取消</v-btn>
            <v-btn color="success" @click="reName(dialogs.reName.filename)">确定</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog
        id="infoDialog"
        v-model="dialogs.info.flag"
        activator="parent"
        min-width="400px"
        width="auto"
        persistent
      >
        <v-card>
          <v-card-text>
            {{ dialogs.info.msg }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" block @click="dialogs.info.flag = false">关闭</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
<!--    编辑文件-->
     <v-dialog
        id="infoDialog"
        v-model="dialogs.edit.flag"
        activator="parent"
        min-width="400px"
        width="auto"
        persistent
      >
        <v-card>
          <v-card-title>编辑器</v-card-title>
          <v-card-text id="edit">
            <ace-edit :value="dialogs.edit.value" :language="dialogs.edit.language" @edit="dialogs.edit.change"></ace-edit>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="editFile('cancelEdit')">关闭</v-btn>
            <v-btn color="success" @click="editFile('saveFile')">保存</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
<!--    上传文件-->
    <v-dialog
        id="uploadFileDialog"
        v-model="dialogs.uploadFile.flag"
        activator="parent"
        min-width="400px"
        width="auto"
        persistent
      >
        <v-card>
          <v-card-title>文件上传</v-card-title>
          <v-card-text v-if="dialogs.uploadFile.preload">
            <v-row
              class="fill-height"
              align-content="center"
              justify="center"
            >
              <v-col
                class="text-subtitle-1 text-center"
                cols="12"
              >
                正在准备上传文件......
              </v-col>
              <v-col cols="6">
                <v-progress-linear
                  color="deep-purple-accent-4"
                  indeterminate
                  rounded
                  height="6"
                ></v-progress-linear>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-text v-if="!dialogs.uploadFile.preload">
<!--            上传文件选择-->
            <v-file-input
              chips
              multiple
              counter
              show-size
              v-model="dialogs.uploadFile.inputFile"
              prepend-icon="mdi:mdi-file"
              label="请选择要上传的文件"
              variant="outlined"
            >
              <template v-slot:selection="{ fileNames }">
                <template v-for="(fileName, index) in fileNames" :key="fileName">
                  <v-chip
                    v-if="index < 2"
                    color="deep-purple-accent-4"
                    label
                    size="small"
                    class="me-2"
                  >
                    {{ fileName }}
                  </v-chip>

                  <span
                    v-else-if="index === 2"
                    class="text-overline text-grey-darken-3 mx-2"
                  >
                    +{{ dialogs.uploadFile.inputFile.length - 2 }} 文件
                  </span>
                </template>
              </template>

            </v-file-input>
<!--            上传进度条-->
            <div class="d-flex flex-column" id="uploadProgress" v-if="dialogs.uploadFile.fileInfoList.length > 0">
              <v-divider></v-divider>
              <div
                v-for="item in dialogs.uploadFile.fileInfoList"
                :key="item.filename"
              >
                <div class="text-caption" v-if="!this.dialogs.uploadFile.uploadProgress[item.filename].uploaded">
                  {{item.filename}}
                </div>
                <v-progress-linear
                  :model-value="this.dialogs.uploadFile.uploadProgress[item.filename].value"
                  v-if="!this.dialogs.uploadFile.uploadProgress[item.filename].uploaded"
                  stream
                  rounded
                ></v-progress-linear>
              </div>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="dialogs.uploadFile.flag = false">关闭</v-btn>
            <v-btn color="success" @click="uploadFile()" :disabled="this.dialogs.uploadFile.uploading">上传</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
<!--    输入框-->
    <v-dialog
      id="inputDialog"
      v-model="dialogs.inputDialog.flag"
      activator="parent"
      min-width="400px"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>{{ dialogs.inputDialog.title }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="dialogs.inputDialog.input" :label="dialogs.inputDialog.label" :type="dialogs.inputDialog.type"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="dialogs.inputDialog.cancelCallback ? dialogs.inputDialog.cancelCallback() : this.dialogs.inputDialog.flag = false">取消</v-btn>
          <v-btn color="success" @click="dialogs.inputDialog.confirmationCallback(this.dialogs.inputDialog.input);this.dialogs.inputDialog.flag = false">确定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
