<template>
  <BContainer class="podium">            
    <div class="podium-box">
      <span>{{SecondPlace}}</span>
      <div class="podium-item second">
        <h2>2st</h2>          
      </div>      
    </div>
    <div class="podium-box">      
      <span>{{FirstPlace}}</span>
      <div class="podium-item first">
        <h2>1st</h2>
        <span class="material-icons">workspace_premium_24</span>          
        <!-- <span class="material-icons">medal</span> -->
      </div>
      
    </div>  
    <div class="podium-box">
      <span>{{ThirdPlace}}</span>
      <div class="podium-item third">
        <h2>3st</h2>          
      </div>
    </div>  
   </BContainer>
</template>
<script>

export default {
  name: "Podium",
  props:  {
    first: String,
    second: String,
    third: String,
  },

  computed: {
    FirstPlace: function() {
      return this.first;
    },

    SecondPlace: function() {
      return this.second;
    },

    ThirdPlace: function() {
      return this.third;
    }
  }
}
</script>
<style scoped>
.podium {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin-top: 20px;
}

.podium-box {
  align-content: center;
  align-items: center;
  text-align: center;
  width: 120px;
}

.podium-item {
  text-align: center;
  align-content: center;
  margin: 0 10px;
  padding: 10px;
  border: 1px solid gray;
  border-radius: 5px;
  width: 100px;
  color: var(--bs-body-bg); /* Change font color to black for better visibility */
}
.podium-item .material-icons {
  font-size: 50px;
  width: 50px;
  height: 50px;
  color: var(--bs-body-bg); /* Change font color to black for better visibility */
}

.first {
  background-color: gold;
  height: 150px;
}

.second {
  background-color: silver;
  height: 110px;
}

.third {
  background-color: #cd7f32; /* Bronze color */
  height: 70px;
}
</style>