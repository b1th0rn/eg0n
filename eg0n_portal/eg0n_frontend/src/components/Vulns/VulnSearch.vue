<template>
  <BContainer>
    <BRow>
      <BInputGroup class="mt-3" >
        <template #append>
          <BButton variant="outline-secondary" @click="emitSearch"><span class="material-icons">search</span></BButton>
          <!-- <BInputGroupText><span class="material-icons">search</span></BInputGroupText> -->
        </template>
        <BFormInput v-model="text"/>
      </BInputGroup>
    </BRow>
  </BContainer> 
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
    emitChangeText()
    {
      this.$emit("changeText",this.searchText);
    },
    emitSearch()
    {
      this.$emit("emitSearch");
    }
  },

  computed:{
    text: {
      get(){
        return this.searchText;
      },
      set(newValue) {
        this.searchText = newValue;
        if(this.searchTimer)
        {
          clearTimeout(this.searchTimer);
        }
        this.searchTimer = setTimeout(() => {
          this.emitChangeText()},this.searchDelay
        );
      }
    }
  }
}
</script>