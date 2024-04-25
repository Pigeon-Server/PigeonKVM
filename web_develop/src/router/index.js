// Composables
import { createRouter, createWebHistory } from 'vue-router'
import login from "@/views/Login.vue";
import UserInfo from "@/views/UserInfo.vue";
import controlPage from "@/views/Control.vue"
import userManagementPage from "@/views/admin/User.vue"
import permissionManagementPage from "@/views/admin/Permission.vue"
import auditAndLoggerPage from "@/views/admin/Audit.vue"
import fileManagementPage from "@/views/Files.vue"
import configPage from "@/views/admin/Config.vue"
import aboutPage from "@/views/About.vue"
import errorPage from "@/views/Error.vue"
import appbar_default from "@/components/header/AppBar_Btn/default.vue"
import appbar_controlPage from "@/components/header/AppBar_Btn/ControlsPage.vue"


const routes = [
  // 登录
  {
    path: '/login',
    name: "login",
    component: login,
  },
  // 控制
  // {
  //   path: '/control',
  //   component:() => import('@/views/Control.vue')
  // },
  // core 无机器列表-直接进入控制页面
  {
    path: '/',
    name: "control",
    components: {
      default: controlPage,
      appBarBtn: appbar_controlPage
    }
  },
  // 个人信息设置
  {
    path: '/userInfo',
    name: "userInfo",
    components: {
      default: UserInfo,
    }
  },
  // 管理 - 用户管理
  {
    path: "/admin/users",
    name: "userManagement",
    components: {
      default: userManagementPage,
    }
  },
  // 管理 - 权限管理
  {
    path: "/admin/permission",
    name: "permissionManagement",
    components: {
      default: permissionManagementPage,
    }
  },
  // 管理 - 审计与日志
  {
    path: "/admin/audit",
    name: "audit",
    components: {
      default: auditAndLoggerPage,
      appBarBtn: appbar_default
    }
  },
  // u盘文件管理
  {
    path: "/files",
    name: "files",
    components: {
      default: fileManagementPage,
      appBarBtn: appbar_default
    }
  },
  // 配置文件编辑
  {
    path: "/admin/settings",
    name: "settings",
    components: {
      default: configPage,
      // appBarBtn: appbar_default
    }
  },
  // 关于
  {
    path: "/about/",
    name: "about",
    component:aboutPage
  },
  // 错误
  { path: '/error/:errorCode', component: errorPage },
  { path: '/:pathMatch(.*)*', redirect: '/error/404' } // 重定向到404页
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
