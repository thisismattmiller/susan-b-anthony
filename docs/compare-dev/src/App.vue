<script>


export default {
  components: {

  },
  data() {
    return {  

      compareData: {},
      doYear: '1893',

      cityOrState:false,
      fullText:true,
      geographicalLocations:false,
      people:false,
      summaryText:true,
      dateFormated: true,
    }
  },
  computed: {
    
  },


  methods: {


  },

  async mounted(){

    console.log('sss')


    let r = await fetch('/susan-b-anthony/json/compare.json')
    this.compareData = await r.json()

    console.log(this.compareData)

    // this.daybookSelected = this.index.daybooks[this.randomBook].date



  }

}


</script>

<template>
  
  <div id="app">
  <header>
     
     <button @click="doYear=year" v-for="year in Object.keys(compareData)">
      <span v-if="doYear == year">✓</span>{{year}}
     </button> 
     <div>
       
<label for="cityOrState">Written From</label><input id="cityOrState" type="checkbox" v-model="cityOrState">
<label for="fullText">Extracted Text</label><input id="fullText" type="checkbox" v-model="fullText">
<label for="geographicalLocations">Locations Mentioned</label><input id="geographicalLocations" type="checkbox" v-model="geographicalLocations">
<label for="people">People Mentioned</label><input id="people" type="checkbox" v-model="people">
<label for="summaryText">Summary</label><input id="summaryText" type="checkbox" v-model="summaryText">
<label for="dateFormated">Extracted Date</label><input id="dateFormated" type="checkbox" v-model="dateFormated">



     </div>

  </header>
  <main>

    <template v-for="file in compareData[doYear]">
      <a target="_blank" :href="`https://www.loc.gov/resource/${file.digital_id}/?sp=${file.page}&st=text`">{{`https://www.loc.gov/resource/${file.digital_id}/?sp=${file.page}`}}</a>
      <table>

        <thead>
          <tr>
            <td>GPT3</td>
            <td>GPT3.5</td>
            <td>GPT4</td>
          </tr>
        </thead>
        
        <tr v-for="(x,idx) in [...Array(file.most_entries)].map((_, i) => i * file.most_entries)" >

          <template v-for="gpt in ['3','3.5','4']">
            <td>
              <template v-if="file[gpt][idx] !== false">
                
                <div v-if="dateFormated">{{file[gpt][idx].dateFormated}}</div>

                <div v-if="cityOrState">....</div>
                <div v-if="cityOrState">{{file[gpt][idx].cityOrState}}</div>

                <div v-if="fullText">....</div>                
                <div v-if="fullText">{{file[gpt][idx].fullText}}</div>

                <div v-if="geographicalLocations">....</div>
                <div v-if="geographicalLocations">{{file[gpt][idx].geographicalLocations}}</div>
                
                <div v-if="people">....</div>
                <div v-if="people">{{file[gpt][idx].people}}</div>

                <div v-if="summaryText">....</div>                
                <div v-if="summaryText">{{file[gpt][idx].summaryText}}</div>


              </template>
              <template v-else>
                <span>---</span>
              </template>

            </td>
          </template>

        </tr>



      </table>
    </template>


  </main>



  </div>

</template>

<style scoped>

label{
  margin-left: 2em;
  margin-right: 1em;
}
table{
    border-collapse: collapse;
  border: 1px solid;
  width:100%;
}

  tr:hover {
    background-color: #ff57223b;
  }

  td{
    min-width: 5em;
    width: 33%;
  }

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {




}
</style>
