webpackJsonp([3],{746:function(e,t,n){n(776);var a=n(20)(n(758),n(788),null,null);e.exports=a.exports},748:function(e,t,n){"use strict";function a(e,t){var n,a,l=0,s=0;try{l=e.toString().split(".")[1].length}catch(e){}try{s=t.toString().split(".")[1].length}catch(e){}return n=Number(e.toString().replace(".","")),a=Number(t.toString().replace(".","")),0==a?1/0:n/a*Math.pow(10,s-l)}function l(e,t){var n=0,a=e.toString(),l=t.toString();try{n+=a.split(".")[1].length}catch(e){}try{n+=l.split(".")[1].length}catch(e){}return Number(a.replace(".",""))*Number(l.replace(".",""))/Math.pow(10,n)}function s(e,t){var n,a,l;try{n=e.toString().split(".")[1].length}catch(e){n=0}try{a=t.toString().split(".")[1].length}catch(e){a=0}return l=Math.pow(10,Math.max(n,a)),(e*l+t*l)/l}function r(e,t){var n,a,l,s;try{n=e.toString().split(".")[1].length}catch(e){n=0}try{a=t.toString().split(".")[1].length}catch(e){a=0}return l=Math.pow(10,Math.max(n,a)),s=n>=a?n:a,((t*l-e*l)/l).toFixed(s)}Object.defineProperty(t,"__esModule",{value:!0}),Number.prototype.add=function(e){return s(e,this)},Number.prototype.sub=function(e){return r(e,this)},Number.prototype.mul=function(e){return l(e,this)},Number.prototype.div=function(e){return a(this,e)},t.accDiv=a,t.accMul=l,t.accAdd=s,t.accSub=r},758:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var l=n(158),s=a(l),r=n(75),o=a(r),i=n(157),c=a(i),u=n(156),m=a(u),_=n(748);t.default={data:function(){return{loading:!1,options:[{settlement_status:1,label:"已结算"},{settlement_status:0,label:"未结算"}],filters:{settlement_status:null,datetimerange:["2021-01-01","2021-12-01"]},orders:[],pageNum:1,pageSize:100,total:0,multipleSelection:[],settlementDialog:!1,settlementData:{settlement_date:new Date,receiving_account:"",note:"",settlement_method:""}}},created:function(){var e=this;return(0,m.default)(c.default.mark(function t(){return c.default.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:e.getOrders();case 1:case"end":return t.stop()}},t,e)}))()},methods:{handleSelectionChange:function(e){this.multipleSelection=e},handleCurrentChange:function(e){this.page=e,this.getOrders()},subSettlement:function(e){var t=this;return(0,m.default)(c.default.mark(function n(){var a;return c.default.wrap(function(n){for(;;)switch(n.prev=n.next){case 0:if(!isNaN(e.actual_settlement_fee)){n.next=6;break}return t.$message.info("当前结算金额为0,请选择正确的保单进行结算"),t.loading=!1,n.abrupt("return");case 6:return"object"==(0,o.default)(e.settlement_date)&&(e.settlement_date=e.settlement_date.format("yyyy-MM-dd hh:mm:ss")),n.next=9,t.$axios.post("Settlements/sub_settlements/",e);case 9:a=n.sent,t.$message.success(a.message),t.settlementDialog=!1,t.getOrders();case 13:case"end":return n.stop()}},n,t)}))()},showSettlementDialog:function(){this.settlementData.actual_settlement_fee=0,this.settlementData.settlement_date=new Date,this.settlementData.insurance_arr=[];for(var e=this,t=0;t<this.multipleSelection.length;t++){if(1==this.multipleSelection[t].settlement_status)return e.settlementDialog=!1,e.$message.info("包含已结算保单，请重新勾选"),null;e.settlementData.insurance_arr.push(this.multipleSelection[t].id),e.settlementData.actual_settlement_fee=(0,_.accAdd)(e.settlementData.actual_settlement_fee,this.multipleSelection[t].settlementForm.actual_settlement_fee),e.settlementData.settlement_fee=e.settlementData.actual_settlement_fee}if(isNaN(e.settlementData.settlement_fee))return void this.$message.info("包含未匹配费率的保单,请重新勾选");console.log(this.multipleSelection),this.settlementDialog=!0},getOrders:function(){var e=this;return(0,m.default)(c.default.mark(function t(){var n,a,l,r;return c.default.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return e.loading=!0,t.next=3,e.$axios("InsurancePolicySettlements/",{params:{page_size:e.pageSize,nature_of_use:e.filters.nature_of_use,chanel_rate_id__chanel:e.filters.chanel_rate_id__chanel,settlement_status:e.filters.settlement_status,startTime:e.filters.datetimerange[0],endTime:e.filters.datetimerange[1]}});case 3:if(n=t.sent,a=n.data,0!=a.length&&a){t.next=9;break}return e.orders=a,e.loading=!1,t.abrupt("return");case 9:for(l=function(t){var n={};0==a[t].settlement_status&&(n.actual_settlement_fee=null,n.settlement_date=new Date,n.insurance_arr=[],n.insurance_arr.push(a[t].id),n.note="",n.settlement_method="",n.receiving_account=""),a[t].settlementForm=(0,s.default)({},n),e.$axios.post("Settlements/get_settlements_insurance/",{insurance_id:a[t].id,nature_of_use:a[t].nature_of_use,generation_date:a[t].generation_date}).then(function(n){var l=(0,_.accAdd)(n.data.commercial_insurance_amount_fee,n.data.jiaoqiang_insurance_amount_fee),r=n.data.jiaoqiang_fee,o=n.data.commercial_fee,i=(0,s.default)(a[t].settlementForm,{actual_settlement_fee:l,settlement_fee:l});e.$set(a,t,(0,s.default)(a[t],{commercial_insurance_amount_fee:n.data.commercial_insurance_amount_fee+" /费率:"+o+"%",jiaoqiang_insurance_amount_fee:n.data.jiaoqiang_insurance_amount_fee+" /费率:"+r+"%",total_amount:l,settlementForm:i}))})},r=0;r<a.length;r++)l(r);e.orders=a,e.total=n.count,e.loading=!1;case 14:case"end":return t.stop()}},t,e)}))()},getSummaries:function(e){var t=e.columns,n=e.data,a=[];return t.forEach(function(e,t){if(0===t)return void(a[t]="总价");var l=n.map(function(t){return Number(t[e.property])});l.every(function(e){return isNaN(e)})?a[t]="N/A":(a[t]=l.reduce(function(e,t){var n=Number(t);return isNaN(n)?e:e+t},0),a[t]+=" 元")}),a}}}},767:function(e,t,n){t=e.exports=n(738)(),t.push([e.i,"#el_link{position:relative}.span_first{display:inline-block;width:100px}","",{version:3,sources:["D:/OutsourcingProject/Insurance_policy_system/InsuranceFront/src/views/Insurance/Settlements.vue"],names:[],mappings:"AACA,SACE,iBAAmB,CACpB,AACD,YACE,qBAAsB,AACtB,WAAa,CACd",file:"Settlements.vue",sourcesContent:["\n#el_link {\n  position: relative;\n}\n.span_first {\n  display: inline-block;\n  width: 100px;\n}\n.span_end {\n}\n"],sourceRoot:""}])},776:function(e,t,n){var a=n(767);"string"==typeof a&&(a=[[e.i,a,""]]),a.locals&&(e.exports=a.locals);n(739)("6343fe51",a,!0)},788:function(e,t){e.exports={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("section",[n("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[n("el-form",{attrs:{inline:!0,model:e.filters}},[n("el-form-item",[n("el-input",{attrs:{placeholder:"使用性质"},nativeOn:{keydown:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getOrders.apply(null,arguments)}},model:{value:e.filters.nature_of_use,callback:function(t){e.$set(e.filters,"nature_of_use",t)},expression:"filters.nature_of_use"}})],1),e._v(" "),n("el-form-item",[n("el-input",{attrs:{placeholder:"渠道"},nativeOn:{keydown:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getOrders.apply(null,arguments)}},model:{value:e.filters.chanel_rate_id__chanel,callback:function(t){e.$set(e.filters,"chanel_rate_id__chanel",t)},expression:"filters.chanel_rate_id__chanel"}})],1),e._v(" "),n("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"保单生成开始时段","end-placeholder":"保单生成结束时段","value-format":"yyyy-MM-dd"},model:{value:e.filters.datetimerange,callback:function(t){e.$set(e.filters,"datetimerange",t)},expression:"filters.datetimerange"}}),e._v(" "),n("el-form-item",[n("el-select",{attrs:{clearable:"",placeholder:"请选择"},model:{value:e.filters.settlement_status,callback:function(t){e.$set(e.filters,"settlement_status",t)},expression:"filters.settlement_status"}},e._l(e.options,function(e){return n("el-option",{key:e.settlement_status,attrs:{label:e.label,value:e.settlement_status}})}),1)],1),e._v(" "),n("el-form-item",[n("el-button",{attrs:{type:"primary"},on:{click:e.getOrders}},[e._v("筛选")])],1),e._v(" "),n("el-form-item",[n("el-button",{on:{click:e.showSettlementDialog}},[e._v("结算当前选中")])],1),e._v(" "),n("el-form-item")],1)],1),e._v(" "),n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"multipleTable",staticStyle:{width:"100%"},attrs:{data:e.orders,"highlight-current-row":"",border:"","show-summary":""},on:{"selection-change":e.handleSelectionChange}},[n("el-table-column",{attrs:{type:"selection",width:"55"}}),e._v(" "),n("el-table-column",{attrs:{prop:"nature_of_use",label:"使用性质"}}),e._v(" "),n("el-table-column",{attrs:{prop:"generation_date",label:"保单生成日期",sortable:""}}),e._v(" "),n("el-table-column",{attrs:{prop:"commercial_insurance_no",label:"商业险保单号"}}),e._v(" "),n("el-table-column",{attrs:{prop:"jiaoqiang_insurance_no",label:"交强险保单号"}}),e._v(" "),n("el-table-column",{attrs:{prop:"applicant",label:"投保人"}}),e._v(" "),n("el-table-column",{attrs:{prop:"insured",label:"被保险人"}}),e._v(" "),n("el-table-column",{attrs:{prop:"commercial_insurance_amount",label:"商业险金额"}}),e._v(" "),n("el-table-column",{attrs:{prop:"jiaoqiang_insurance_amount",label:"交强险金额"}}),e._v(" "),n("el-table-column",{attrs:{prop:"vehicel_and_vessel_tax",label:"车船税"}}),e._v(" "),n("el-table-column",{attrs:{prop:"total_premium",label:"保费合计"}}),e._v(" "),n("el-table-column",{attrs:{prop:"salesman",label:"业务员"}}),e._v(" "),n("el-table-column",{attrs:{prop:"chanel_rate_id.chanel",label:"渠道"}}),e._v(" "),n("el-table-column",{attrs:{label:"结算状态"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.row.settlement_status?n("span",[e._v("是")]):n("span",[e._v("否")])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"结算金额",width:"200px"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("div",[e._v("商业险金额："+e._s(t.row.commercial_insurance_amount_fee))]),e._v(" "),n("div",[e._v("交强险金额："+e._s(t.row.jiaoqiang_insurance_amount_fee))]),e._v(" "),n("div",[e._v("总金额："+e._s(t.row.total_amount))])]}}])}),e._v(" "),n("el-table-column",{attrs:{label:"结算表单",width:"330px"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.row.settlement_status?n("div",[n("section",{staticStyle:{width:"300px"}},[n("span",{staticClass:"span_first"},[e._v(" 结算单id：")]),e._v("\n            "+e._s(t.row.settlements_id.id)+"\n          ")]),e._v(" "),n("section",{staticStyle:{width:"300px"}},[n("span",{staticClass:"span_first"},[e._v(" 结算单id：")]),e._v("\n            实际结算金额:\n            "+e._s(t.row.settlements_id.actual_settlement_fee)+"\n          ")]),e._v(" "),n("section",{staticStyle:{width:"300px"}},[n("span",{staticClass:"span_first"},[e._v(" 结算日期：")]),e._v("\n            结算日期：\n            "+e._s(t.row.settlements_id.settlement_date)+"\n          ")]),e._v(" "),n("section",[n("span",{staticClass:"span_first"},[e._v(" 结算方式:")]),e._v("\n            "+e._s(t.row.settlements_id.settlement_method)+"\n          ")]),e._v(" "),n("section",[n("span",{staticClass:"span_first"},[e._v(" 收款账号：")]),e._v("\n            "+e._s(t.row.settlements_id.receiving_account)+"\n          ")]),e._v(" "),n("section",[n("span",{staticClass:"span_first"},[e._v(" 备注:")]),e._v("\n            "+e._s(t.row.settlements_id.note)+"\n          ")])]):n("div",[n("div",[e._v("\n            费率计算金额：\n            "),n("el-tag",[e._v(e._s(t.row.settlementForm.settlement_fee))])],1),e._v(" "),n("div",[e._v("\n            实际结算金额：\n            "),n("el-input-number",{attrs:{precision:2,"controls-position":"right"},model:{value:t.row.settlementForm.actual_settlement_fee,callback:function(n){e.$set(t.row.settlementForm,"actual_settlement_fee",n)},expression:"scope.row.settlementForm.actual_settlement_fee"}})],1),e._v(" "),n("div",[e._v("\n            结算日期：\n            "),n("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期时间","value-format":"yyyy-MM-dd HH:mm:ss"},model:{value:t.row.settlementForm.settlement_date,callback:function(n){e.$set(t.row.settlementForm,"settlement_date",n)},expression:"scope.row.settlementForm.settlement_date"}})],1),e._v(" "),n("div",[n("span",{staticStyle:{width:"150px"}},[e._v("结算方式：")]),e._v(" "),n("div",{staticStyle:{width:"220px",display:"inline-block"}},[n("el-input",{attrs:{placeholder:"结算方式"},model:{value:t.row.settlementForm.settlement_method,callback:function(n){e.$set(t.row.settlementForm,"settlement_method",n)},expression:"scope.row.settlementForm.settlement_method"}})],1)]),e._v(" "),n("div",[n("span",{staticStyle:{width:"150px"}},[e._v("收款账号：")]),e._v(" "),n("div",{staticStyle:{width:"220px",display:"inline-block"}},[n("el-input",{attrs:{placeholder:"收款账号"},model:{value:t.row.settlementForm.receiving_account,callback:function(n){e.$set(t.row.settlementForm,"receiving_account",n)},expression:"scope.row.settlementForm.receiving_account"}})],1)]),e._v(" "),n("div",[n("span",[e._v("备注备注：")]),e._v(" "),n("div",{staticStyle:{width:"220px",display:"inline-block"}},[n("el-input",{attrs:{placeholder:"备注"},model:{value:t.row.settlementForm.note,callback:function(n){e.$set(t.row.settlementForm,"note",n)},expression:"scope.row.settlementForm.note"}})],1)]),e._v(" "),n("div",[n("el-button",{attrs:{type:"primary"},on:{click:function(n){return e.subSettlement(t.row.settlementForm)}}},[e._v("结算")])],1)])]}}])})],1),e._v(" "),n("el-button",[e._v("结算当前选中")]),e._v(" "),n("el-col",{staticClass:"toolbar",attrs:{span:24}},[n("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":e.pageSize,total:e.total},on:{"current-change":e.handleCurrentChange}})],1),e._v(" "),n("el-dialog",{attrs:{title:"结算页面",visible:e.settlementDialog},on:{"update:visible":function(t){e.settlementDialog=t}}},[n("el-form",{staticClass:"demo-form-inline",attrs:{model:e.settlementData,"label-width":"180px",inline:!0}},[n("div",[n("h1",[e._v("选中的保单号")]),e._v(" "),e._l(e.multipleSelection,function(t){return n("span",{key:t.id},[e._v("\n          "+e._s(t.jiaoqiang_insurance_no)+"\n        ")])})],2),e._v(" "),n("el-form-item",{attrs:{label:"结算总金额"}},[e._v("\n        "+e._s(e.settlementData.settlement_fee)+"\n      ")]),e._v(" "),n("el-form-item",{attrs:{label:"实际结算总金额"}},[n("el-input-number",{attrs:{precision:2,"controls-position":"right"},model:{value:e.settlementData.actual_settlement_fee,callback:function(t){e.$set(e.settlementData,"actual_settlement_fee",t)},expression:"settlementData.actual_settlement_fee"}})],1),e._v(" "),n("el-form-item",{attrs:{label:"结算日期"}},[n("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期时间","value-format":"yyyy-MM-dd HH:mm:ss"},model:{value:e.settlementData.settlement_date,callback:function(t){e.$set(e.settlementData,"settlement_date",t)},expression:"settlementData.settlement_date"}})],1),e._v(" "),n("el-form-item",{attrs:{label:"结算方式"}},[n("el-input",{attrs:{"auto-complete":"off"},model:{value:e.settlementData.settlement_method,callback:function(t){e.$set(e.settlementData,"settlement_method",t)},expression:"settlementData.settlement_method"}})],1),e._v(" "),n("el-form-item",{attrs:{label:"收款账号"}},[n("el-input",{attrs:{"auto-complete":"off"},model:{value:e.settlementData.receiving_account,callback:function(t){e.$set(e.settlementData,"receiving_account",t)},expression:"settlementData.receiving_account"}})],1),e._v(" "),n("el-form-item",{attrs:{label:"备注"}},[n("el-input",{attrs:{"auto-complete":"off"},model:{value:e.settlementData.note,callback:function(t){e.$set(e.settlementData,"note",t)},expression:"settlementData.note"}})],1)],1),e._v(" "),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{on:{click:function(t){e.settlementDialog=!1}}},[e._v("取 消")]),e._v(" "),n("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.subSettlement(e.settlementData)}}},[e._v("提交")])],1)],1)],1)},staticRenderFns:[]}}});
//# sourceMappingURL=3.fd66076f9ecccffdb5fb.js.map