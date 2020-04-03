<template>
    <div class="box">
      <div class="top"> <span>账号:</span><input type="text" placeholder="请输入账号" v-model="user"></div>
      <div class="bottom">
        <div>
          <el-transfer
            style="text-align: left; display: inline-block"
            v-model="selected"
            filterable
            :titles="['待选列表', '已添加']"
            :button-texts="['删除', '添加']"
            @change="handleChange"
            :data="data">
            <span slot-scope="{ option }">{{ option.label }}</span>
            <!--<el-button class="transfer-footer" slot="left-footer" size="small">上一页</el-button>-->
            <!--<el-button class="transfer-footer" slot="left-footer" size="small">下一页</el-button>-->
            <!--<el-button class="transfer-footer" slot="right-footer" size="small">上一页</el-button>-->
            <!--<el-button class="transfer-footer" slot="right-footer" size="small">下一页</el-button>-->
          </el-transfer>
        </div>
      </div>
      <div class="bts"><span class="gayr" @click="cancel">取消</span>
        <span class="blue" @click="submit">提交</span></div>
    </div>
</template>

<script>
    export default {
      data() {
        const generateData = _ => {
          const data = [];
          for (let i = 1; i <= 20; i++) {
            data.push({
              key: i,
              label: `备选项 ${ i }`,
            });
          }
          data.push({key:201,label:'zhangsan'})
          return data;
        };
        return {
          data: generateData(),
          selected: [],
          user:''
        };
      },

      methods:{
          handleChange(value, direction, movedKeys) {
            console.log(value,123, direction, movedKeys);
          },
        cancel(){
            this.selected=[]
            this.user=''
        },
        submit(){

        }
        }
    }
</script>

<style scoped>
  .box{
    margin: 50px 0px 0px 100px;
  }
  .top>input {
    padding: 5px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    outline: 0;
    height: 30px;
    line-height: 40px;
    width: 300px;
    margin-left: 30px;
  }
  .bottom{
    margin-top: 60px;
  }
  .bts{
    margin-top: 100px;
    margin-left: 50px;
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
