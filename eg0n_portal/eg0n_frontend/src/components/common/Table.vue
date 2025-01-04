<template>
  <BContainer>
    <BRow>
      <BCol md="4"> </BCol>
      <BCol sm="5" md="4" class="my-1">
        <BFormGroup
          label="Per page"
          label-for="per-page-select"
          label-cols-sm="6"
          label-cols-md="4"
          label-align-sm="right"
          label-size="sm"
          class="mb-0"
        >
          <BFormSelect
            id="per-page-select"
            v-model="perPage"
            :options="perPageOptions"
            size="sm"
          >
          </BFormSelect>
        </BFormGroup>
      </BCol>
      <BCol md="4" class="my-1">
        <BPagination
          v-model="curPage"
          :total-rows="totalVulns"
          :perPage="perPage"
          :align="'fill'"
          size="sm"
          class="my'0"
        >
        </BPagination>
      </BCol>
    </BRow>
    <BRow> </BRow>
    <!-- :current-page="curPage" -->
    <BTable
      :items="vulnsList"
      :fields="fieldsConfiguration"
      :sort-by="defaultSort"
      multisort="false"
      no-local-sorting="true"
      :per-page="perPage"
      :sorted="sort"
      @row-dblclicked="
        (row, index, e) => {
          rowDblClicked(row, index, e);
        }
      "
      @sorted="sort($event)"
    />
  </BContainer>
</template>

<script>
export default {
  name: "VulnTable",
  props: {
    items: Array,
    fieldsConfiguration: Array,
    currentPage: Number,
    totalVulns: Number,
    perPageValue: 25,
    defaultSort: Array,
  },

  mounted() {
    /* if(!this.fieldsConfiguration || this.fieldsConfiguration.length == 0){
       manage base configuration 
    } */
  },

  methods: {
    sort(event) {
      this.$emit("changeSort", event);
    },

    rowDblClicked(item, index, event) {
      let payload = {
        item,
        index,
        event,
      };
      this.$emit("rowDblClicked", payload);
    },
  },

  computed: {
    perPageOptions() {
      return [2, 25, 50, 75, 100];
    },

    perPage: {
      get() {
        return this.perPageValue;
      },
      set(newValue) {
        this.$emit("changePerPage", newValue);
      },
    },

    curPage: {
      get() {
        if (this.currentPage && this.currentPage == 0) {
          return 1;
        }
        return this.currentPage;
      },
      set(newValue) {
        this.$emit("changePage", newValue);
      },
    },

    vulnsList: {
      get() {
        return this.items;
      },
    },
  },
};
</script>
