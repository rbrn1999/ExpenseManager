var filter_details=[];
Vue.component('u-item', {
  props:['u_item'],
  template: '<div v-on:click="add_add_detail()" class="u-item">{{u_item.name}} <input type="button" v-on:click="delete_add_detail()" value="x"></div>',
  methods:{
    add_add_detail:function(){
       this.$emit('add_add_detail')
    },
    delete_add_detail:function(){
      this.$emit('delete_add_detail')
    }
  }
})


const Type = {
  Income: '收入',
  Expense: '支出'
};

class Record {
  constructor(name, type, amount, date) {
    this.name = name;
    this.type = type;
    this.amount = amount;
    this.date = date;
  }
};

class Income extends Record{
  
};

class Expense extends Record{
  
};

class UsualItem {
  constructor(name, itemType) {
    self.name = name;
    self.itemType = itemType;
  }
}


var app = new Vue({ 
  el: '#app',
  data: {
    usually_item:[
      {name: '工作', itemType: Type.Income},
      {name: '吃飯', itemType: Type.Expense}
      // new UsualItem('工作', Type.Income),
      // new UsualItem('吃飯', Type.Expense),
      // new UsualItem('買生活用品', Type.Expense)
    ],
    details: [
    ],
    total_spend:[],
    total_income:[],
    ts:0,
    ti:0,
    add_detail:{name: '',type:'收入',amount:'',date:''},
    filter_date:{start:'',end:''},
    recent_day:7,
    total:0
  },
  created:function(){
    this.set_filter_date();
  },
  methods: {
    add_uitem:function(){
      this.usually_item.push({
        name:this.add_detail.name,
        itemType:this.add_detail.type
      })
    },
    delete_uitem:function(index){
      this.usually_item.splice(index, 1)
    },
    add: function () {
      if(this.add_detail.name == ''){
        alert('項目名稱不可為空')
      }
      else if(this.add_detail.amount == ''){
        alert('金額不可為空')
      }
      else if(this.add_detail.date == ''){
        alert('日期不可為空')
      }
      else{
        this.details.push({
          name:this.add_detail.name,
          type:this.add_detail.type,
          amount:this.add_detail.amount,
          date:this.add_detail.date
        })
        this.compute_total_detail();
      }
    },
    set_add_detail:function(detail_name){
      this.add_detail.name = detail_name;
      this.add_detail.amount = "";
    },
    delete_detail:function(index){
      this.details.splice(index, 1)
      this.compute_total_detail();
    },
    isNumber: function(evt) {//只能輸入數字
      evt = (evt) ? evt : window.event;
      var charCode = (evt.which) ? evt.which : evt.keyCode;
      if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
        evt.preventDefault();
      } else {
        return true;
      }
    },
    check_date:function(start_date,item_date,to_date){
      if(start_date==="" || to_date==="")return true;
      var sd = new Date(start_date).getTime();
      var id = new Date(item_date).getTime();
      var td = new Date(to_date).getTime();
      if(sd <= id && td>=id)
        return true;
    },
    set_filter_date:function(){
      var today = new Date();
      var day = new Date();
      day.setDate(day.getDate() - this.recent_day);
      
      var today_formate = this.date_formate(today);
      var day_formate = this.date_formate(day);
      
      this.filter_date.start = day_formate;
      this.filter_date.end = today_formate;
      
      this.compute_total_detail();
      
    },
    date_formate:function(date){
      dd = date.getDate();
      mm = date.getMonth() + 1;
      y = date.getFullYear();
      return y + '/' + mm + '/'+ dd;
    },
    clear_date:function(){
      this.filter_date.start="";
      this.filter_date.end="";
      from.datepicker();
      to.datepicker();
    },
    add_spend_array:function(detail){
      var name = detail.name;
      var check = true;
      for(var j in this.total_spend){
        if(this.total_spend[j].name == name){
          check = false;
          var amount = detail.amount;
          this.total_spend[j].amount += amount;
        }
      }
      if(check)this.total_spend.push({name:name,type:"支出",amount:detail.amount})
    },
    add_income_array:function(detail){
      var name = detail.name;
      var check = true;
      for(var j in this.total_income){
        if(this.total_income[j].name == name){
          check = false;
          var amount = detail.amount;
          this.total_income[j].amount += amount;
        }
      }
      if(check)this.total_income.push({name:name,type:"收入",amount:detail.amount})
    },
    compute_total_detail:function(){
      this.total_income=[];
      this.total_spend=[];
      this.ts=0;
      this.ti=0;
      this.total=0;
      var name="";
      var check=true;
      for(var i in this.details){
        if(this.check_date(this.filter_date.start,this.details[i].date,this.filter_date.end)){
          if(this.details[i].type=="收入"){
            this.total += parseInt(this.details[i].amount)
            this.ti += parseInt(this.details[i].amount)
            this.add_income_array(this.details[i]);
          }else{
            this.add_spend_array(this.details[i]);
            this.total -= parseInt(this.details[i].amount)
            this.ts += parseInt(this.details[i].amount)
          }
        }
      }
      
      //計算百分比
      var percent=0;
      for(i in this.total_spend){
        percent = ((this.total_spend[i].amount / this.ts) * 100).toFixed(2)
        this.total_spend[i].percent = percent;
      }
      for(i in this.total_income){
        percent = ((this.total_income[i].amount / this.ti)* 100).toFixed(2)
        this.total_income[i].percent = percent;
      }
    }
  }
})

$( function() {
  $( "#datepicker" ).datepicker({ dateFormat: 'yy/mm/dd' });
    var dateFormat = "yy/mm/dd",
      from = $( "#from" )
        .datepicker({
          defaultDate: "+1w",
          changeMonth: true,
          numberOfMonths: 1,
          dateFormat: dateFormat
        })
        .on( "change", function() {
          to.datepicker( "option", "minDate", getDate( this ) );
        }),
      to = $( "#to" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        dateFormat: dateFormat
      })
      .on( "change", function() {
        from.datepicker( "option", "maxDate", getDate( this ) );
      });
 
    function getDate( element ) {
      var date;
      try {
        date = $.datepicker.parseDate( dateFormat, element.value );
      } catch( error ) {
        date = null;
      }
 
      return date;
    }
  } );

$(document).ready(function () {
        $("#from").datepicker().on("change", function (e) {
            app.$data.filter_date.start = $(this).val();
            app.compute_total_detail();
        });
        $("#to").datepicker().on("change", function (e) {
            app.$data.filter_date.end = $(this).val();
            app.compute_total_detail();
        });
        $("#datepicker").datepicker().on("change", function (e) {
            app.$data.add_detail.date = $(this).val();
        });
    });