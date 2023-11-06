<script setup>
import axios from 'axios';
import { reactive, ref, onMounted, defineExpose } from 'vue';
import { MessageBox, resetFields, validateField } from 'element-ui';

const users = reactive([])

const getUsers = () => {
    axios.get('http://127.0.0.1:5000/user/',).then(res => {
        users.splice(0, users.length)
        users.push(...res.data.results)
        console.log('更新数据')
    })
}

onMounted(() => {
    getUsers()
})

const handleDelete = async (index, scope) => {
    try {
        await MessageBox.confirm('确认删除该条数据？', {
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            type: 'warning'
        })
        await axios.delete(`http://127.0.0.1:5000/user/${scope.user_id}`)
        await getUsers()
    } catch (error) {
        console.error(error)
    }
}


const add_dialog_visible = ref(false)
console.log(add_dialog_visible)
const ruleFormRole = ref()

const user_form = reactive({
    user_id: "",
    user_name: "",
    user_email: "",
    user_phone: "",
    user_password: "",
    user_type: "",
})

const user_form2 = reactive({
    user_id: "",
    user_name: "",
    user_email: "",
    user_phone: "",
    user_password: "",
    check_password: "",
    user_type: "",
})

const showAlert = ref(false)
const showAlertPwd = ref(false)

const submitForm = (form) => {
    if (user_form2.user_password != user_form2.check_password) {
        showAlertPwd.value = true
        console.log('提交失败');
        return
    }
    axios.post('http://127.0.0.1:5000/user/', user_form2).then((response) => {
        const result = response.data;
        if (result.status == 'success') {
            add_dialog_visible.value = false
            form.resetFields()
            getUsers()
        }
        else {
            showAlert.value = true
            console.log('提交失败');
        }
    })
}


const resetForm = (form) => {
    showAlert.value = false
    showAlertPwd.value = false
    form.resetFields()
    console.log('重置成功');
}

const editFormRef = ref()
const edit_dialog_visible = ref(false)
const handleEdit = (index, scope) => {
    for (let key in scope) {
        user_form[key] = scope[key]
    }
    edit_dialog_visible.value = true
}

const submitEditForm = (form) => {
    console.log(`http://127.0.0.1:5000/user/${user_form.user_id}`)
    axios.put(`http://127.0.0.1:5000/user/${user_form.user_id}`, user_form).then((res) => {
        form.resetFields()
        edit_dialog_visible.value = false
        getUsers()
    })
}


// 查询
const user_name = reactive({
    user_name: ""
})

const handleSearch = () => {
    axios.put('http://127.0.0.1:5000/user/0', user_name).then(res => {
        users.splice(0, users.length)
        users.push(...res.data.results)
    })
}

defineExpose({ user_form2 });
</script>

