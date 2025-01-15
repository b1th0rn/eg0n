<template>
  <BContainer>
    <h1>Welcome on Hash page</h1>
    <span class="mb-2 mt-2"
      >This page show a list of hash find by our validtor and contributor, you
      can use a search bar to filter result</span
    >
    <SearchBar @changeText="changeSearchText($event)" @emitSearch="search()" />
    <Table
      :items="hashs"
      :fieldsConfiguration="fieldsConfiguration"
      :currentPage="currentPage"
      :perPageValue="perPage"
      :totalVulns="total"
      :defaultSort="defaultSortBy"
      @changePage="changePage($event)"
      @changePerPage="changePerPage($event)"
      @changeSort="changeSort($event)"
      @rowDblClicked="openHashDetails($event)"
    />
    <Details
      :showDetails="showDetails"
      :vuln="hashSelected"
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
  name: "VulnView",

  data() {
    return {
      hashSearch: {
        text: "",
        pageNumber: 1,
        perPage: 25,
        sortBy: "publish_date",
        sortOrder: "asc",
      },
      items: [],
      totalHashs: 0,
      fieldsConfiguration: [],
      showDetails: false,
      hashSelected: {},
    };
  },

  mounted() {
    this.fieldsConfiguration = [
      { key: "filename", sortable: true },
      { key: "platform", sortable: false },
      { key: "md5", sortable: false },
      { key: "publish_date", sortable: true },
      { key: "author", sortable: true },
    ];
    this.search();
  },

  methods: {
    async search() {
      var response = await eg0nApiService.GetHashs(this.hashSearch);
      this.currentPage = response.data.current_page;
      this.totalHashs = response.data.total_items;
      this.items = response.data.hash_list;
    },

    changeSort(newValue) {
      this.sort = newValue;
      this.changePage(1);
    },

    openHashDetails(payload) {
      this.hashSelected = payload.item;
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
        return this.hashSearch.text;
      },
      set(newValue) {
        this.hashSearch.text = newValue;
        //this.search();
      },
    },

    currentPage: {
      get() {
        return this.hashSearch.pageNumber;
      },
      set(newValue) {
        this.hashSearch.pageNumber = newValue;
      },
    },

    sort: {
      get() {
        return this.hashSearch.sortBy;
      },
      set(newValue) {
        this.hashSearch.sortBy = newValue.key;
        this.hashSearch.sortOrder = newValue.order ? newValue.order : "asc";
      },
    },

    defaultSortBy: {
      get() {
        let keyValue = this.hashSearch.sortBy
          ? this.hashSearch.sortBy
          : "publish_date";
        let orderValue = this.hashSearch.sortOrder
          ? this.hashSearch.sortOrder
          : "asc";
        return [{ key: keyValue, order: orderValue }];
      },
    },

    perPage: {
      get() {
        return this.hashSearch.perPage;
      },
      set(newValue) {
        this.hashSearch.perPage = newValue;
        //this.search();
      },
    },

    hashs: {
      get() {
        return this.items;
      },
    },

    total: {
      get() {
        return this.totalHashs;
      },
    },
  },
};
</script>
<style></style>
