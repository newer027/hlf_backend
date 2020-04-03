<template>
  <div class="box">
    <div class="top">
      <div class="item">
        <div class="inp"><span>账号:</span><input type="text" placeholder="请输入内容" v-model="userName"></div>
        <div class="block">
          <span class="demonstration">创建时间:</span>
          <el-date-picker
            v-model="time"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </div>
      </div>
      <div class="item">
        <div class="inp"><span>姓名:</span><input type="text" placeholder="请输入内容" v-model="name"></div>
        <div class="inp"><span>手机号码:</span><input type="text" placeholder="请输入内容" v-model="phone"></div>
        <div> <el-button type="primary" @click="search">查询</el-button>
          <el-button type="info" @click="reset">重置</el-button></div>
      </div>
    </div>
    <div class="export"><el-button type="primary" @click="route('/home/newAccount')">+ 创建账号</el-button></div>
    <div class="con">
      <div class="conItem">
        <div class="check"><el-checkbox v-model="checked"></el-checkbox></div>
        <div class="user">登录账号</div>
        <div class="time">创建时间</div>
        <div class="phone">手机号码</div>
        <div class="name">姓名</div>
        <div class="remarks">备注</div>
        <div class="set">操作</div>
      </div>
      <div class="conItem" v-for="v in 10">
        <div class="check"><el-checkbox v-model="checked"></el-checkbox></div>
        <div class="user">panquan</div>
        <div class="time">2018-08-08 08:50:20</div>
        <div class="phone">18296270000</div>
        <div class="name">孙悟空</div>
        <div class="remarks">齐天大圣</div>
        <div class="set"><span @click="route('/home/Jurisdiction')">权限设置</span><span @click="route('/home/newAccount')">编辑</span><span>删除</span></div>
      </div>
    </div>
    <div class="block page">
      <el-pagination
        @current-change="handleCurrentChange"
        :page-sizes="[10]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="600">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  export default {
    data(){
      return {
        time:'',//创建时间
        userName:'',//账号
        name:'',//姓名
        phone:'',//电话
        checked:false
      }
    },
    methods:{
      handleCurrentChange(val){//分页
        console.log(val)
      },
      route(data){
        this.$router.push({ path: data });
      },
      //条件查询
      search(){
        console.log(this.time)
      },
      reset(){
        this.time=this.userName=this.name=this.phone=''
      }
    }
  }
</script>

<style scoped>
  .item{
    display: flex;
    align-items: center;
  }
  .inp{
    display: flex;
    align-items: center;
  }
  .inp>input{
    border:1px solid #dcdfe6;
    border-radius: 4px;
    outline: 0;
    height: 40px;
    line-height: 40px;
    width: 75%;
  }
  .item>div{
    display: flex;
    align-items: center;
    width: 30%;
  }
  .item>div>span{
    width: 20%;
  }
  .demonstration{
    display: block;
  }
  .item+.item{
    margin-top: 10px;
  }
  .export{
    margin: 20px;
  }
  .con{
    height: 500px;
    overflow: hidden;
  }
  .conItem{
    display: flex;
    padding: 10px;
    border-bottom: 1px solid rgba(232,232,232,1);
  }
  .conItem:nth-child(1){
    background: #ddd;
    border-top: 1px solid rgba(232,232,232,1);
  }
  .conItem:nth-child(n+2){
    color: #999;
  }
  .check{
    width: 3%;
  }
  .phone,.name{
    width: 10%;
  }
  .conItem:nth-child(n+2)>.set{
    color: #406fff;
  }
  .conItem:nth-child(n+2)>.set>span:hover{
    cursor:pointer;
  }
  .conItem:nth-child(n+2)>.set>span+span{
    margin-left: 16px;
  }
  .user,.time,.remarks{
    width: 19%;
    white-space:nowrap;
    text-overflow:ellipsis;
    overflow: hidden;
  }
  .page{
    text-align: center;
  }
</style>
