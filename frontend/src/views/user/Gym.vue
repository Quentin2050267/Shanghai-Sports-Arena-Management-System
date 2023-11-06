<template>
    <div class='gym' style="margin: 0 auto">
        <h1>体育馆预约</h1>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <!-- 搜索 -->
            <el-input placeholder="请输入体育馆名称" v-model="gym.gym_name" class="input-with-select"
                style="width: 20%; padding-right: 45px;">
                <el-button slot="append" icon="el-icon-search" @click="handleSearch()"></el-button>
            </el-input>
        </div>
        <el-table :data="gyms.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
            style="width: 100% margin: 20px auto; overflow: auto;" height="500" stripe
            :default-sort="{ prop: 'gym_district', order: 'descending' }">

            <el-table-column label="区" prop="gym_district" sortable />

            <el-table-column label="名称" prop="gym_name" sortable />

            <el-table-column label="地址" prop="gym_address" />

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="handleReserve(scope.$index, scope.row)">预约</el-button>
                </template>
            </el-table-column>

        </el-table>
        <el-pagination background layout="prev, pager, next,jumper, ->, total, slot" :total="gyms.length"
            @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
            style="text-align: center; padding-top: 20px;">
        </el-pagination>

        <el-dialog title="预约体育设施" :visible.sync="reserve_dialog_visible" width="30%" :before-close="handleClose">
            <el-form ref="ruleFormRole" :model="reservation" status-icon label-width="120px" class="demo-ruleForm">
                <el-form-item label="设施" prop="facility">
                    <el-select v-model="reservation.facility" placeholder="请选择设施">
                        <el-option v-for="option in facilities" :key="option" :label="option" :value="option"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="预约日期">
                    <el-col :span="12">
                        <el-date-picker type="date" placeholder="请选择日期" v-model="reservation.schedule_date"
                            style="width: 100%;"></el-date-picker>
                    </el-col>
                </el-form-item>

                <el-form-item label="预约时间">

                    <el-select v-model="reservation.schedule_time" :no-match-text="'无可预约日期'" placeholder="请选择时间段"
                        @visible-change="chooseTimeSpan">
                        <el-option v-for="option in timeSpan" :key="option" :label="option" :value="option"></el-option>
                    </el-select>

                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm()">提交</el-button>
                </el-form-item>
            </el-form>
            <el-alert v-if="showAlert" title="已预约！" type="warning" show-icon @close="showAlert = false">
            </el-alert>
            <el-alert v-if="showAlert_" title="该天无开放时间段！" type="warning" show-icon @close="showAlert = false">
            </el-alert>
        </el-dialog>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            currentPage: 1,
            pageSize: 20,
            gyms: [],
            gym: {
                gym_name: "",
                gym_id: "",
            },
            reservation: {
                user_id: "",
                gym_id: "",
                facility: "",
                reservation_date: "",
                schedule_date: "",
                // 开放时间段起始时间
                schedule_time: ""
            },
            facilities: [],
            showAlert: false,
            showAlert_: false,
            reserve_dialog_visible: false,
            timeSpan: [],
            year: "",
            month: "",
            day: ""
        };
    },
    methods: {
        //点击按钮切换页面
        handleCurrentChange(currentPage) {
            this.currentPage = currentPage; //每次点击分页按钮，当前页发生变化
        },
        handleClose(done) {
            done();
        },
        getGyms() {
            axios.get('http://127.0.0.1:5000/gym/',).then(res => {
                this.gyms.splice(0, this.gyms.length)
                this.gyms.push(...res.data.results)
                console.log('更新数据')
            })
        },
        handleSearch() {
            console.log(this.gym)
            axios.put('http://127.0.0.1:5000/gym/0', this.gym).then(res => {
                this.gyms.splice(0, this.gyms.length)
                this.gyms.push(...res.data.results)
            })
        },
        handleReserve(index, scope) {
            // console.log(scope);
            this.facilities = scope.facility
            this.gym.gym_id = scope.gym_id
            this.reservation.gym_id = scope.gym_id
            this.reserve_dialog_visible = true
        },
        submitForm() {
            if (this.reservation.schedule_time.length == 0) {
                this.showAlert_ = true
                console.log('提交失败');
                return
            }
            this.year = this.cookie.getCookie('year')
            this.month = this.cookie.getCookie('month')
            this.day = this.cookie.getCookie('day')
            this.reservation.reservation_date = `${this.year}-${this.month}-${this.day}`
            this.reservation.user_id = this.cookie.getCookie('id')
            console.log(this.reservation);


            axios.post('http://127.0.0.1:5000/gym/', this.reservation).then((response) => {
                const result = response.data;
                if (result.status == 'success') {
                    this.reserve_dialog_visible = false
                    this.$refs.ruleFormRole.resetFields();
                    this.getGyms()
                    this.open1()
                }
                else {
                    this.showAlert = true
                    console.log('提交失败');
                }
            })
        },
        chooseTimeSpan(visible) {
            if (visible) {
                let myDate;
                // 获取this.facility.gym_id中名为this.reservation.facility的facility_id
                axios.get(`http://127.0.0.1:5000/page1/${this.gym.gym_id}/${this.reservation.facility}`,).then(res => {
                    myDate = res.data.results
                    console.log(myDate)
                    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
                    this.reservation.schedule_date = this.reservation.schedule_date.toLocaleDateString('zh-CN', options).replace(/\//g, '-')
                    // 再查询facility_id中this.reservation.schedule_date这一天的开放时间段
                    let matchingObjects = [];

                    // 使用 for 循环遍历 myDate 数组
                    for (let i = 0; i < myDate.length; i++) {
                        if (myDate[i].date === this.reservation.schedule_date) {
                            matchingObjects.push(myDate[i]);
                        }
                    }
                    matchingObjects = matchingObjects.map(item => {
                        const convertedItem = { ...item };

                        const startTimeSeconds = convertedItem.start_time;
                        const startTime = new Date(startTimeSeconds * 1000);
                        convertedItem.start_time = startTime.toISOString().substr(11, 8);

                        // Convert endtime
                        const endTimeSeconds = convertedItem.end_time;
                        const endTime = new Date(endTimeSeconds * 1000);
                        convertedItem.end_time = endTime.toISOString().substr(11, 8);

                        this.timeSpan.push(`${convertedItem.start_time}-${convertedItem.end_time}`)
                        return convertedItem;
                    });

                    console.log(this.timeSpan)

                })
            }
        },
        open1() {
            this.$notify({
                title: '成功',
                message: '操作成功！！',
                type: 'success'
            });
        },

    },
    mounted() {
        this.getGyms()

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