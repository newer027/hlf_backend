<template>
  <div class="wrap">
    <img class="loge" src="../../assets/LOGO.png">
    <div class="box">
      <p class="title">区块链金融管理后台</p>
      <p class="titleEnglish">TDH-Chain Management Systerm</p>
      <div class="inp"> <span class="user"></span><input type="text" placeholder="请输入用户名" v-model="user"></div>
      <div class="inp"> <span class="pwd"></span><input type="password" placeholder="请输入密码" v-model="pwd"></div>
      <div class="bt" @click="login()">登录</div>
    </div>
  </div>
</template>

<script>
    export default {
      data(){
        return {
          user:'',
          pwd:''
        }
      },
      methods:{
        login(){
          this.$router.push({ path: "/home/billList" });
        }
      }
    }
</script>

<style scoped>
.wrap{
  width: 100vw;
  height: 100vh;
  background: #eee;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.loge{
  margin-bottom: 30px;
  height: 60px;
}
  .box{
    width: 500px;
    height: 400px;
    background: #fff;
    text-align: center;
    border-radius: 10px;
    color: #666;
  }
  .title{
    margin-top: 30px;
    font-size: 30px;
    padding: 20px;
  }
  .titleEnglish{
    font-size: 24px;
  }
  .inp{
    height: 32px;
    display: flex;
    width: 300px;
    margin-left: 100px;
    padding: 5px;
    border: 1px solid #b8bebe;
    border-radius: 5px;
    margin-top: 30px;
  }
  .inp>span{
    width: 32px;
    height: 32px;
    margin-right: 20px;
  }
  .user{
    background-image: url("../../assets/user.png");
  }
  .pwd{
    background-image: url("../../assets/pwd.png");
  }
  .inp>input{
    outline: none;
  }
input::-webkit-input-placeholder{
  color: #999;
}
  .bt{
    color: #fff;
    background: #406fff;
    width: 300px;
    height: 50px;
    border-radius: 10px;
    font-size: 24px;
    line-height: 50px;
    text-align: center;
    margin: 30px 0 0 100px;
  }
  .bt:hover{
    cursor:pointer;
  }
</style>
