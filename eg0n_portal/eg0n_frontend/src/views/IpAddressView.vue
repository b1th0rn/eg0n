<template>
  <BContainer>
    <h1>Welcome on vulns page</h1>
    <span class="mb-2 mt-2"
      >This page show a list of vuls find by our validtor anc contributor, you
      can use a search bar to filter result by desciption</span
    >
    <SearchBar @changeText="changeSearchText($event)" @emitSearch="search()" />
    <Table
      :items="ipAddress"
      :fieldsConfiguration="fieldsConfiguration"
      :currentPage="currentPage"
      :perPageValue="perPage"
      :totalVulns="total"
      :defaultSort="defaultSortBy"
      @changePage="changePage($event)"
      @changePerPage="changePerPage($event)"
      @changeSort="changeSort($event)"
      @rowDblClicked="openIPDetails($event)"
    />
    <Details
      :showDetails="showDetails"
      :vuln="ipSelected"
      @closeDescription="closeVulnDetails($event)"
    />
  </BContainer>
</template>
<script>
import SearchBar from "@/components/common/SearchBar.vue";
import Table from "@/components/common/Table.vue";
import Details from "@/components/common/Details.vue";
import { eg0nApiService } from "@/utils/eg0nApiServices";

export default {
  name: "IpAddrView",

  data() {
    return {
      ipAddSearch: {
        text: "",
        pageNumber: 1,
        perPage: 10,
        sortBy: "publish_date",
        sortOrder: "asc",
      },
      items: [],
      totalVulns: 0,
      fieldsConfiguration: [],
      showDetails: false,
      ipSelected: {},
    };
  },

  mounted() {
    this.fieldsConfiguration = [
      { key: "ip_address", sortable: false },
      { key: "url", sortable: false },
      { key: "fqdn", sortable: true },
      { key: "publish_date", sortable: true },
      { key: "author", sortable: true },
    ];
    this.search();
  },

  methods: {
    async search() {
      var response = await eg0nApiService.GetIPAddr(this.ipAddSearch);
      this.currentPage = response.data.current_page;
      this.totalVulns = response.data.total_items;
      this.items = response.data.ip_address_list;
    },

    changeSort(newValue) {
      this.sort = newValue;
      this.changePage(1);
    },

    openIPDetails(payload) {
      this.ipSelected = payload.item;
      this.showDetails = true;
      console.log("doppio click su una riga della tabella", payload);
    },

    closeVulnDetails() {
      this.showDetails = false;
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
    },
  },

  computed: {
    searchText: {
      get() {
        return this.ipAddSearch.text;
      },
      set(newValue) {
        this.ipAddSearch.text = newValue;
        //this.search();
      },
    },

    currentPage: {
      get() {
        return this.ipAddSearch.pageNumber;
      },
      set(newValue) {
        this.ipAddSearch.pageNumber = newValue;
      },
    },

    sort: {
      get() {
        return this.ipAddSearch.sortBy;
      },
      set(newValue) {
        this.ipAddSearch.sortBy = newValue.key;
        this.ipAddSearch.sortOrder = newValue.order ? newValue.order : "asc";
      },
    },

    defaultSortBy: {
      get() {
        let keyValue = this.ipAddSearch.sortBy
          ? this.ipAddSearch.sortBy
          : "publish_date";
        let orderValue = this.ipAddSearch.sortOrder
          ? this.ipAddSearch.sortOrder
          : "asc";
        return [{ key: keyValue, order: orderValue }];
      },
    },

    perPage: {
      get() {
        return this.ipAddSearch.perPage;
      },
      set(newValue) {
        this.ipAddSearch.perPage = newValue;
        //this.search();
      },
    },

    ipAddress: {
      get() {
        return this.items;
      },
    },

    total: {
      get() {
        return this.totalVulns;
      },
    },
  },
};
</script>
<style></style>
