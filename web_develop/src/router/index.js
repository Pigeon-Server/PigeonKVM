// Composables
import {createRouter, createWebHistory} from 'vue-router'
import {setBeforeEach} from '@/router/permission'

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
// import appbar_default from "@/components/header/AppBar_Btn/default.vue"
import appbar_controlPage from "@/components/header/AppBar_Btn/ControlsPage.vue"


const routes = [
    // 登录
    {
        path: '/login',
        name: "login",
        component: login,
        meta: {
            title: "登录"
        },
    },
    // 控制
    // core 无机器列表-直接进入控制页面
    {
        path: '/',
        name: "home",
        components: {
            default: controlPage,
            appBarBtn: appbar_controlPage
        }
    },
    {
        path: '/control',
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
        // component:
        components: {
            default: UserInfo,
        },
        meta: {
            title: "个人信息"
        }
    },
    // 管理 - 用户管理
    {
        path: "/admin/users",
        name: "userManagement",
        components: {
            default: userManagementPage,
        },
        meta: {
            title: "管理 - 用户管理"
        },
    },
    // 管理 - 权限管理
    {
        path: "/admin/permission",
        name: "permissionManagement",
        components: {
            default: permissionManagementPage,
        },
        meta: {
            title: "管理 - 权限管理"
        },
    },
    // 管理 - 审计与日志
    {
        path: "/admin/audit",
        name: "audit",
        components: {
            default: auditAndLoggerPage,
            // appBarBtn: appbar_default
        },
        meta: {
            title: "管理 - 审计与日志"
        },
    },
    // u盘文件管理
    {
        path: "/files",
        name: "files",
        components: {
            default: fileManagementPage,
            // appBarBtn: appbar_default
        },
        meta: {
            title: "文件管理"
        }
    },
    // 设置
    {
        path: "/admin/settings",
        name: "settings",
        components: {
            default: configPage,
            // appBarBtn: appbar_default
        },
        meta: {
            title: "管理 - 设置"
        }
    },
    // 关于
    {
        path: "/about/",
        name: "about",
        component: aboutPage,
        meta: {
            title: "关于PigeonKVM"
        }
    },
    // 错误
    {
        path: '/error/:errorCode',
        name: "error",
        component: errorPage,
        meta: {
            title: "Error!"
        }
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/error/404'
    } // 重定向到404页
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

// 设置路由前置守卫
// setBeforeEach(router)

export default router
