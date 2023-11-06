<script setup>
import axios from 'axios';
import { reactive, ref, onMounted } from 'vue';
import { MessageBox, resetFields } from 'element-ui';
import router from "@/router";


const gyms = reactive([])

const getGyms = () => {
    axios.get('http://127.0.0.1:5000/gym/',).then(res => {
        gyms.splice(0, gyms.length)
        gyms.push(...res.data.results)
        console.log('更新数据')
    })
}

onMounted(() => {
    getGyms()
})


const handleDelete = async (index, scope) => {
    try {
        await MessageBox.confirm('确认删除该条数据？', {
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            type: 'warning'
        })
        await axios.delete(`http://127.0.0.1:5000/gym/${scope.gym_id}`)
        await getGyms()
    } catch (error) {
        console.error(error)
    }
}


const gym_form = reactive({
    gym_id: "",
    gym_district: "",
    gym_name: "",
    gym_address: "",
    facility: [],
    facility_single: ""
})

const gym_form2 = reactive({
    gym_id: "",
    gym_district: "",
    gym_name: "",
    gym_address: "",
})

const showAlert = ref(false)

const add_dialog_visible = ref(false)
const ruleFormRole = ref()
const submitForm = (form) => {
    axios.post('http://127.0.0.1:5000/gym/', gym_form2).then((response) => {
        const result = response.data;
        if (result.status == 'success') {
            add_dialog_visible.value = false
            form.resetFields()
            getGyms()
        }
        else {
            showAlert.value = true
            console.log('提交失败');
        }
    })
}


const resetForm = (form) => {
    showAlert.value = false
    form.resetFields()
    console.log('重置成功');
}

const addFacilityRef = ref()
const add_facility_dialog_visible = ref(false)
const addFacility = (index, scope) => {
    console.log(scope)
    for (let key in scope) {
        // if (key !== 'facility'){
        gym_form[key] = scope[key]
        // }
    }
    console.log(gym_form)

    add_facility_dialog_visible.value = true
}

const submitAddForm = (form) => {
    axios.post('http://127.0.0.1:5000/gym/', gym_form).then((response) => {
        const result = response.data;
        if (result.status == 'success') {
            add_facility_dialog_visible.value = false
            form.resetFields()
            gym_form.facility_single = ''
            getGyms()
        }
        else {
            showAlert.value = true
            console.log('提交失败');
        }
    })
}

const deleteFacilityRef = ref()
const delete_facility_dialog_visible = ref(false)
const deleteFacility = async (index, scope) => {
    for (let key in scope) {
        gym_form[key] = scope[key]
    }
    console.log(gym_form)

    delete_facility_dialog_visible.value = true
}

const submitDeleteForm = (form) => {
    axios.delete(`http://127.0.0.1:5000/gym/${gym_form.gym_id}/${gym_form.facility_single}`).then((response) => {
        const result = response.data;
        if (result.status == 'success') {
            delete_facility_dialog_visible.value = false
            form.resetFields()
            gym_form.facility_single = ''
            getGyms()
        }
        else {
            showAlert.value = true
            console.log('提交失败');
        }
    })
}


const editFacility = (info, idx) => {
    console.log(info.gym_id, info.facility[idx])
    router.push({
        path: '/admin/page1',
        query: {
            gym_id: info.gym_id,
            facility: info.facility[idx]
        }
    });
}

const editFormRef = ref()
const edit_dialog_visible = ref(false)
const handleEdit = (index, scope) => {
    for (let key in scope) {
        gym_form[key] = scope[key]
    }
    edit_dialog_visible.value = true
}

const submitEditForm = (form) => {
    axios.put(`http://127.0.0.1:5000/gym/${gym_form.gym_id}`, gym_form).then((res) => {
        form.resetFields()
        edit_dialog_visible.value = false
        getGyms()
    })
}


// 查询
const gym_name = reactive({
    gym_name: ""
})

