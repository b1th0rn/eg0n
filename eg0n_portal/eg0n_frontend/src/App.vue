<template>
  <header>
    <BNavbar
      class="nav"
      v-b-color-mode="'dark'"
      :toggleable="true"
      variant="secondary"
    >
      <img :src="logoPath" class="logo" />
      <BNavbarBrand href="/" tag="h1" class="mb-0">eg0n Portal</BNavbarBrand>
      <BNavbarToggle target="nav-offcanvas" />
      <BOffcanvas id="nav-offcanvas" title="eg0n Portal" placement="end" is-nav>
        <BNavbarNav>
          <BNavItem href="/admin">Login</BNavItem>
        </BNavbarNav>
        <BNavbarNav>
          <BNavItem href="/">Home</BNavItem>
          <BNavItem href="/Vulns">Vulns</BNavItem>
        </BNavbarNav>
      </BOffcanvas>
    </BNavbar>
  </header>
  <RouterView />
</template>

<script>
import { RouterView } from "vue-router";
import { useConfigurationStore } from "@/stores/configuration";

export default {
  mounted() {
    this.configuration = useConfigurationStore();
    let contextName = this.$el.parentElement.getAttribute("data-contextName");
    let csrf_token = this.$el.parentElement.getAttribute("data-csrfToken");

    if (contextName) {
      this.configuration.setContextName(contextName);
    }

    if (csrf_token) {
      this.configuration.setCsrfToken(csrf_token);
    }
  },

  computed: {
    logoPath: {
      get() {
        let baseUri = document.baseURI;
        return new URL("/static/images/bitHorn.jpg", baseUri);
      },
    },
  },
};
</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  display: flex;
  place-items: center;
  position: sticky;
  padding-bottom: 1rem;
  top: 0;
  z-index: 999;
  /* padding-right: calc(var(--section-gap) / 2); */
}

nav {
  width: 100%;
  text-align: center;
  font-size: 1rem;
  padding: 1rem;
  /* margin-top: 1rem; */
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.logo {
  margin: 0 2rem 0 0;
  background-repeat: no-repeat;
  background-position: 50%;
  border-radius: 50%;
  width: 75px;
  height: 75px;
}
</style>
