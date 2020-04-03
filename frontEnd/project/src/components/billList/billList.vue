<template>
    <div class="box">
      <div class="top">
        <div class="item">
          <div class="inp"><span>供应商:</span><input type="text" placeholder="请输入内容" v-model="supplier"></div>
          <div class="block">
            <span class="demonstration">对账时间:</span>
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
          <div class="inp"><span>对账单号:</span><input type="text" placeholder="请输入内容" v-model="orderNum"></div>
          <div class="inp"><span>签约主体:</span><input type="text" placeholder="请输入内容" v-model="subject"></div>
          <div> <el-button type="primary" @click="search">查询</el-button>
            <el-button type="info" @click="reset">重置</el-button></div>
        </div>
      </div>
      <div class="export"><el-button type="primary">导出</el-button></div>
      <div class="con">
        <div class="conItem">
          <div class="check"><el-checkbox v-model="checked"></el-checkbox></div>
          <div class="supplier">供应商</div>
          <div class="time">对账时间</div>
          <div class="orderNum">对账单号</div>
          <div class="subject">签约主体</div>
          <div class="money">对账总金额</div>
          <div class="set">操作</div>
        </div>
        <div class="conItem" v-for="v in 10">
          <div class="check"><el-checkbox v-model="checked"></el-checkbox></div>
          <div class="supplier">三志物流公司</div>
          <div class="time">2018-08-08 08:50:20</div>
          <div class="orderNum">1234567894561234</div>
          <div class="subject">泉州一卡供应链管理有限公司</div>
          <div class="money">9999999.00</div>
          <div class="set" @click="route('/home/billDetail')">查看明细</div>
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
            time:'',//签约时间
            subject:'',//签约主体
            supplier:'',//供应商
            orderNum:'',//对账单号
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
          this.time=this.subject=this.supplier=this.orderNum=''
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
  .set{
    width: 10%;
  }
  .set:hover{
    cursor: pointer;
  }
.conItem:nth-child(n+2)>.set{
  color: #406fff;
}
.supplier,.money,.time,.orderNum,.subject{
    width: 19%;
  white-space:nowrap;
  text-overflow:ellipsis;
  overflow: hidden;
  }
  .page{
    text-align: center;
  }
</style>