const handleSearch = () => {
    axios.put('http://127.0.0.1:5000/gym/0', gym_name).then(res => {
        gyms.splice(0, gyms.length)
        gyms.push(...res.data.results)
    })
}

</script>


<template>
    <div class='gym' style="margin: 0 auto">
        <h1>体育馆管理</h1>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <el-button type="primary" @click="add_dialog_visible = true, showAlert = false" size="small">添加体育馆</el-button>
            <!-- 搜索 -->
            <el-input placeholder="请输入体育馆名称" v-model="gym_name.gym_name" class="input-with-select"
                style="width: 20%; padding-right: 45px;">
                <el-button slot="append" icon="el-icon-search" @click="handleSearch()"></el-button>
            </el-input>
        </div>
        <el-table :data="gyms.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
            style="width: 100% margin: 20px auto; overflow: auto;" height="500" stripe
            :default-sort="{ prop: 'gym_district', order: 'descending' }">

            <el-table-column type="expand">
                <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                        <el-form-item label="运动设施：">
                            <!-- <el-link target="_blank" v-for="facility in props.row.facility" :key="facility"
                                @click="editFacility(props.row)"><span class="space" />{{ facility }} <span
                                    class="space" /></el-link> -->
                            <el-link target="_blank" v-for="(facility, index) in props.row.facility" :key="facility"
                                @click="editFacility(props.row, index)">
                                <span class="space" />{{ facility }} <span class="space" />
                            </el-link>
                            <el-button size="mini" icon="el-icon-plus"
                                @click="addFacility(props.$index, props.row), showAlert = false"></el-button>
                            <el-button size="mini" type="danger" icon="el-icon-delete"
                                @click="deleteFacility(props.$index, props.row)"></el-button>

                        </el-form-item>
                    </el-form>
                </template>
            </el-table-column>

            <el-table-column label="区" prop="gym_district" sortable />

            <el-table-column label="名称" prop="gym_name" sortable />

            <el-table-column label="地址" prop="gym_address" />

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row);">删除</el-button>
                </template>
            </el-table-column>

        </el-table>
        <el-pagination background layout="prev, pager, next,jumper, ->, total, slot" :total="gyms.length"
            @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
            style="text-align: center; padding-top: 20px;">
        </el-pagination>



        <el-dialog title="添加体育馆" :visible.sync="add_dialog_visible" width="30%" :before-close="handleClose">
            <el-form ref="ruleFormRole" :model="gym_form2" status-icon label-width="120px" class="demo-ruleForm">
                <el-form-item label="所在区" prop="gym_district">
                    <el-select v-model="gym_form2.gym_district" placeholder="请选择区域">
                        <el-option label="浦东新区" value="浦东新区"></el-option>
                        <el-option label="黄浦区" value="黄浦区"></el-option>
                        <el-option label="杨浦区" value="杨浦区"></el-option>
                        <el-option label="徐汇区" value="徐汇区"></el-option>
                        <el-option label="奉贤区" value="奉贤区"></el-option>
                        <el-option label="嘉定区" value="嘉定区"></el-option>
                        <el-option label="松江区" value="松江区"></el-option>
                        <el-option label="闵行区" value="闵行区"></el-option>
                        <el-option label="普陀区" value="普陀区"></el-option>
                        <el-option label="长宁区" value="长宁区"></el-option>
                        <el-option label="静安区" value="静安区"></el-option>
                        <el-option label="虹口区" value="虹口区"></el-option>
                        <el-option label="宝山区" value="宝山区"></el-option>
                        <el-option label="金山区" value="金山区"></el-option>
                        <el-option label="青浦区" value="青浦区"></el-option>
                        <el-option label="崇明区" value="崇明区"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="名称" prop="gym_name">
                    <el-input v-model="gym_form2.gym_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="地址" prop="gym_address">
                    <el-input v-model="gym_form2.gym_address" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRole)">提交</el-button>
                    <el-button @click="resetForm(ruleFormRole)">重置</el-button>
                </el-form-item>
            </el-form>
            <el-alert v-if="showAlert" title="该体育馆已存在" type="warning" show-icon @close="showAlert = false">
            </el-alert>
        </el-dialog>

        <el-dialog title="编辑体育馆" :visible.sync="edit_dialog_visible" width="30%" :before-close="handleClose">
            <el-form ref="editFormRef" :model="gym_form" status-icon label-width="120px" class="demo-ruleForm">
                <el-form-item label="所在区" prop="gym_district">
                    <el-select v-model="gym_form.gym_district" placeholder="请选择区域">
                        <el-option label="浦东新区" value="浦东新区"></el-option>
                        <el-option label="黄浦区" value="黄浦区"></el-option>
                        <el-option label="杨浦区" value="杨浦区"></el-option>
                        <el-option label="徐汇区" value="徐汇区"></el-option>
                        <el-option label="奉贤区" value="奉贤区"></el-option>
                        <el-option label="嘉定区" value="嘉定区"></el-option>
                        <el-option label="松江区" value="松江区"></el-option>
                        <el-option label="闵行区" value="闵行区"></el-option>
                        <el-option label="普陀区" value="普陀区"></el-option>
                        <el-option label="长宁区" value="长宁区"></el-option>
                        <el-option label="静安区" value="静安区"></el-option>
                        <el-option label="虹口区" value="虹口区"></el-option>
                        <el-option label="宝山区" value="宝山区"></el-option>
                        <el-option label="金山区" value="金山区"></el-option>
                        <el-option label="青浦区" value="青浦区"></el-option>
                        <el-option label="崇明区" value="崇明区"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="名称" prop="gym_name">
                    <el-input v-model="gym_form.gym_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="地址" prop="gym_address">
                    <el-input v-model="gym_form.gym_address" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitEditForm(editFormRef)">提交</el-button>
                    <el-button @click="resetForm(editFormRef)">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>

        <el-dialog title="添加体育设施" :visible.sync="add_facility_dialog_visible" width="25%" :before-close="handleClose">
            <el-form ref="addFacilityRef" :model="gym_form" status-icon label-width="100px" class="demo-ruleForm">

                <p style="text-align: center; padding-bottom: 20px;">为 {{ gym_form.gym_name }} 添加</p>
                <el-form-item label="设施" prop="facility">
                    <el-input v-model="gym_form.facility_single" autocomplete="off" size="small"
                        style="width: 200px;"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitAddForm(addFacilityRef)">提交</el-button>
                    <el-button @click="resetForm(addFacilityRef)">重置</el-button>
                </el-form-item>
            </el-form>
            <el-alert v-if="showAlert" title="该体育馆已存在该设施" type="warning" show-icon @close="showAlert = false">
            </el-alert>
        </el-dialog>

        <el-dialog title="删除体育设施" :visible.sync="delete_facility_dialog_visible" width="25%" :before-close="handleClose">
            <el-form ref="deleteFacilityRef" :model="gym_form" status-icon label-width="100px" class="demo-ruleForm">

                <p style="text-align: center; padding-bottom: 20px;">为 {{ gym_form.gym_name }} 删除</p>
                <el-form-item label="设施" prop="facility">
                    <el-select v-model="gym_form.facility_single" placeholder="请选择设施">
                        <el-option v-for="option in gym_form.facility" :key="option" :label="option"
                            :value="option"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="submitDeleteForm(deleteFacilityRef)">提交</el-button>
                    <el-button @click="resetForm(deleteFacilityRef)">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>



    </div>
</template>

<script>
export default {
    data() {
        return {
            currentPage: 1,
            pageSize: 20,
            // add_dialog_visible: false
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

.space::after {
    content: '\00a0';
    /* 添加两个空格 */
}
</style>