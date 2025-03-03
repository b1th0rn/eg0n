<template>
  <BContainer>
    <h1>Top Contributors</h1>
    <p>This page showcases the top contributors, authors, and reviewers. Here, you can find the most active and impactful members of our community.</p>
    <p>If you are interested in joining our community, please visit the home page where you can find detailed instructions and contact information. We look forward to welcoming you!</p>
    <BRow class="my-1">
      <BCol cols="6" class="podium-container">
        <h4>Top IOC Authors</h4>
          <Podium  
            :first="firstAuthor"
            :second="secondAuthor"
            :third="thirdAuthor" />
      </BCol>
      <BCol cols="6" class="podium-container">
        <h4>Top IOC Reviewer</h4>
          <Podium  
            :first="firstReviewer"
            :second="secondReviewer"
            :third="thirdReviewer" />
      </BCol>
    </BRow>    
      <BRow class="my-3">        
        <BCol class="podium-container">
          <h4>Top Contributors</h4>
            <Podium  
              :first="firstContributor"
              :second="secondContributor"
              :third="thirdContributor" />
        </BCol>      
    </BRow>    
  </BContainer>
</template>

<script>
import Podium from "@/components/Podium.vue";
import { eg0nApiService } from "@/utils/eg0nApiServices";

export default {
  name: "ScoreboardView",
  data() {
    return {
      scoreBoard: {},
    };
  },

  components: {
    Podium,
  },

  created() {
    this.fetchScoreBoard();
  },

  methods: {
    async fetchScoreBoard() {
      try {
        let response = await eg0nApiService.GetScoreBoard();
        this.scoreBoard = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
  computed: {
    firstAuthor() {
      if(this.scoreBoard.top_authors){
        return this.scoreBoard.top_authors.author1;
      }
    return "";
    },

    secondAuthor() {
      if(this.scoreBoard.top_authors){
        return this.scoreBoard.top_authors.author2;
      }
    return "";
    },
    thirdAuthor() {
      if(this.scoreBoard.top_authors){
        return this.scoreBoard.top_authors.author3;
      }
    return "";
    },

    firstReviewer() {
      if(this.scoreBoard.top_reviewers){
        return this.scoreBoard.top_reviewers.reviewer1;
      }
    return "";
    }, 

    secondReviewer() {
      if(this.scoreBoard.top_reviewers){
        return this.scoreBoard.top_reviewers.reviewer2;
      }
    return "";
    },

    thirdReviewer() {
      if(this.scoreBoard.top_reviewers){
        return this.scoreBoard.top_reviewers.reviewer3;
      }
    return "";
    },

    firstContributor() {
      if(this.scoreBoard.top_contributors){
        return this.scoreBoard.top_contributors.contributor1;
      }
    return "";
    },

    secondContributor() {
      if(this.scoreBoard.top_contributors){
        return this.scoreBoard.top_contributors.contributor2;
      }
    return "";
    },

    thirdContributor() {
      if(this.scoreBoard.top_contributors){
        return this.scoreBoard.top_contributors.contributor3;
      }
    return "";
    },
  }
};
</script>

<style scoped>
.podium-container {
  text-align: center;
}

@media (max-width: 768px) { /* Adjust breakpoint as needed */
    .podium-container {
      width: 100%; /* Occupy full width */
      margin-bottom: 1rem; /* Add some spacing between containers */
    }
    .col-6{
        width: 100%;
    }
  }
</style>

