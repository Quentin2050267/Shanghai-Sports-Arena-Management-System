import http from '../utils/request'

// 请求首页数据
export const getData = () => {
    // 可能需要改
    return http.get('/home/getData')
}