(this["webpackJsonpdocassemble-app"]=this["webpackJsonpdocassemble-app"]||[]).push([[0],{345:function(e,t,a){},346:function(e,t,a){"use strict";a.r(t);var n=a(1),s=a(0),r=a.n(s),i=a(13),o=a.n(i),c=(a(88),a(89),a(11)),l=a(47),d=a(37),u=a(26),p=a(7),h=a(8),j=a(10),b=a(9),m=a(48),O=a(36),f=a(39),v=a.n(f),g=a(59),x=a(82),y=0;function k(e){return Object(n.jsx)(g.a,{id:"da_popover_"+y++,children:Object(n.jsx)(g.a.Content,{children:v()(e["data-content"])})})}var q={replace:function(e){var t,a=e.attribs,s=e.children;if(a)return a["data-js"]?Object(n.jsx)("a",{href:"#js",onClick:(t=a["data-js"],function(e){return console.log(t),e.preventDefault(),!1}),children:Object(f.domToReact)(s,q)}):"daterm"===a.class?Object(n.jsx)(x.a,{trigger:"click",transition:!1,placement:a["data-placement"]||"auto",overlay:k(a),children:Object(n.jsx)("span",{className:"daterm",children:Object(f.domToReact)(s,q)})}):void 0}};function w(e){return"string"!==typeof e?null:v()(e,q)}var S=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.html?Object(n.jsxs)("div",{className:"da-page-header",children:[Object(n.jsx)("h1",{className:"h3",id:"daMainQuestion",children:w(this.props.html)}),Object(n.jsx)("div",{className:"daclear"})]}):null}}]),a}(r.a.Component),C=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.html?Object(n.jsx)("div",{className:"da-subquestion",children:w(this.props.html)}):null}}]),a}(r.a.Component),_=a(30),N=a(15),T=a(12),E="WRITE_ANSWERS",I="SUBMIT_ANSWERS",B="GET_DATA",D="SET_SUBMITTED",R="GET_ERRORS",A="CREATE_MESSAGE",F="GET_CHECKIN",H="SET_HELP",L="SET_SOURCE",V=function(e,t,a){return{type:R,payload:{msg:e,status:t,variant:a}}},U=a(52),M=a.n(U),G=function(e){return{type:E,payload:{data:e}}},W="docassemble.demo:data/questions/questions.yml";var J=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(e){var n;return Object(p.a)(this,a),(n=t.call(this)).onChangeValue=n.onChangeValue.bind(Object(N.a)(n)),n}return Object(h.a)(a,[{key:"onChangeValue",value:function(e){this.props.writeAnswers(Object(_.a)({},this.props.name,e.target.value))}},{key:"render",value:function(){var e=this,t=0;return Object(n.jsx)("fieldset",{className:"da-field-radio",children:Object(n.jsx)("div",{className:"mb-3",onChange:this.onChangeValue,children:this.props.choices.map((function(a){return Object(n.jsx)(m.a.Check,{type:"radio",value:a.value,label:w(a.label),name:e.props.fieldName,id:e.props.fieldName+"_"+t++,checked:e.props.answers[e.props.name]===a.value,onChange:e.onChangeRadio},e.props.fieldName+"_"+t)}))})})}}]),a}(r.a.Component),P=Object(T.b)((function(e){return{answers:e.answers}}),{writeAnswers:G})(J),K=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){if("multiple_choice"===this.props.data.question.questionType)return"radio"===this.props.data.question.questionVariety?Object(n.jsx)(P,{name:this.props.data.question.fields[0].variable_name,fieldName:"_field_0",choices:this.props.data.question.fields[0].choices,answers:this.props.answers}):null;if("fields"===this.props.data.question.questionType){for(var e=this.props.data.question.fields.length,t=0;t<e;++t);return""}return null}}]),a}(r.a.Component),Q=Object(T.b)((function(e){return{submitted:e.submitted,answers:e.answers,data:e.data}}))(K),z=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(e){var n;return Object(p.a)(this,a),(n=t.call(this)).onClick=n.onClick.bind(Object(N.a)(n)),n}return Object(h.a)(a,[{key:"onClick",value:function(e){var t=e.target.value;"true"===e.target.value?t="True":"false"===e.target.value?t="False":"null"===e.target.value&&(t="None"),this.props.writeAnswers(Object(_.a)({},this.props.data.question.fields[0].variable_name,t))}},{key:"render",value:function(){var e=this;if("multiple_choice"===this.props.data.question.questionType){if("radio"===this.props.data.question.questionVariety)return Object(n.jsx)("fieldset",{className:"da-field-buttons",children:Object(n.jsx)("div",{children:Object(n.jsx)(O.a,{variant:"primary",className:"btn-da",type:"submit",disabled:this.props.submitted,children:w(this.props.data.question.continueLabel)},"button_0")})});if("buttons"===this.props.data.question.questionVariety){var t=0;return Object(n.jsx)("fieldset",{className:"da-field-buttons",children:Object(n.jsx)("div",{children:this.props.data.question.fields[0].choices.map((function(a){return Object(n.jsxs)(r.a.Fragment,{children:[Object(n.jsx)(O.a,{variant:"primary",className:"btn-da",type:"submit",disabled:e.props.submitted,value:a.value,onClick:e.onClick,children:w(a.label)},"button"+t)," "]},"buttonfragment"+t++)}))})})}return null}return null}}]),a}(r.a.Component),X=Object(T.b)((function(e){return{submitted:e.submitted,answers:e.answers,data:e.data}}),{writeAnswers:G})(z),Y=a(19),Z=a(46),$=a(34);Y.b.add(Z.a);var ee=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){var e;Object(p.a)(this,a);for(var n=arguments.length,s=new Array(n),r=0;r<n;r++)s[r]=arguments[r];return(e=t.call.apply(t,[this].concat(s))).onSubmit=function(t){t.preventDefault(),e.props.setSubmitted(!0),e.props.submitData()},e}return Object(h.a)(a,[{key:"componentDidMount",value:function(){this.props.getData(),this.props.setSubmitted(!1)}},{key:"render",value:function(){if(!this.props.data.question)return null;if(this.props.data.showHelp&&this.props.data.question.help){return Object(n.jsxs)(r.a.Fragment,{children:[Object(n.jsx)("div",{className:"mt-2 mb-2",children:Object(n.jsxs)(O.a,{variant:"info",children:[Object(n.jsx)($.a,{icon:["fas","caret-left"]})," ",this.props.data.question.helpBackLabel]})}),this.props.data.question.helpText.map((function(e){return Object(n.jsxs)(r.a.Fragment,{children:[e.heading?Object(n.jsx)("div",{className:"da-page-header",children:Object(n.jsx)("h1",{className:"h3",children:w(e.heading)})}):null,Object(n.jsx)("div",{children:w(e.content)})]},"help0")}))]})}return Object(n.jsxs)(m.a,{onSubmit:this.onSubmit,children:[Object(n.jsx)(S,{html:this.props.data.question.questionText}),Object(n.jsx)(C,{html:this.props.data.question.subquestionText}),Object(n.jsx)(Q,{}),Object(n.jsx)(X,{}),Object(n.jsxs)("div",{children:["Here are the answers: ",JSON.stringify(this.props.answers)]})]})}}]),a}(r.a.Component),te=Object(T.b)((function(e){return{submitted:e.submitted,answers:e.answers,data:e.data}}),{writeAnswers:G,submitAnswers:function(e){return{type:I,payload:{data:e}}},getData:function(){return function(e,t){var a,n=t(),s={i:W,session:n.data.session||sessionStorage.getItem("daSessionID")||"",secret:n.data.secret||sessionStorage.getItem("daSecret")||"",user_code:n.data.user_code||sessionStorage.getItem("daUserCode")||""};M.a.get("http://localhost/api/interview?"+(a=s,Object.entries(a).map((function(e){return e.map(encodeURIComponent).join("=")})).join("&"))).then((function(t){"activeElement"in document&&document.activeElement.blur();var a={session:n.data.session||sessionStorage.getItem("daSessionID"),secret:n.data.secret||sessionStorage.getItem("daSecret"),user_code:n.data.user_code||sessionStorage.getItem("daUserCode")};t.data.session&&s.session!=t.data.session&&sessionStorage.setItem("daSessionID",t.data.session),t.data.secret&&s.secret!=t.data.secret&&sessionStorage.setItem("daSecret",t.data.secret),t.data.user_code&&s.user_code!=t.data.user_code&&sessionStorage.setItem("daUserCode",t.data.user_code),e({type:B,payload:Object(c.a)(Object(c.a)({},a),t.data)})})).catch((function(t){return e(V(t.response?t.response.data:t,t.response?t.response.status:0,"danger"))}))}},setSubmitted:function(e){return{type:D,payload:e}},submitData:function(){return function(e,t){var a=t(),n={i:W,session:a.data.session,secret:a.data.secret,user_code:a.data.user_code,variables:a.answers};M.a.post("http://localhost/api/interview",n).then((function(t){"activeElement"in document&&document.activeElement.blur(),e({type:B,payload:t.data})})).catch((function(t){return e(V(t.response?t.response.data:"Error",t.response?t.response.status:0,"danger"))}))}}})(ee),ae=a(49),ne=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"componentDidUpdate",value:function(e){var t=this.props,a=t.error,n=t.alert;a!==e.error&&(console.log("msg is "+a.msg),a.msg&&(console.log("Doing alert"),n.error("".concat(a.msg))))}},{key:"render",value:function(){return Object(n.jsx)(s.Fragment,{})}}]),a}(s.Component),se=Object(T.b)((function(e){return{error:e.errors,message:e.messages}}))(Object(ae.b)()(ne)),re=a(78),ie=a(353),oe=a(58),ce=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.item.code?Object(n.jsx)(ie.a,{language:"yaml",style:oe.a,children:this.props.item.code}):null}}]),a}(r.a.Component),le=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.item.source_file?Object(n.jsx)("p",{children:Object(n.jsx)("small",{children:Object(n.jsxs)("strong",{children:["(from ",this.props.item.source_file,")"]})})}):null}}]),a}(r.a.Component),de=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){switch(this.props.item.reason){case"needed":return Object(n.jsxs)("h5",{children:[this.props.item.reason_text+" ",Object(n.jsx)("code",{children:this.props.item.variable_name})," at"," ",this.props.item.time]});default:return Object(n.jsxs)("h5",{children:[this.props.item.reason_text," at ",this.props.item.time]})}}}]),a}(r.a.Component),ue=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){var e;return this.props.data.showSource&&this.props.data.question.source?(e=this.props.data.showHelp?"help":"question",Object(n.jsxs)(r.a.Fragment,{children:[Object(n.jsx)(d.a,{children:Object(n.jsxs)(u.a,{xl:6,lg:6,md:8,sm:12,className:"offset-xl-3 offset-lg-3 offset-md-2",children:[Object(n.jsx)("h3",{children:"Readability"}),Object(n.jsxs)(re.a,{children:[Object(n.jsx)("thead",{children:Object(n.jsxs)("tr",{children:[Object(n.jsx)("th",{children:"Formula"}),Object(n.jsx)("th",{children:"Score"})]})}),Object(n.jsx)("tbody",{children:this.props.data.question.source.readability[e].map((function(e){return Object(n.jsxs)("tr",{children:[Object(n.jsx)("td",{children:e[0]}),Object(n.jsx)("td",{children:e[1]})]},e[0])}))})]})]})}),Object(n.jsx)(d.a,{children:Object(n.jsxs)(u.a,{md:12,children:[Object(n.jsx)("a",{rel:"noreferrer",target:"_blank",href:this.props.data.question.source.varsLink,children:this.props.data.question.source.varsLabel}),Object(n.jsx)("h3",{children:"Source code for question"}),Object(n.jsx)(ie.a,{language:"yaml",style:oe.a,children:this.props.data.question.source.history.source_code}),Object(n.jsx)("h4",{children:"How question came to be asked"}),Object(n.jsx)(r.a.Fragment,{children:this.props.data.question.source.history.steps.map((function(e){return Object(n.jsxs)(r.a.Fragment,{children:[Object(n.jsx)(de,{item:e}),Object(n.jsx)(le,{item:e}),Object(n.jsx)(ce,{item:e})]},"Step_"+e.index)}))})]})})]})):null}}]),a}(r.a.Component),pe=Object(T.b)((function(e){return{data:e.data}}))(ue),he=a(35),je=a(16),be=a(79);Y.b.add(be.a,Z.a);var me=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.data.phone?Object(n.jsx)(je.a.Item,{children:Object(n.jsxs)(je.a.Link,{role:"button",href:"#dahelp","data-target":"#dahelp",title:this.props.data.phone.title,className:"dapointer dahelptrigger",children:[Object(n.jsx)($.a,{icon:["fas","phone"],className:"da-chat-active"}),Object(n.jsx)("span",{className:"sr-only",children:this.props.data.phone.label})]})}):null}}]),a}(r.a.Component),Oe=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.data.chat?Object(n.jsx)(je.a.Item,{children:Object(n.jsxs)(je.a.Link,{href:"#dahelp","data-target":"#dahelp",className:"nav-link dapointer dahelptrigger",children:[Object(n.jsx)($.a,{icon:["fas","comment-alt"]}),Object(n.jsx)("span",{className:"sr-only",children:this.props.data.chat.label})]})}):null}}]),a}(r.a.Component),fe=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(e){var n;return Object(p.a)(this,a),(n=t.call(this)).doToggle=n.doToggle.bind(Object(N.a)(n)),n}return Object(h.a)(a,[{key:"doToggle",value:function(e){return e.preventDefault(),this.props.toggleHelp(),"activeElement"in document&&document.activeElement.blur(),!1}},{key:"render",value:function(){return this.props.data.question.help?Object(n.jsx)(je.a.Item,{children:Object(n.jsx)(je.a.Link,{className:"dapointer da-no-outline dahelptrigger",href:"#help",id:"dahelptoggle",onClick:this.doToggle,title:this.props.data.question.help.title,active:this.props.data.showHelp,children:this.props.data.question.help.label})}):null}}]),a}(r.a.Component),ve=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(e){var n;return Object(p.a)(this,a),(n=t.call(this)).doToggle=n.doToggle.bind(Object(N.a)(n)),n}return Object(h.a)(a,[{key:"doToggle",value:function(e){return e.preventDefault(),this.props.toggleSource(),"activeElement"in document&&document.activeElement.blur(),!1}},{key:"render",value:function(){return this.props.data.question.source?Object(n.jsx)(je.a.Item,{children:Object(n.jsx)(je.a.Link,{className:"da-no-outline d-none d-md-block",href:"#source",id:"dasourcetoggle",onClick:this.doToggle,title:this.props.data.question.source.title,active:this.props.data.showSource,children:this.props.data.question.source.label})}):null}}]),a}(r.a.Component),ge=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(e){var n;return Object(p.a)(this,a),(n=t.call(this)).clickBackButton=n.clickBackButton.bind(Object(N.a)(n)),n}return Object(h.a)(a,[{key:"clickBackButton",value:function(e){return console.log("go back"),e.preventDefault(),this.props.goBack(),!1}},{key:"render",value:function(){return this.props.data.question.allow_going_back?Object(n.jsx)(he.a.Brand,{href:"#",onClick:this.clickBackButton,children:Object(n.jsx)("button",{className:"dabackicon text-muted dabackbuttoncolor",title:this.props.data.question.backTitle,children:Object(n.jsxs)("span",{children:[Object(n.jsx)($.a,{icon:["fas","chevron-left"]}),Object(n.jsx)("span",{className:"daback",children:this.props.data.question.cornerBackButton})]})})},"daback"):null}}]),a}(r.a.Component),xe=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.data.question.menu&&0==this.props.data.question.menu.items.length?Object(n.jsx)(je.a.Link,{href:this.props.data.question.menu.top.href||"#",children:this.props.data.question.menu.top.anchor}):null}}]),a}(r.a.Component),ye=function(e){Object(j.a)(a,e);var t=Object(b.a)(a);function a(){return Object(p.a)(this,a),t.apply(this,arguments)}return Object(h.a)(a,[{key:"render",value:function(){return this.props.data&&this.props.data.question?Object(n.jsx)(he.a,{bg:this.props.data.question.navbarVariant,variant:this.props.data.question.navbarVariant,expand:"md",className:"fixed-top",children:Object(n.jsxs)(l.a,{className:"danavcontainer justify-content-start",children:[Object(n.jsx)(ge,{data:this.props.data,goBack:this.props.goBack}),Object(n.jsxs)(he.a.Brand,{id:"dapagetitle",className:"danavbar-title dapointer",href:"#",children:[Object(n.jsx)("span",{className:"d-none d-md-block",children:w(this.props.data.question.title)}),Object(n.jsx)("span",{className:"d-block d-md-none",children:w(this.props.data.question.short_title)})]},"datitle"),Object(n.jsxs)(je.a,{className:"damynavbar-right",children:[Object(n.jsx)(ve,{data:this.props.data,toggleSource:this.props.toggleSource}),Object(n.jsx)(fe,{data:this.props.data,toggleHelp:this.props.toggleHelp}),Object(n.jsx)(me,{data:this.props.data}),Object(n.jsx)(Oe,{data:this.props.data})]}),Object(n.jsx)(he.a.Toggle,{"aria-controls":"basic-navbar-nav",className:"ml-auto"}),Object(n.jsx)(he.a.Collapse,{id:"basic-navbar-nav",children:Object(n.jsx)(je.a,{className:"ml-auto",children:Object(n.jsx)(xe,{data:this.props.data})})})]})}):null}}]),a}(r.a.Component),ke=Object(T.b)((function(e){return{submitted:e.submitted,answers:e.answers,data:e.data}}),{goBack:function(){return function(e,t){var a=t(),n={i:W,session:a.data.session,secret:a.data.secret,user_code:a.data.user_code,command:"back"};M.a.post("http://localhost/api/interview",n).then((function(t){"activeElement"in document&&document.activeElement.blur(),e({type:B,payload:t.data})})).catch((function(t){return e(V(t.response?t.response.data:"Error",t.response?t.response.status:0,"danger"))}))}},toggleHelp:function(){return function(e,t){var a=t();e({type:H,payload:{showHelp:!a.data.showHelp}})}},toggleSource:function(){return function(e,t){var a=t();e({type:L,payload:{showSource:!a.data.showSource}})}}})(ye),qe=(a(345),a(22)),we=a(80),Se=a(81),Ce={};var _e=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:Ce,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case E:return Object(c.a)(Object(c.a)({},e),t.payload.data);case I:return Object(c.a)(Object(c.a)({},e),t.payload);case B:var a={};if(t.payload.question.fields)for(var n=t.payload.question.fields.length,s=0;s<n;++s)t.payload.question.fields[s].variable_name&&void 0!==t.payload.question.fields[s].default&&null!==t.payload.question.fields[s].default&&(a[t.payload.question.fields[s].variable_name]=t.payload.question.fields[s].default);return a;default:return e}},Ne={};var Te=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:Ne,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case B:return Object(c.a)(Object(c.a)({},e),{},{question:{}},t.payload);case F:case H:case L:return Object(c.a)(Object(c.a)({},e),t.payload);default:return e}};var Ee=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:null,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case D:return!!t.payload;case B:return!1;default:return e}},Ie={msg:{},status:null,variant:"danger"};var Be=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:Ie,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case R:return console.log("reducing GET_ERRORS"),{msg:t.payload.msg,status:t.payload.status,variant:t.payload.variant};default:return e}},De={};var Re=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:De,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case A:return t.payload;default:return e}},Ae=Object(qe.combineReducers)({data:Te,answers:_e,submitted:Ee,errors:Be,messages:Re}),Fe=[Se.a],He=Object(qe.createStore)(Ae,{data:{question:{}}},Object(we.composeWithDevTools)(qe.applyMiddleware.apply(void 0,Fe))),Le={timeout:5e3,position:"top center",containerStyle:{marginTop:"60px"}},Ve=function(e){var t=e.style,a=(e.options,e.message),s=e.close;return Object(n.jsxs)("div",{className:"alert alert-danger ",role:"alert",style:t,children:[a,Object(n.jsx)("button",{onClick:s,type:"button",className:"close",children:Object(n.jsx)("span",{"aria-hidden":"true",children:"\xd7"})})]})};var Ue=function(){return Object(n.jsx)(T.a,{store:He,children:Object(n.jsx)(ae.a,Object(c.a)(Object(c.a)({template:Ve},Le),{},{children:Object(n.jsxs)("div",{className:"da-pad-for-navbar",children:[Object(n.jsx)(ke,{}),Object(n.jsxs)(l.a,{children:[Object(n.jsx)(d.a,{children:Object(n.jsxs)(u.a,{xl:6,lg:6,md:8,className:"offset-xl-3 offset-lg-3 offset-md-2",children:[Object(n.jsx)(te,{}),Object(n.jsx)(se,{})]})}),Object(n.jsx)(pe,{})]})]})}))})},Me=function(e){e&&e instanceof Function&&a.e(3).then(a.bind(null,354)).then((function(t){var a=t.getCLS,n=t.getFID,s=t.getFCP,r=t.getLCP,i=t.getTTFB;a(e),n(e),s(e),r(e),i(e)}))};o.a.render(Object(n.jsx)(r.a.StrictMode,{children:Object(n.jsx)(Ue,{})}),document.getElementById("root")),Me()},88:function(e,t,a){}},[[346,1,2]]]);
//# sourceMappingURL=main.d393c7de.chunk.js.map