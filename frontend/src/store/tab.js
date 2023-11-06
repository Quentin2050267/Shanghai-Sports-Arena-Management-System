export default {
    state: {
        isCollapse: false // 控制菜单展开还是收起
    },
    mutations: {
        // 修改菜单展开收起的方式
        collapseMenu(state){
            state.isCollapse = !state.isCollapse
        }
    }
}