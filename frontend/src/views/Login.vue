<template>
    <div class="bg-login">
        <!--logo-->
        <!-- <el-image :src="require('@/assets/logo.png')" class="logo" /> -->
        <!--标题-->
        <el-row type="flex" class="row-bg row-two" justify="center">
            <!-- <el-col :span="6"></el-col> -->
            <el-col :span="9">
                <!--标题-->
                <h1 class="title">上海运动馆管理预约系统</h1>
            </el-col>
            <!-- <el-col :span="6"></el-col> -->
        </el-row>
        <!--form表单-->
        <el-row type="flex" class="row-bg card" justify="center">
            <el-col :span="7" class="login-card">
                <!--loginForm-->
                <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="21%" class="loginForm">
                    <el-form-item label="账户" prop="username" style="width: 380px">
                        <el-input v-model="loginForm.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password" style="width: 380px">
                        <el-input type="password" v-model="loginForm.password"></el-input>
                    </el-form-item>
                    <el-form-item class="btn-ground">
                        <el-button type="primary" @click="submitForm('loginForm')">登录</el-button>
                        <el-button @click="resetForm('loginForm')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </div>
</template>
  
<script>
import Element from 'element-ui';
import router from "@/router";
import axios from 'axios';

export default {
    name: "Login",
    data() {
        return {
            // 表单信息
            loginForm: {
                // 账户数据
                username: '',
                // 密码数据
                password: '',
                id: '',
                user_type: '',
            },
            dateInfo:{
                year: "",
                month: "",
                day: ""
            },
            // 表单验证
            rules: {
                // 设置账户效验规则
                username: [
                    { required: true, message: '请输入账户', trigger: 'blur' },
                ],
                // 设置密码效验规则
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                ],
            },
        };
    },
    methods: {
        // 提交表单
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    // 表单验证成功
                    axios.post('http://127.0.0.1:5000/login/', this.loginForm).then(res => {

                        // 拿到结果
                        let status = res.data.status;
                        let message = res.data.message;
                        this.loginForm.id = res.data.user_id;
                        this.loginForm.user_type = res.data.user_type;

                        // 判断结果
                        if (status) {
                            /*登陆成功*/
                            const now = new Date();

                            // 格式化时间
                            this.dateInfo.year = now.getFullYear();
                            this.dateInfo.month = ('0' + (now.getMonth() + 1)).slice(-2);
                            this.dateInfo.day = ('0' + now.getDate()).slice(-2);
                            Element.Message.success(message);
                            this.cookie.setCookie(this.loginForm, 1)
                            this.cookie.setCookie(this.dateInfo, 365)
                            if (res.data.user_type === 'admin') {
                                /*跳转页面*/
                                router.push('/admin/home')
                            }
                            else {
                                /*跳转页面*/
                                router.push('/user/home')
                            }
                        } else {
                            /*打印错误信息*/
                            Element.Message.error(message);
                        }
                    })
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        // 重置表单
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },

    },

}
</script>
  
<style scoped>


.bg-login {
    height: 762px;
    /* height: 100%; */
    background-image: url("../assets/images/background.jpg");
    background-size: 150%;

}

.btn-ground {
    text-align: center;
}


.title {
    text-shadow: -3px 3px 1px #5f565e;
    text-align: center;
    margin-top: 40%;
    color: #41b9a6;
    font-size: 40px;
}

.login-card {
    background-color: #ffffff;
    opacity: 0.9;
    box-shadow: 0 0 20px #ffffff;
    border-radius: 10px;
    padding: 40px 40px 30px 15px;
    width: auto;
}
</style>
  