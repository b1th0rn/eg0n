<template>
  <BOffcanvas
    v-model="showPanel"
    title="Vuln Description"
    placement="end"
    shodow="false"
  >
    <BNavbarNav>
      <BRow class="my-1" v-for="[key, value] of Object.entries(vuln)">
        <BCol cols="4">{{ capitalizeKey(key) }}:</BCol>
        <BCol cols="8">{{ value }}</BCol>
        <hr class="hr" />
      </BRow>
    </BNavbarNav>
  </BOffcanvas>
</template>

<script>
export default {
  name: "Details",

  props: {
    showDetails: Boolean,
    vuln: Object,
  },

  mounted() {
    console.log("mounted vulnDetails");
  },

  methods: {
    capitalizeKey(string)
    {
      string = string[0].toUpperCase() + string.slice(1);
      return string.replace('_',' ');
    }
  },

  computed: {
    showPanel: {
      get() {
        return this.showDetails;
      },
      set(newValue) {
        this.$emit("closeDescription");
      },
    },
  },
};
</script>
