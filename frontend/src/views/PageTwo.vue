<!-- <template>
    <h1>{{facility}}</h1>
</template> -->

<template>
    <div class='gym' style="margin: 0 auto">
        <!-- <h1>个人中心</h1> -->



        <el-descriptions class="margin-top" title="个人信息表" :column="3" border>
            <template slot="extra">
                <el-button type="primary" size="small" v-if="!isEditing" @click="isEditing = true">编辑</el-button>
                <el-button type="primary" size="small" v-else @click="submitEditForm()">保存</el-button>

            </template>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-food"></i>
                    用户ID
                </template>
                <div>{{ ID }}</div>
                <!-- <el-input size="mini" v-else v-model="user.user_id"></el-input> -->
            </el-descriptions-item>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-chicken"></i>
                    用户名
                </template>
                <div v-if="!isEditing">{{ user.user_name }}</div>
                <el-input size="mini" v-else v-model="user.user_name"></el-input>

            </el-descriptions-item>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-burger"></i>
                    电子邮箱
                </template>
                <div v-if="!isEditing">{{ user.user_email }}</div>
                <el-input size="mini" v-else v-model="user.user_email"></el-input>

            </el-descriptions-item>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-sugar"></i>
                    手机号
                </template>
                <div v-if="!isEditing">{{ user.user_phone }}</div>
                <el-input size="mini" v-else v-model="user.user_phone"></el-input>

            </el-descriptions-item>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-ice-cream"></i>
                    用户类型
                </template>
                <div>{{ user.user_type }}</div>


            </el-descriptions-item>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-cold-drink"></i>
                    密码
                </template>
                <div v-if="!isEditing">{{ user.user_password }}</div>
                <el-input size="mini" v-else v-model="user.user_password"></el-input>

            </el-descriptions-item>
            <el-descriptions-item span="3">
                <template slot="label">
                    <i class="el-icon-grape"></i>
                    备注
                </template>
                <el-tag size="small">没啥备注</el-tag>
            </el-descriptions-item>



        </el-descriptions>

    </div>
</template>

<script>
import axios from 'axios';
import { MessageBox, resetFields } from 'element-ui';
import { reactive, ref, onMounted } from 'vue';

export default {

    data() {
        return {
            ID: "",
            user: "",
            isEditing: false,
        }
    },
    mounted() {
        this.ID = this.cookie.getCookie('id')
        this.getOneUser()

    },
    methods: {
        getOneUser() {
            axios.get(`http://127.0.0.1:5000/user/${this.ID}`).then(res => {
                this.user = res.data
                console.log('更新数据')
            })
        },
        handleClose(done) {
            done();
        },
        submitEditForm() {
            axios.put(`http://127.0.0.1:5000/user/${this.ID}`, this.user).then((res) => {
                this.isEditing = false
                this.getOneUser()
            })
        }
    }
}
</script>