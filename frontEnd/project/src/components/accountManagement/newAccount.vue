<template>
    <div>
      <div class="item"><span>账号:</span><input type="text" v-model="user"></div>
      <div class="item"><span>姓名:</span><input type="text" v-model="name"></div>
      <div class="item"><span>密码:</span><input type="password" v-model="pwd"></div>
      <div class="item"><span>手机号码:</span><input type="text" v-model="phone"></div>
      <div class="item"><span>备注:</span><textarea v-model="remarks"></textarea></div>
      <div class="bts">
        <span class="gayr" @click="cancel">取消</span>
        <span class="blue" @click="submenu">提交</span>
      </div>
    </div>
</template>

<script>
    export default {
        data(){
          return {
            pwd:'',//密码
            phone:'',//电话
            user:'',//账号
            name:'',//姓名
            remarks:''//备注
          }
        },
      methods:{
        submenu(){//提交

        },
        cancel(){//取消
          this.pwd=this.phone=this.user=thia.name=this.remarks=''
        }
      }
    }
</script>

<style scoped>
.item{
  margin-top: 50px;
  margin-left: 50px;
  display: flex;
  align-items: center;
}
  .item>span{
    width: 100px;
  }
  .item>input{
    border: 1px solid rgba(217,217,217,1);
    height: 26px;
    padding: 2px;
    width: 300px;
    border-radius: 5px;
    outline: none;
  }
  .item>textarea{
    width: 400px;
    height: 80px;
    border-radius: 5px;
    padding: 5px;
    outline: none;
    resize: none;
  }
  .item+.item{
    margin-top: 30px;
  }
  .bts{
    margin-top: 50px;
    margin-left: 150px;
  }
  .bts>span{
    border-radius: 5px;
    color: #fff;
    padding: 10px 80px;
  }
.bts>span+span{
  margin-left: 20px;
}
  .blue{
    background: rgba(24,144,255,1);
  }
  .gayr{
    background: rgba(204,204,204,1);
  }
</style>
