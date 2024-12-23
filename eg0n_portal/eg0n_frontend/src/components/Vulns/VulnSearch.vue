<template>
<BInputGroup class="mt-3" >
  <template #append>
    <BInputGroupText ><span class="material-icons">search</span></BInputGroupText>
  </template>
  <BFormInput v-model="text"/>
</BInputGroup>
<div class="mt-2">Value: {{ text }}</div>
</template>
<script>
export default {
  name: "VulnsSearhc",
  data() {
    return {
      searchText: "",
      searchTimer: null,
      searchDelay: 2000,
    }
  },

  methods: {
    callSearch()
    {
      this.$emit("search",this.searchText);
    }
  },

  computed:{
    text: {
      get(){
        console.log("dentro la get computed text");
        return this.searchText;
      },
      set(newValue) {
        console.log("dentro la set computed text new value: ", newValue);        
        this.searchText = newValue;
        if(this.searchTimer)
        {
          clearTimeout(this.searchTimer);
        }
        this.searchTimer = setTimeout(() => {
          this.callSearch()},this.searchDelay
        );
      }
    }
  }
}
</script>