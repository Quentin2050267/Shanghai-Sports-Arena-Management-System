<template>
    <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
        :collapse="isCollapse" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
        <h3>{{isCollapse ? '系统' : '上海运动馆管理预约系统'}}</h3>
        <el-menu-item @click="clickMenu(item)" v-for="item in noChildren" :key="item.name" :index="item.name">
            <i :class="`el-icon-${item.icon}`"></i>
            <span slot="title">{{ item.label }}</span>
        </el-menu-item>
        <el-submenu v-for="item in hasChildren" :key="item.label" :index="item.label">
            <template slot="title">
                <i :class="`el-icon-${item.icon}`"></i>
                <span slot="title">{{ item.label }}</span>
            </template>

            <el-menu-item-group v-for="subitem in item.children" :key="subitem.path">
                <el-menu-item @click="clickMenu(subitem)" :index="subitem.path">{{ subitem.label }}</el-menu-item>
            </el-menu-item-group>
        </el-submenu>
    </el-menu>
</template>

  
<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
    /* height: 100vh; */
}

.el-menu {
    height: 100vh;

    h3 {
        color: #fff;
        text-align: center;
        line-height: 48px;
        font-size: 16px;
        font-weight: 400;
    }
}
</style>
  
<script>
export default {
    data() {
        return {
            user_type: "",
            menuDataAdmin: [
                {
                    path: '/admin/home',
                    name: 'home',
                    label: '首页',
                    icon: 's-home',
                    url: 'Home/Home'
                },
                {
                    path: '/admin/gym',
                    name: 'gym',
                    label: '体育馆管理',
                    icon: 'basketball',
                    url: 'GymManage/GymManage'
                },
                {
                    path: '/admin/user',
                    name: 'user',
                    label: '用户管理',
                    icon: 'user',
                    url: 'UserManage/UserManage'
                },
            ],
            menuDataUser: [
                {
                    path: '/user/home',
                    name: 'home',
                    label: '首页',
                    icon: 's-home',
                    url: 'Home/Home'
                },
                {
                    path: '/user/gym',
                    name: 'gym',
                    label: '体育馆预约',
                    icon: 'basketball',
                    url: 'GymManage/GymManage'
                },
                // {
                //     path: '/admin/user',
                //     name: 'user',
                //     label: '用户管理',
                //     icon: 'user',
                //     url: 'UserManage/UserManage'
                // },
            ]
        };
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        // 点击菜单
        clickMenu(item) {
            // 当页面路由不一致时才跳转
            if (this.$router.path !== item.path || (this.$router.path === '/home' && (item.path === '/'))) {
                console.log(item)
                this.$router.push(item.path)
            }
        }
    },
    computed: {
        // 没有子菜单
        noChildren() {
            if (this.user_type=='admin'){
                return this.menuDataAdmin.filter(item => !item.children)
            }
            else{
                return this.menuDataUser.filter(item => !item.children)
            }
        },
        // 有子菜单
        hasChildren() {
            if (this.user_type=='admin'){
                return this.menuDataAdmin.filter(item => item.children)
            }
            else{
                return this.menuDataUser.filter(item => item.children)
            }
        },
        isCollapse() {
            return this.$store.state.tab.isCollapse
        }
    },
    mounted(){
        this.user_type = this.cookie.getCookie('user_type')
    }
}
</script>
<style lang="less" scoped>
.el-menu{
    border-right: none;
}
</style>
  