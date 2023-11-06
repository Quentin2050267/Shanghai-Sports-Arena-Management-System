<template>
    <el-row>
        <el-col :span="24" style="padding-right: 10px;">
            <el-card class="box-card">
                <div class="user">
                    <img src="../../assets/images/admin/profile.png" alt="" @click="person()">
                    <div class="userinfo">
                        <p class="name">{{ loginname }}</p>
                        <p class="access" v-if="user_type == 'admin'">管理员</p>
                        <p class="access" v-if="user_type == 'user'">普通用户</p>
                    </div>
                </div>
                <div class="login-info">
                    <p>上次登录时间: <span>{{ year }}-{{ month }}-{{ day }}</span></p>
                </div>
            </el-card>

            <el-card style="margin-top: 20px;height: 370px;">
                <el-table :data="reservation" style="width: 100% margin: 20px auto; overflow: auto;" height="370px" stripe>
                    <el-table-column label="用户ID" prop="user_id" />
                    <el-table-column label="场馆" prop="gym_name" />
                    <el-table-column label="设施" prop="facility_name" />
                    <el-table-column label="预约日期" prop="schedule_date" sortable />
                    <el-table-column label="预约时间段" prop="schedule_time" />
                    <el-table-column label="预约提交日期" prop="reservation_date" />
                    <el-table-column label="操作" width="200px">
                        <template slot-scope="scope">
                            <div v-if="scope.row.status == 1">
                                <el-button size="mini" type="success" @click="Pass(scope.$index, scope.row)">通过</el-button>
                                <el-button size="mini" type="danger" @click="Reject(scope.$index, scope.row)">拒绝</el-button>
                            </div>
                            <div v-else-if="scope.row.status == 4">
                                <el-button size="mini" @click="reverseReject(scope.$index, scope.row)">取消拒绝</el-button>
                            </div>
                            <div v-else-if="scope.row.status == 3">
                                <el-button size="mini">已结束活动</el-button>
                            </div>
                            <div v-else>
                                <el-button size="mini" @click="reversePass(scope.$index, scope.row)">取消通过</el-button>
                                <el-button size="mini" @click="finish(scope.$index, scope.row)">活动结束</el-button>
                            </div>
                        </template>
                    </el-table-column>

                </el-table>
            </el-card>

        </el-col>
    </el-row>
</template>
<script>

import axios from 'axios';


export default {
    data() {
        return {
            reservation: [],
            loginname: "",
            user_id: '',
            user_type: "",
            year: "",
            month: "",
            day: "",
        }
    },
    mounted() {
        this.loginname = this.cookie.getCookie('username')
        this.user_type = this.cookie.getCookie('user_type')
        this.user_id = this.cookie.getCookie('id')
        this.year = this.cookie.getCookie('year')
        this.month = this.cookie.getCookie('month')
        this.day = this.cookie.getCookie('day')
        this.getReservation()
    },
    methods: {
        person() {
            this.$router.replace('/page2')
        },
        getReservation() {
            axios.get(`http://127.0.0.1:5000/reservation/`).then(res => {
                this.reservation.splice(0, this.reservation.length)
                this.reservation.push(...res.data.results)

                const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
                this.reservation.forEach(item => {
                    let a = new Date(item.schedule_date);
                    item.schedule_date = a.toLocaleDateString('zh-CN', options).replace(/\//g, '-')
                    let b = new Date(item.reservation_date);
                    item.reservation_date = b.toLocaleDateString('zh-CN', options).replace(/\//g, '-')
                });
                console.log('更新数据')
            })
        },
        Pass(index, row) {
            this.reservation[index].status = 2
            this.editStatus(index, row.reservation_id)
        },
        Reject(index, row) {
            this.reservation[index].status = 4
            this.editStatus(index, row.reservation_id)
        },
        reversePass(index, row) {
            this.reservation[index].status = 1
            this.editStatus(index, row.reservation_id)

        },
        reverseReject(index, row) {
            this.reservation[index].status = 1
            this.editStatus(index, row.reservation_id)
        },
        finish(index, row) {
            this.reservation[index].status = 3
            this.editStatus(index, row.reservation_id)
        },
        editStatus(index, id) {
            axios.put(`http://127.0.0.1:5000/reservation/${id}`, this.reservation[index]).then((res) => {
                this.getReservation()
            })
        }
    }
}
</script>
<style lang="less" scoped>
.user {
    padding-bottom: 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid #ccc;
    display: flex;
    align-items: center;

    img {
        margin-right: 40px;
        width: 150px;
        height: 150px;
        border-radius: 50%;
    }

    .userinfo {
        .name {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .access {
            color: #999999;
        }
    }
}

.login-info {
    p {
        line-height: 28px;
        font-size: 14px;
        color: #999999;

        span {
            color: #666666;
            margin-left: 60px;
        }
    }
}

.num {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;

    .icon {
        width: 80px;
        height: 80px;
        font-size: 30px;
        text-align: center;
        line-height: 80px;
        color: #fff;
    }

    .detail {
        margin-left: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;

        .price {
            font-size: 30px;
            margin-bottom: 10px;
            line-height: 30px;
            height: 30px;
        }

        .desc {
            font-size: 14px;
            text-align: center;
            color: #999999;
        }
    }

    .el-card {
        width: 32%;
        margin-bottom: 20px;
    }
}

.graph {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;

    .el-card {
        height: 220px;
        width: 48%;
    }
}
</style>