<template>
    <div class='user' style="margin: 0 auto">
        <h1>用户管理</h1>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <el-button type="primary" @click="add_dialog_visible = true, showAlert = false" size="small">添加用户</el-button>
            <!-- 搜索 -->
            <el-input placeholder="请输入用户名称" v-model="user_name.user_name" class="input-with-select"
                style="width: 20%; padding-right: 45px;">
                <el-button slot="append" icon="el-icon-search" @click="handleSearch()"></el-button>
            </el-input>
        </div>
        <el-table :data="users.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
            style="width: 100% margin: 20px auto; overflow: auto;" height="500" stripe
            :default-sort="{ prop: 'user_type', order: 'descending' }">
            <el-table-column label="ID" prop="user_id" sortable />
            <el-table-column label="名称" prop="user_name" />

            <el-table-column label="邮箱" prop="user_email" />

            <el-table-column label="电话" prop="user_phone" />


            <!-- <el-table-column label="密码" prop="user_password"  /> -->
            <el-table-column label="密码" prop="user_password">
                <template slot-scope="{ row }">
                    {{ row.user_password && (row.user_type == 'admin') ? '*'.repeat(8) : row.user_password }}
                </template>
            </el-table-column>


            <el-table-column label="用户类型" prop="user_type" sortable />


            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" v-if="scope.row.user_type !== 'admin'"
                        @click="handleEdit(scope.$index, scope.row)">修改</el-button>
                    <el-button size="mini" v-if="scope.row.user_type !== 'admin'" type="danger"
                        @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>

        </el-table>
        <el-pagination background layout="prev, pager, next,jumper, ->, total, slot" :total="users.length"
            @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
            style="text-align: center; padding-top: 20px;">
        </el-pagination>



        <el-dialog title="添加用户" :visible.sync="add_dialog_visible" width="40%" :before-close="handleClose">
            <el-form ref="ruleFormRole" :model="user_form2" status-icon :rules="rules" label-width="120px"
                class="add-ruleForm">
                <el-form-item label="ID" prop="user_id">
                    <el-input v-model="user_form2.user_id" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="名称" prop="user_name">
                    <el-input v-model="user_form2.user_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="user_email">
                    <el-input v-model="user_form2.user_email" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="电话" prop="user_phone">
                    <el-input v-model="user_form2.user_phone" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="user_password">
                    <el-input type="password" v-model="user_form2.user_password" autocomplete="off"
                        show-password></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="check_password">
                    <el-input type="password" v-model="user_form2.check_password" autocomplete="off"
                        show-password></el-input>
                </el-form-item>
                <el-form-item label="用户类型" prop="user_type">
                    <el-select v-model="user_form2.user_type" placeholder="请选择类型">
                        <el-option label="user" value="user"></el-option>
                        <el-option label="admin" value="admin"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRole)"
                        :disabled="!user_form2.user_id || !user_form2.user_type">提交</el-button>
                    <el-button @click="resetForm(ruleFormRole)" style=" float: right;">重置</el-button>
                </el-form-item>
            </el-form>
            <el-alert v-if="showAlert" title="该用户已存在，请更改ID" type="warning" show-icon @close="showAlert = false" />
            <el-alert v-if="showAlertPwd" title="密码不匹配，请检查" type="warning" show-icon @close="showAlertPwd = false" />
        </el-dialog>


        <el-dialog title="编辑用户" :visible.sync="edit_dialog_visible" width="30%" :before-close="handleClose">
            <el-form ref="editFormRef" :model="user_form" status-icon label-width="120px" class="demo-ruleForm">
                <!-- <el-form-item label="ID" prop="user_id">
                                                <el-input v-model="user_form.user_id" autocomplete="off"></el-input>
                                            </el-form-item> -->
                <el-form-item label="名称" prop="user_name">
                    <el-input v-model="user_form.user_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="user_email">
                    <el-input v-model="user_form.user_email" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="电话" prop="user_phone">
                    <el-input v-model="user_form.user_phone" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="user_password">
                    <el-input v-model="user_form.user_password" autocomplete="off" show-password></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitEditForm(editFormRef)">提交</el-button>
                    <el-button @click="resetForm(editFormRef)" style=" float: right;">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>


    </div>
</template>

<script>
export default {
    data() {
        var checkType = (rule, value, callback) => {
            console.log(value)
            if (!value) {
                return callback(new Error('用户类型不能为空'));
            }
        };
        var checkID = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('ID不能为空'));
            }
        };
        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else {
                // console.log(this.user_form2.check_password)
                if (this.user_form2.check_password !== '') {
                    // console.log('user_form2.check_passworduser_form2.check_passworduser_form2.check_passworduser_form2.check_passworduser_form2.check_passworduser_form2.check_password')
                    this.$refs.ruleFormRole.validateField('check_password');
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            // console.log(value)
            // console.log( this.user_form2.user_password)
            if (value === '') {
                callback(new Error('请再次输入密码'));
            }
            else if (value !== this.user_form2.user_password) {
                callback(new Error('两次输入密码不一致!'));
            }
            else {
                callback();
            }
        };
        return {
            currentPage: 1,
            pageSize: 20,
            // user_form2:  {
            //     user_id: "",
            //     user_name: "",
            //     user_email: "",
            //     user_phone: "",
            //     user_password: "",
            //     check_password: "",
            //     user_type: "",
            // },
            rules: {
                user_password: [
                    {required: true, validator: validatePass, trigger: 'blur' }
                ],
                check_password: [
                    {required: true, validator: validatePass2, trigger: 'blur' }
                ],
                user_id: [
                    {required: true, validator: checkID, trigger: 'blur' }
                ],
                user_type: [
                    {required: true,  trigger: 'change' }
                ]
            }
        };
    },
    methods: {
        //点击按钮切换页面
        handleCurrentChange(currentPage) {
            this.currentPage = currentPage; //每次点击分页按钮，当前页发生变化
            // console.log(this.currentPage);
        },
        handleClose(done) {
            // this.$confirm('确认关闭？')
            //     .then(_ => {
            done();
            // })
            // .catch(_ => { });
        },
    },
    mounted() {

    }
}
</script>

<style lang="less" scoped>
.el-table {
    text-align: center;
}

.add-ruleForm {
    .el-form-item {
        width: 90%;
    }
}

.demo-ruleForm {
    .el-form-item {
        width: 90%;
    }
}
</style>