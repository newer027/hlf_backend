<template>
    <div class="box">
      <div class="top">
        <p class="title">基本信息</p>
        <div class="item"><p><span>供应商:</span><span>三志物流</span></p><p><span>签约主体:</span><span>手机客户端手机卡河山大好</span></p></div>
        <div class="item"><p><span>对账单号:</span><span>三志物流</span></p><p><span>对账总金额:</span><span>手机客户端手机卡河山大好</span></p></div>
        <div class="item"><p><span>对账时间:</span><span>三志物流</span></p></div>
        <div class="border"></div>
      </div>
      <div class="detailed"> <span>单据明细</span><el-button type="primary" class="bt">导出</el-button></div>
      <div class="con">
        <div class="conItem">
          <div class="orderNum">单据单号</div>
          <div class="time">创建时间</div>
          <div class="orderType">单据类别</div>
          <div class="routeName">路线名称</div>
          <div class="carNum">车牌号</div>
          <div class="money">应付金额</div>
          <div class="set">上链ID</div>
        </div>
        <div class="conItem" v-for="v in 10">
          <div class="orderNum">12345678945612345</div>
          <div class="time">2018-08-08 08:50:20</div>
          <div class="orderType">干线任务</div>
          <div class="routeName">上海-南昌</div>
          <div class="carNum">赣A12345</div>
          <div class="money">9999999.00</div>
          <div class="set">1234651374651567454654664655645</div>
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
      data (){
        return {

        }
      },
      methods:{
        handleCurrentChange(val){//分页
          console.log(val)
        }
      }
    }
</script>

<style scoped>
  .top{
    margin: 0 20px;
    border-bottom: 1px solid #ddd;
  }
  .title{
    font-weight: 600;
    margin-left: 20px;
    font-size: 18px;
  }
  .item{
    margin: 20px;
    display: flex;
  }
  .item>p{
    width: 40%;
    display: flex;
  }
  .item>p>span:nth-child(1){
    width: 20%;
  }
  .detailed{
    margin: 20px;
    overflow: hidden;
  }
  .detailed>.bt{
    float: right;
  }
  .detailed>span{
    float: left;
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
  .conItem:nth-child(n+2)>.set{
    color: #406fff;
  }
  .set,.carNum,.money,.time,.orderNum,.orderType,.routeName{
    width: 18%;
    white-space:nowrap;
    text-overflow:ellipsis;
    overflow: hidden;
  }
  .page{
    text-align: center;
  }
</style>
