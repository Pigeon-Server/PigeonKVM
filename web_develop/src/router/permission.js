import { useUserStore } from '@/store/userInfo'

//路由白名单列表，把路由添加到这个数组，不用登陆也可以访问
const whiteList = ['/login', '/handbook']

export function setBeforeEach(router) {
  router.beforeEach(async (to, from, next) => {
    // 设置标题
    if (to.meta.title) {
      document.title = to.meta.title
    }

    const userStore = useUserStore()
    // const permissionStore = usePermissionStore()
    console.log(to.path)
    //如果存在token，即存在已登陆的令牌
    if (userStore.id) {
      //如果用户存在令牌的情况请求登录页面，就让用户直接跳转到首页，避免存在重复登录的情况
      if (to.path === '/login') {
        // 直接跳转到首页，取决于你的路由重定向到哪里
        next({ path: '/' })
      } else {
        next()
      }
    } else {
      //这里是没有令牌的情况
      //whiteList.indexOf(to.path) !== -1)判断用户请求的路由是否在白名单里
      if (whiteList.indexOf(to.path) !== -1) {
        // 不是-1就证明存在白名单里，不管你有没有令牌，都直接去到白名单路由对应的页面
        next()
      } else {
        // 如果这个页面不在白名单里，直接跳转到登录页面
        next(`/login?redirect=${to.path}`)
      }
    }
  })
}
