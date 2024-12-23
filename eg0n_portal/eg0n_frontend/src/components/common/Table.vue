<template>
  <BContainer>
    <BRow>
    <BCol md="4">
    </BCol>
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
        <BFormSelect id="per-page-select"
          v-model="perPage"
          :options="perPageOptions"
          size="sm">
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
      class="my'0">
      
      </BPagination>
    </BCol>
    </BRow>
    <BRow>      
    </BRow>
    <BTable 
    :items="items" 
    :fields="fieldsConfiguration"
    :per-page="perPage"
    :current-page="curPage"
    :sorted="sort"
    @row-dblclicked="
      (row, index, e) => {
        rowDblClicked(row, index, e)
      }
    "
    @sorted="sort($event)"/>

  </BContainer>
</template>

<script>
export default {
  name: "VulnTable",
  props:{
    items: Array,
    fieldsConfiguration: Array,
    currentPage: Number,
    totalVulns: Number,
    perPageValue: 25,
  },

  data() {
    return {
    
    }
  },

  mounted()
  {
    console.log("dentro table.vue");
    if(!this.fieldsConfiguration || this.fieldsConfiguration.length == 0){
      /* manage base configuration */
    }
  },
  methods: {
    sort(event,value) {
      console.log("change sorting",value,event);
      this.$emit('changeSort',event);
    },

    rowDblClicked(item,index,event) 
    {
      let payload = {
        item,
        index,
        event
      };
      this.$emit("rowDblClicked",payload);
    }
  },

  computed:
  {
    perPageOptions() {
      return [2,25,50,75,100];
    },


    perPage: {
      get() {
        return this.perPageValue;
      },
      set(newValue) {
        console.log("in table.vue set perpage",newValue);
        //this.perPageValue = newValue;
        this.$emit('changePerPage',newValue);
      }
    },

    curPage: {
    get() {
      if(this.currentPage && this.currentPage == 0)
      {
        return 1; 
      }
      return this.currentPage;
      },
      set(newValue){
        console.log("in table.vue set curPage", newValue);
        this.$emit('changePage',newValue);
      }
    }
  },

  
}
</script>
