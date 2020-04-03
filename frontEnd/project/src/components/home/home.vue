<template>
    <div style="height: 100vh">
      <div class="top">
        <div class="left">
          <img src="../../assets/LOGO1.png" alt=""><span>天地汇区块链金融平台</span>
        </div>
        <div class="right">
          <img src="../../assets/user.png" alt=""><span>tiandihui</span>
        </div>
      </div>
      <div class="buttom">
        <div class="leftBox">
          <el-col class="tac">
            <el-menu
              :default-active=index
              class="el-menu-vertical-demo"
              background-color="#545c64"
              text-color="#fff"
              active-text-color="#ffd04b">
              <el-submenu index="1" >
                <template slot="title">
                  <i class="el-icon-document"></i>
                  <span>账单管理</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="1-1" @click="route('/home/billList','1-1')">账单列表</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="2">
                <template slot="title">
                  <i class="el-icon-setting"></i>
                  <span>系统管理</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="2-1" @click="route('/home/accountManagement','2-1')">账号管理</el-menu-item>
                  <!--<el-menu-item index="2-2" @click="route('/home/billList')">角色管理</el-menu-item>-->
                </el-menu-item-group>
              </el-submenu>
            </el-menu>
          </el-col>
        </div>
        <div class="rightBox">
          <div class="title">
            <p class="router"><span :class="k==arr.length-1?'black':'gary'" v-for="(i,k) in arr">{{i}}</span></p>
            <p class="position">{{arr[arr.length-1]}}</p>
          </div>
          <div class="con">
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
    export default {
      data(){
        return{
          index:'1-1',
          arr:[]
        }
      },
      mounted(){
        if(sessionStorage.getItem('index')){
          this.index=sessionStorage.getItem('index')
          this.arr=this.$route.meta.titleRoute
        }
      },
        methods:{
          route(data,index){
            this.$router.push({ path: data});
            this.index=index
            sessionStorage.setItem('index',index)
          },
        },
      watch:{
        $route(to,from){
          this.arr=to.meta.titleRoute
        }
      }
    }
</script>

<style scoped>
  .tac{
    width: 300px;
  }
  .el-menu{
    border: none;
  }
  .top{
    height: 60px;
    overflow: hidden;
    border-bottom: 1px solid #545c64;
    background: rgba(204,204,204,0.1);
  }
  .top>.left{
    width: 300px;
    height: 100%;
    background: #545c64;
    float: left;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .left>img{
    width: 80px;
    height: 30px;
  }
  .left>span{
    color: #fff;
    font-size: 16px;
    margin-left: 10px;
  }
  .right{
    float: right;
    color: #333;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;
  }
  .buttom{
    height: calc(100% - 61px);
    overflow: hidden;
  }
  .leftBox {
    float: left;
    width: 300px;
    height: 100%;
    background-color:#545c64;
    overflow-x: hidden;
    overflow-y: auto;
    opacity: 0.8;
  }
  .rightBox{
    float: right;
    width: calc(100vw - 300px);
    height: 100%;
    background: rgba(204,204,204,0.1);
  }
  .title{
    height: 80px;
    overflow: hidden;
    background: #fff;
  }
  .title>p{
    margin-top: 12px;
    padding-left: 20px;
  }
  .position{
    font-weight: bolder;
    font-size: 20px;
  }
  .gary{
    color: #777;
  }
  .black{
    color: #333;
  }
  .con{
    width: calc(98% - 40px);
    height: calc(100% - 140px);
    background: #fff;
    margin: 10px 1%;
    padding: 20px;
    border-radius: 5px;
    min-width: 1000px;
    overflow-y: scroll;
  }
</style>
