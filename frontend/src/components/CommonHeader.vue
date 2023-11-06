<template>
    <div class="header-container">
        <div class="l-content">
            <el-button @click="handleMenu()" icon="el-icon-menu" size="mini"></el-button>
            <!-- 面包屑 -->
            <!-- <span class="text">首页</span> -->
        </div>
        <div class="r-content">
            <el-dropdown>
                <span class="el-dropdown-link">
                    <img class="user" src="../assets/images/admin/profile.png" alt="" v-if="user_type == 'admin'">
                    <img class="user" src="../assets/images/user/profile.jpg" alt="" v-if="user_type == 'user'">
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="person()">个人中心</el-dropdown-item>
                    <el-dropdown-item @click.native="exit()">退出</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            user_type: ""
        }
    },
    mounted() {
        this.user_type = this.cookie.getCookie('user_type')
    },
    methods: {
        handleMenu() {
            this.$store.commit('collapseMenu')
        },
        exit() {
            this.cookie.clearCookie('username')
            this.cookie.clearCookie('password')
            this.$router.replace('/login')
        },
        person() {
            this.$router.replace('/page2')
        }
    }
}
</script>

<style lang="less" scoped>
.header-container {
    padding: 0px 20px;
    background-color: #333;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .text {
        color: #fff;
        font-size: 14px;
        margin: 10px;
    }

    .r-content {
        .user {
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }
    }
}
</style>