import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'

import Home from '../views/admin/Home.vue'
import User from '../views/admin/User.vue'
import Gym from '../views/admin/Gym.vue'
import PageOne from '../views/admin/PageOne.vue'

import Home_ from '../views/user/Home.vue'
// import User_ from '../views/user/User.vue'
import Gym_ from '../views/user/Gym.vue'
// import PageOne_ from '../views/user/PageOne.vue'

import PageTwo from '../views/PageTwo.vue'
import Login from '../views/Login.vue'

import cookie from '../utils/cookie.js'

Vue.use(VueRouter)



// 1. 创建路由组件
// 2. 路由与组件映射
// 3. 创建route实例

const routes = [
    // 登录路由
    {
        path: '/',
        component: Login,
        redirect: '/login',
        children: [
            // 子路由
            { path: '/login', component: Login },
        ],
    },
    // 主路由，需要登录后才能访问
    {
        path: '/admin/home',
        component: Main,
        // redirect: '/home',
        children: [
            // 子路由
            { path: '/admin/home', component: Home },
            { path: '/admin/user', component: User },
            { path: '/admin/gym', component: Gym },
            { path: '/admin/page1', component: PageOne },
            { path: '/page2', component: PageTwo }
        ],
    },
    {
        path: '/user/home',
        component: Main,
        // redirect: '/home',
        children: [
            // 子路由
            { path: '/user/home', component: Home_ },
            // { path: '/user/user', component: User },
            { path: '/user/gym', component: Gym_ },
            // { path: '/user/page1', component: PageOne_ },
            { path: '/page2', component: PageTwo }
        ],
    }
]


const router = new VueRouter({
    routes
})

/*
* beforeEach:从一个页面跳转到另外一个页面时触发
* to:要跳转的页面
* from:从哪个页面出来
* next:决定是否通过
*/
router.beforeEach((to, from, next) => {
    // 如果跳转的页面不存在，跳转到404页面
    if (to.matched.length === 0) {
        next('/404')
    }
    if (cookie.getCookie("password")) {
        next()
    } else {
        if (to.path === "/login") {
            next()
        } else {
            next('/login')
        }
    }
})

export default router

