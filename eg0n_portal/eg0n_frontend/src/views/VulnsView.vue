<template>
  <BContainer>
    <h1>Welcome on vulns page</h1>
    </br>
    <span class="mb-2 mt-2">This page show a list of vuls find by our validtor anc contributor, 
      you can use a search bar to filter result by desciption</span>
    <VulnSearch 
      @search="search($event)"
    />
    <Table 
    :items="vulns"
    :fieldsConfiguration="fieldsConfiguration"
    :currentPage="currentPage"
    :perPageValue="perPage"
    :totalVulns="total"
    @changePage="changePage($event)"
    @changePerPage="changePerPage($event)"
    @changeSort="sort($event)"
    @rowDblClicked="openVulnDetail($event)"
      />
  </BContainer>
</template>
<script>  
import VulnSearch from "@/components/Vulns/VulnSearch.vue";
import Table from "@/components/common/Table.vue";
import {eg0nApiService} from "@/utils/eg0nApiServices";

export default {
  name: "VulnView",

  data() {
    return {
      vulnSearch: {
        text: "",
        pageNumber: 1,
        perPage: 25,
        sortBy:"publish_date",
        sortOrder: "asc",        
      },
      items: [],
      totalVulns: 0,
      fieldsConfiguration: [],
    }
  },

  mounted() {
    this.items = [
      {cve: "cve1111", name: "name cve1111", description:"description cve1111", publish_date:"12/12/2023",author:"Pandevana"},
      {cve: "cve2222", name: "name cve2222", description:"description cve2222", publish_date:"12/12/2023",author:"Condor"},
      {cve: "cve3333", name: "name cve3333", description:"description cve3333", publish_date:"12/12/2023",author:"Sheliak"},
      {cve: "cve4444", name: "name cve4444", description:"description cve4444", publish_date:"12/12/2023",author:"soupnazi"},
      {cve: "cve5555", name: "name cve5555", description:"description cve5555", publish_date:"12/12/2023",author:"ASTRA"}
    ];

    this.fieldsConfiguration = [
      {key: "cve", sortable:false},
      {key: "name", sortable:false},
      {key: "description", sortable:false},
      {key: "publish_date", sortable:true},
      {key: "author", sortable:true},
    ]
    this.totalVulns=5;
  },

  methods:  {
    async search(text)
    {
      console.log("inserito testo da ricercare text: ",text);
      this.vulnSearch.text = text;
      var response = await eg0nApiService.GetVulns(this.vulnSearch);
      console.log("test post page search",response);
    },

    sort(event)
    {
      console.log("modificato il sorting della tabella", event);      
    },

    openVulnDetail(payload)
    {
      console.log("doppio click su una riga della tabella",payload);
    },

    changePerPage(newValue)
    {
      console.log("modificata il perpage",newValue);
      this.perPage = newValue;
    },

    changePage(newValue)
    {
      console.log("cambiata la pagina",newValue);
      this.currentPage = newValue;
    }
  
  },

  computed:{
    currentPage: {
      get()
      {
        return this.vulnSearch.pageNumber;
      },
      set(newValue) {
        this.vulnSearch.pageNumber = newValue
      }
    },
    perPage: {
      get() {
        return this.vulnSearch.perPage;
      },
      set(newValue)
      {
        this.vulnSearch.perPage = newValue;
      }
    },
    vulns: {
      get(){
        return this.items
      }
    },
    total: {
      get() {
        return this.totalVulns;
      }
    }
  }
}
</script>
<style>
</style>
