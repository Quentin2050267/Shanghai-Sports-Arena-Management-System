<template>
    <div class='gym' style="margin: 0 auto">
        <h1>体育设施时间管理</h1>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <el-button type="primary" @click="add_dialog_visible = true, showAlert = false" size="small">添加时间段</el-button>
            <!-- 搜索 -->
            <!-- <el-input placeholder="请输入体育馆名称" v-model="gym_name.gym_name" class="input-with-select"
                style="width: 20%; padding-right: 45px;">
                <el-button slot="append" icon="el-icon-search" @click="handleSearch()"></el-button>
            </el-input> -->
        </div>
        <el-table :data="facility.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
            style="width: 100% margin: 20px auto; overflow: auto;" height="500"
            :default-sort="{ prop: 'date', order: 'descending' }">


            <el-table-column label="日期" prop="date" sortable />

            <el-table-column label="开放时间" prop="start_time" />

            <el-table-column label="结束时间" prop="end_time" />

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>

        </el-table>
        <el-pagination background layout="prev, pager, next,jumper, ->, total, slot" :total="facility.length"
            @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
            style="text-align: center; padding-top: 20px;">
        </el-pagination>


        <el-dialog title="添加时间段" :visible.sync="add_dialog_visible" width="30%" :before-close="handleClose">
            <el-form ref="ruleFormRole" :model="singleFacility" status-icon label-width="120px" class="demo-ruleForm">
                <el-form-item label="开放日期">
                    <el-col :span="11">
                        <el-date-picker type="date" placeholder="选择日期" v-model="singleFacility.date"
                            style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>
                <el-form-item label="开放时间段">

                    <el-col :span="11">
                        <el-time-picker placeholder="选择时间" v-model="singleFacility.start_time"
                            style="width: 100%;"></el-time-picker>
                    </el-col>
                    <el-col class="line" :span="1"> &nbsp-</el-col>
                    <el-col :span="11">
                        <el-time-picker placeholder="选择时间" v-model="singleFacility.end_time"
                            style="width: 100%;"></el-time-picker>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm()">提交</el-button>
                </el-form-item>
            </el-form>
            <el-alert v-if="showAlert" title="该时间段已存在" type="warning" show-icon @close="showAlert = false">
            </el-alert>
        </el-dialog>


        <el-dialog title="编辑时间段" :visible.sync="edit_dialog_visible" width="30%" :before-close="handleClose">
            <el-form ref="editFormRef" :model="singleFacility2" status-icon label-width="120px" class="demo-ruleForm">
                <el-form-item label="开放日期">
                    <el-col :span="11">
                        <el-date-picker type="date" placeholder="选择日期" v-model="singleFacility2.date"
                            style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>
                <el-form-item label="开放时间段">

                    <el-col :span="11">
                        <el-time-picker placeholder="选择时间" v-model="singleFacility2.start_time"
                            style="width: 100%;"></el-time-picker>
                    </el-col>
                    <el-col class="line" :span="1"> &nbsp-</el-col>
                    <el-col :span="11">
                        <el-time-picker placeholder="选择时间" v-model="singleFacility2.end_time"
                            style="width: 100%;"></el-time-picker>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitEditForm()">提交</el-button>
                    <el-button @click="resetForm()">重置</el-button>
                </el-form-item>
            </el-form>
            <el-alert v-if="showAlert" title="该时间段已存在" type="warning" show-icon @close="showAlert = false">
            </el-alert>
        </el-dialog>


    </div>
</template>

<script>
import axios from 'axios';
import { MessageBox, resetFields } from 'element-ui';
import { reactive, ref, onMounted } from 'vue';

