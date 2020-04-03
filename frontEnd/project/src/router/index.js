import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('@/components/login/login'),
      meta:{
        title:'登陆'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/components/login/login'),
      meta:{
        title:'登陆'
      }
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/components/home/home'),
      children:[
        {
          path:'billList',
          name:'billList',
          component:()=>import('@/components/billList/billList'),
          meta: {
            title: '账单列表',
            titleRoute:['账单管理/','账单列表']
          }
        },
        {
          path:'billDetail',
          name:'billDetail',
          component:()=>import('@/components/billList/billDetail'),
          meta: {
            title: '账单详情',
            titleRoute:['账单管理/','账单列表/','账单详情']
          }
        },
        {
          path:'accountManagement',
          name:'accountManagement',
          component:()=>import('@/components/accountManagement/accountManagement'),
          meta: {
            title: '账号管理',
            titleRoute:['系统管理/','账号管理']
          }
        },
        {
          path:'newAccount',
          name:'newAccount',
          component:()=>import('@/components/accountManagement/newAccount'),
          meta: {
            title: '新建账号/编辑',
            titleRoute:['系统管理/','账号管理/','账号编辑']
          }
        },
        {
          path:'Jurisdiction',
          name:'Jurisdiction',
          component:()=>import('@/components/accountManagement/Jurisdiction'),
          meta: {
            title: '权限',
            titleRoute:['系统管理/','账号管理/','权限']
          }
        }
      ]
    }
  ]
})
