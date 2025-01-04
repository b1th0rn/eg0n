<template>
  <BOffcanvas
    v-model="showPanel"
    title="Vuln Description"
    placement="end"
    shodow="false"
  >
    <BNavbarNav>
      <BRow class="my-1" v-for="[key, value] of Object.entries(vuln)">
        <BCol cols="4">{{ key }}:</BCol>
        <BCol cols="8">{{ value }}</BCol>
        <hr class="hr" />
      </BRow>
    </BNavbarNav>
  </BOffcanvas>
</template>

<script>
export default {
  name: "VulnDetails",

  props: {
    showDetails: Boolean,
    vuln: Object,
  },

  mounted() {
    console.log("mounted vulnDetails");
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
