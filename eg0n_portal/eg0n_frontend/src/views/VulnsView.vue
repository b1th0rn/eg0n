<template>
  <BContainer>
    <h1>Welcome on vulns page</h1>
    </br>
    <span class="mb-2 mt-2">This page show a list of vuls find by our validtor anc contributor, 
      you can use a search bar to filter result by desciption</span>
    <VulnSearch 
      @changeText="changeSearchText($event)"
      @emitSearch="search()"
    />
    <Table 
    :items="vulns"
    :fieldsConfiguration="fieldsConfiguration"
    :currentPage="currentPage"
    :perPageValue="perPage"
    :totalVulns="total"
    :defaultSort="defaultSortBy"
    @changePage="changePage($event)"
    @changePerPage="changePerPage($event)"
    @changeSort="changeSort($event)"
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
    this.fieldsConfiguration = [
      {key: "cve", sortable:false},
      {key: "name", sortable:false},
      {key: "description", sortable:false},
      {key: "publish_date", sortable:true},
      {key: "author", sortable:true},
    ];
    this.search();
  },

  methods:  {
    async search() {
      var response = await eg0nApiService.GetVulns(this.vulnSearch);  
      this.currentPage = response.data.current_page;
      this.totalVulns = response.data.total_items;
      this.items = response.data.vulnerabilities;
    },

    changeSort(newValue) {   
      this.sort= newValue; 
      this.changePage(1);
    },

    openVulnDetail(payload) {
      console.log("doppio click su una riga della tabella",payload);
    },

    changePerPage(newValue) {
      this.perPage = newValue;
      this.changePage(1);
    },

    changePage(newValue) {
      this.currentPage = newValue;
      this.search();
    },

    changeSearchText(newValue) {
      this.searchText = newValue;
      this.changePage(1);
    }  
  },

  computed:{
    searchText: {
      get() {
        return this.vulnSearch.text;
      },
      set(newValue){
        this.vulnSearch.text = newValue;
        //this.search();
      }
    },

    currentPage: {
      get() {
        return this.vulnSearch.pageNumber;
      },
      set(newValue) {
        this.vulnSearch.pageNumber = newValue;
      }
    },

    sort: {
      get() {
        return this.VulnSearch.sortBy;
      },
      set(newValue) {
        this.vulnSearch.sortBy = newValue.key;
        this.vulnSearch.sortOrder = newValue.order ? newValue.order : "asc";
      }
    },

    defaultSortBy: {
      get() {
        let keyValue = this.vulnSearch.sortBy ? this.vulnSearch.sortBy : "publish_date";
        let orderValue = this.vulnSearch.sortOrder ? this.vulnSearch.sortOrder : "asc";  
        return [{key: keyValue, order: orderValue}] 
      }
    },

    perPage: {
      get() {
        return this.vulnSearch.perPage;
      },
      set(newValue)
      {
        this.vulnSearch.perPage = newValue;
        //this.search();
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
  },
}
</script>
<style>
</style>
