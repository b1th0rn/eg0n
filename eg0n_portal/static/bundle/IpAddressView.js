import{e as h,c as g,_ as c,a as p,b as f}from"./eg0nApiServices.js";import{_ as m,c as S,w as P,o as _,a as n,b as i}from"./eg0nPortal.js";const b={name:"IpAddrView",data(){return{ipAddSearch:{text:"",pageNumber:1,perPage:25,sortBy:"publish_date",sortOrder:"asc"},items:[],totalVulns:0,fieldsConfiguration:[],showDetails:!1,ipSelected:{}}},mounted(){this.fieldsConfiguration=[{key:"ip_address",sortable:!1},{key:"url",sortable:!1},{key:"fqdn",sortable:!0},{key:"publish_date",sortable:!0},{key:"author",sortable:!0}],this.search()},methods:{async search(){var e=await h.GetIPAddr(this.ipAddSearch);this.currentPage=e.data.current_page,this.totalVulns=e.data.total_items,this.items=e.data.ip_address_list},changeSort(e){this.sort=e,this.changePage(1)},openIPDetails(e){this.ipSelected=e.item,this.showDetails=!0,console.log("doppio click su una riga della tabella",e)},closeVulnDetails(){this.showDetails=!1},changePerPage(e){this.perPage=e,this.changePage(1)},changePage(e){this.currentPage=e,this.search()},changeSearchText(e){this.searchText=e,this.changePage(1)}},computed:{searchText:{get(){return this.ipAddSearch.text},set(e){this.ipAddSearch.text=e}},currentPage:{get(){return this.ipAddSearch.pageNumber},set(e){this.ipAddSearch.pageNumber=e}},sort:{get(){return this.ipAddSearch.sortBy},set(e){this.ipAddSearch.sortBy=e.key,this.ipAddSearch.sortOrder=e.order?e.order:"asc"}},defaultSortBy:{get(){let e=this.ipAddSearch.sortBy?this.ipAddSearch.sortBy:"publish_date",t=this.ipAddSearch.sortOrder?this.ipAddSearch.sortOrder:"asc";return[{key:e,order:t}]}},perPage:{get(){return this.ipAddSearch.perPage},set(e){this.ipAddSearch.perPage=e}},ipAddress:{get(){return this.items}},total:{get(){return this.totalVulns}}}};function A(e,t,y,C,a,r){const o=c,l=p,d=f,u=g;return _(),S(u,null,{default:P(()=>[t[7]||(t[7]=n("h1",null,"Welcome on vulns page",-1)),t[8]||(t[8]=n("span",{class:"mb-2 mt-2"},"This page show a list of vuls find by our validtor anc contributor, you can use a search bar to filter result by desciption",-1)),i(o,{onChangeText:t[0]||(t[0]=s=>r.changeSearchText(s)),onEmitSearch:t[1]||(t[1]=s=>r.search())}),i(l,{items:r.ipAddress,fieldsConfiguration:a.fieldsConfiguration,currentPage:r.currentPage,perPageValue:r.perPage,totalVulns:r.total,defaultSort:r.defaultSortBy,onChangePage:t[2]||(t[2]=s=>r.changePage(s)),onChangePerPage:t[3]||(t[3]=s=>r.changePerPage(s)),onChangeSort:t[4]||(t[4]=s=>r.changeSort(s)),onRowDblClicked:t[5]||(t[5]=s=>r.openIPDetails(s))},null,8,["items","fieldsConfiguration","currentPage","perPageValue","totalVulns","defaultSort"]),i(d,{showDetails:a.showDetails,vuln:a.ipSelected,onCloseDescription:t[6]||(t[6]=s=>r.closeVulnDetails(s))},null,8,["showDetails","vuln"])]),_:1})}const k=m(b,[["render",A]]);export{k as default};