export default {

    data() {
        return {
            currentPage: 1,
            pageSize: 20,
            facility: [],
            add_dialog_visible: false,
            edit_dialog_visible: false,
            singleFacility: {
                facilityID: "",
                date: "",
                start_time: "",
                end_time: ""
            },
            singleFacility2: {
                facilityID: "",
                date: "",
                start_time: "",
                end_time: ""
            },
            showAlert: false,
            ruleFormRole: ref(),
            tmp: {}
        }
    },
    mounted() {
        this.getFacilityTime()

    },
    methods: {
        getFacilityTime() {
            axios.get(`http://127.0.0.1:5000/page1/${this.$route.query.gym_id}/${this.$route.query.facility}`,).then(res => {
                this.singleFacility.facilityID = res.data.facility_id
                this.facility.splice(0, this.facility.length)
                this.facility.push(...res.data.results)
                // 转换时间
                this.facility = this.facility.map(item => {
                    const convertedItem = { ...item };

                    // Convert starttime
                    const startTimeSeconds = convertedItem.start_time;
                    const startTime = new Date(startTimeSeconds * 1000);
                    convertedItem.start_time = startTime.toISOString().substr(11, 8);

                    // Convert endtime
                    const endTimeSeconds = convertedItem.end_time;
                    const endTime = new Date(endTimeSeconds * 1000);
                    convertedItem.end_time = endTime.toISOString().substr(11, 8);

                    return convertedItem;
                }); 
                console.log('更新数据')
            })
        },
        //点击按钮切换页面
        handleCurrentChange(currentPage) {
            this.currentPage = currentPage; //每次点击分页按钮，当前页发生变化
        },
        handleClose(done) {
            done();
        },
        submitForm() {
            axios.post('http://127.0.0.1:5000/page1/', this.singleFacility).then((response) => {
                const result = response.data;
                if (result.status == 'success') {
                    this.add_dialog_visible = false
                    // this.$refs.ruleFormRole.resetFields();
                    // this.singleFacility = {}
                    this.getFacilityTime()
                    this.open1()

                }
                else {
                    this.showAlert = true
                    console.log('提交失败');
                }
            })
        },
        resetForm() {
            this.showAlert = false
            this.singleFacility2 = Object.assign({}, this.singleFacility)
            this.$refs.ruleFormRole.resetFields();
            this.$refs.editFormRef.resetFields()
            console.log('重置成功');
        },
        async handleSearch(info) {
            try {
                const res = await axios.put('http://127.0.0.1:5000/page1/', info)
                return res.data.time_id
            } catch (error) {
                console.error(error)
            }
        },
        async handleDelete(index, scope) {
            try {
                await MessageBox.confirm('确认删除该条数据？', {
                    confirmButtonText: 'Yes',
                    cancelButtonText: 'No',
                    type: 'warning'
                })
                scope['facility_id'] = this.singleFacility.facilityID
                const time_id = await this.handleSearch(scope)
                await axios.delete(`http://127.0.0.1:5000/page1/${time_id}`)

                this.getFacilityTime()
                this.open1()

            } catch (error) {
                console.error(error)
            }
        },
        async handleEdit(index, scope) {
            scope['facility_id'] = this.singleFacility.facilityID
            this.tmp = await this.handleSearch(scope)
            this.singleFacility2['date'] = new Date(`${scope['date']}`)

            this.singleFacility2['start_time'] = new Date(`${scope['date']}T${scope['start_time']}`)
            this.singleFacility2['end_time'] = new Date(`${scope['date']}T${scope['end_time']}`)
            this.singleFacility2['facility_id'] = this.singleFacility['facilityID']
            this.singleFacility = Object.assign({}, this.singleFacility2)
            this.edit_dialog_visible = true
        },
        async submitEditForm() {
            axios.put(`http://127.0.0.1:5000/page1/${this.tmp}`, this.singleFacility2).then((res) => {
                this.$refs.editFormRef.resetFields()
                // this.singleFacility = {}

                this.edit_dialog_visible = false
                this.getFacilityTime()
                this.open1()

            })
        },
        open1() {
        this.$notify({
          title: '成功',
          message: '操作成功！！',
          type: 'success'
        });
      },

    }
}
</script>