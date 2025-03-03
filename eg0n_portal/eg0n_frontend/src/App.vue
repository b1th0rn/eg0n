<template>
  <header>
    <BNavbar
      class="nav"
      v-b-color-mode="'dark'"
      :toggleable="true"
      variant="secondary"
    >
      <a class="img-link" href="/">
        <img :src="logoPath" class="logo" />
      </a>
      <BNavbarBrand href="/" tag="h1" class="mb-0">eg0n Portal</BNavbarBrand>
      <BNavbarToggle target="nav-offcanvas" />
      <BOffcanvas id="nav-offcanvas" title="eg0n Portal" placement="end" is-nav>
        <BNavbarNav>
          <BNavItem href="/admin">
            <div class="nav-custom-link">
              <span class="material-icons">login</span>
              <span>Login</span>
            </div> 
            </BNavItem>
        </BNavbarNav>
        <hr class="hr" />
        <BNavbarNav>
          <BNavItem href="/" >
            <div class="nav-custom-link">
              <span class="material-icons">home</span>
              <span>Home</span>
            </div>            
          </BNavItem>
          <BNavItem href="/Vulns"> 
            <div class="nav-custom-link">
              <span class="material-icons">warning</span>
              <span>Vulns</span>
            </div> 
          </BNavItem>
          <BNavItem href="/Hash">
            <div class="nav-custom-link">
              <span class="material-icons">bug_report</span>
              <span>Hash</span>
            </div>
          </BNavItem>
          <BNavItem href="/IpAdd">
            <div class="nav-custom-link">
              <span class="material-icons">dns</span>
              <span>IP Address</span>
            </div>
          </BNavItem>
          <BNavItem href="/ScoreBoard">
            <div class="nav-custom-link">
              <span class="material-icons">scoreboard</span>
              <span>Top Contributors</span>
            </div>
          </BNavItem>
        </BNavbarNav>
      </BOffcanvas>
    </BNavbar>
  </header>
  <footer>
    <BNavbar 
    class="nav footer-nav"
    v-b-color-mode="'dark'"
    variant="secondary"
    :toggleable="true"
    fixed="bottom">
      <BRow class="footer-row my-1">
        <BCol class="nav-custom-link">          
          <img alt="" width="24" height="24" :src="discordLogo">
          <a class="nav-link" href="https://discord.gg/Ys5AAbsyyH">Discord Server</a>          
        </BCol>
        <BCol class="nav-custom-link">          
          <img alt="" width="24" height="24" :src="githubLogo">
          <a class="nav-link" href="https://github.com/b1th0rn/eg0n">GitHub Project</a>        
        </BCol>
        <BCol class="nav-custom-link">          
          <img alt="" width="24" height="24" :src="telegramLogo">
          <a class="nav-link" href="https://t.me/+a7sF3JQV4bMzY2Nk">Telegram</a>        
        </BCol>
        <BCol class="nav-custom-link">          
          <img alt="" width="24" height="24" src="https://encrypted-tbn2.gstatic.com/favicon-tbn?q=tbn:ANd9GcRv6wsf8x-VM2sEClVU2kf507xgf2fmN2LPyNQ5fzVADeUe3L-e7slT5K_e6qbsiznKPXne_NM0LBPeH95CBBld_hDa00OA0C0AARvkz9Y-v9TKaSk">
          <a class="nav-link" href="https://www.patreon.com/roccosicilia">Support the project</a>        
        </BCol>
      </BRow>
        <!-- <BNavItem href="https://discord.gg/Ys5AAbsyyH">
          <div class="nav-custom-link">
            <img alt="" width="24" height="24" :src="discordLogo">
            <span>Discord Server</span>
          </div>
        </BNavItem>
        <BNavItem href="https://github.com/b1th0rn/eg0n">
          <div class="nav-custom-link">
            <img alt="" width="24" height="24" :src="githubLogo">
            <span>GitHub Project</span>
          </div>
        </BNavItem>
        <BNavItem href="https://t.me/+a7sF3JQV4bMzY2Nk">
          <div class="nav-custom-link">
            <img alt="" width="24" height="24" :src="telegramLogo">
            <span>Telegram</span>
          </div>
        </BNavItem>
        <BNavItem href="https://www.patreon.com/roccosicilia">
          <div class="nav-custom-link">
            <img alt="" width="24" height="24" src="https://encrypted-tbn2.gstatic.com/favicon-tbn?q=tbn:ANd9GcRv6wsf8x-VM2sEClVU2kf507xgf2fmN2LPyNQ5fzVADeUe3L-e7slT5K_e6qbsiznKPXne_NM0LBPeH95CBBld_hDa00OA0C0AARvkz9Y-v9TKaSk">
            <span>Support the project</span>
          </div>
        </BNavItem> -->
    </BNavbar>
  </footer>
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

    discordLogo: {
      get() {
        let baseUri = document.baseURI;
        return new URL("/static/images/Discord-Symbol-White.png", baseUri);
      },
    },

    githubLogo: {
      get() {
        let baseUri = document.baseURI;
        return new URL("/static/images/github-mark-white.png", baseUri);
      },
    },

    telegramLogo: {
      get() {
        let baseUri = document.baseURI;
        return new URL("/static/images/Telegram-Logo.png", baseUri);
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

footer {
  line-height: 1.5;
  max-height: 100vh;
  display: flex;
  place-items: center;
  padding-bottom: 1rem;
  bottom: 0;
  z-index: 999;
  overflow-x: hidden;
}

.footer-nav {
  background-color: black !important;
  color: lightslategray;
}

.footer-row{
  width: 80%;
  margin: 0 auto;
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
  padding: 0 1rem;
}

.nav-custom-link
{
  display: flex;
  align-items: center;

}

.nav-custom-link .material-icons {
  margin-right: 0.5rem;
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

.img-link{
  width: 75px;
  padding: 0;
}

</style>
