import { defineStore } from 'pinia'
import axios from "axios";
// 1. 创建store
// 参数1：store的唯一表示
// 参数2：对象，可以提供state actions getters
export const useSettingsStore = defineStore('Settings', {
  state: () => ({
    settings: {}
  }),
  actions: {
    getSettings() {
      return new Promise((resolve, reject) => {
        axios.get('/admin/api/settings/getSettings').then(res=>{
          this.settings = res.data
          console.log(this.settings)
          resolve(this.settings)
        }).catch(err=>{
          console.error(err)
          reject(err)
        })
      })
    },
    saveEditSettings() {
      return new Promise((resolve, reject) => {

      })
    }
  },
  persist: true,
})
