<script>

import RelatedModal from "@/components/RelatedModal.vue";
import { useToast } from "vue-toastification";
import { BounceLoader } from "vue3-spinner";
import { Vue3ToggleButton } from 'vue3-toggle-button'
import '../node_modules/vue3-toggle-button/dist/style.css'
import { ModalsContainer } from 'vue-final-modal'

export default {
  components: {
      RelatedModal,
      BounceLoader,
      Vue3ToggleButton,
      ModalsContainer
  },
  data() {
    return {

      show: false,
      index: {},
      book:{},
      bookOrg:{},
      textSearchOpen: false,
      textSearchOpenTimer: null,
      textSearchLoading:false,
      showMLFields: false,
      activeFacet: false,
      activeFacetValue: false,

      sumLevel: 1,

      randomBook: Math.floor(Math.random() * 24),
      daybookSelected: null,
      loading: true,
      expand: {},
      activeSimilar: {
        daybook:[],
        correspondence:[],
        writings:[]
      },


    }
  },
  computed: {
    // other computed properties


    // showLocalPreferenceModal: {
    //   get() {
    //     return this.showPrefModal
    //   },
    //   set() {
    //     this.preferenceStore.togglePrefModal()     
    //   }
    // }

    
  },


  methods: {

    showSimilar(similar,source,sourceText){
        this.$nextTick(() => {
            this.show = true
            this.$nextTick(() => {
                // this.activeSimilar=similar

                
                this.$refs.modal.load(similar,source,sourceText)
            })
        })
        // 
    },

    removeFacet(){

        this.book = JSON.parse(JSON.stringify(this.bookOrg))
        this.activeFacet=false
        this.activeFacetValue=false

    },

    applyFacet(key,name){

        console.log(key,name)
        this.bookOrg = JSON.parse(JSON.stringify(this.book))

        if (key === 'all_recipients'){
            this.book.letters = this.book.letters.filter((v) => { if (!v.recipient){return false} return (v.recipient == name)})
        }else if (key === 'all_senders'){
            this.book.letters = this.book.letters.filter((v) => { if(!v.sender){return false} return v.sender == name} ) 
        }else if (key === 'sent_from'){
            this.book.letters = this.book.letters.filter((v) => { if(!v.sentFrom){return false} return v.sentFrom == name} ) 

        }else if (key === 'people'){
            this.book.letters = this.book.letters.filter((v) => { if(!v.peopleMentioned){return false} return v.peopleMentioned.includes(name)} ) 
        }

        this.activeFacet = true
        this.activeFacetValue = `${key}::${name}`

    },


    textSearchMouseMove(){
        window.clearTimeout(this.textSearchOpenTimer)
    },
    textSearchMouseOut(){
    
       if (this.textSearchLoading){return false}
       this.textSearchOpenTimer = window.setTimeout(()=>{
        this.textSearchOpen = false
       },1000)

    },

    dateToNum(dateVal){
      
      console.log(dateVal.split('-'))
      if (!dateVal){
        return 0
      }

      let val =  parseInt(dateVal.split('-')[0]) + parseInt(dateVal.split('-')[1]) + parseInt(dateVal.split('-')[2])

      console.log(dateVal,val)

      return val

    },

    async loadIndex(){

      this.loading=true
      let r = await fetch('/susan-b-anthony/json/index.json')
      this.index = await r.json()
      this.loading=false

      this.loadBook()




    },

    async loadBook(){

      this.loading=true
      // await new Promise(r => setTimeout(r, 2000));
      this.activeFacet=false
      this.activeFacetValue=false
      let r = await fetch('/susan-b-anthony/json/correspondences.json')
      this.book = await r.json()
      this.loading=false



      for (let l of this.book.letters){
        if (l.dateFormated){
          l.dateFormatted = l.dateFormated
        }else{
          l.dateFormated = l.dateFormatted
        }
        l.dateNum = this.dateToNum(l.dateFormated)
        console.log("HHHHHH",l,l.dateFormatted,l.dateNum)

      }

      this.book.letters.sort((a, b) => Number(b.pages[0]) - Number(a.pages[0]))
      console.log(this.book.letters)
      // this.$nextTick(() => {
      //     // for (let el of document.getElementsByClassName('text-search')){
      //     //   console.log(el)
      //     //   el.addEventListener('mouseup', (event) => {  
      //     //       if(window.getSelection().toString().length){
      //     //          let exactText = window.getSelection().toString();  
      //     //          console.log(exactText)      
      //     //       }   
      //     //   })


      //     // }
      // })






    },

    cleanFacetName (facet){

      facet = facet.replace('all_recipients','From')
      facet = facet.replace('people','People')
      facet = facet.replace('locations','Locations')



      return facet
    },




    expandEntry(event,letter){


      let id = `${letter.digital_id}_${letter.index[1]}`

      let svgDom = document.getElementById(id)

      if (svgDom.classList.contains('-rotate-90') && event.target.tagName === 'path'){

        svgDom.classList.remove('-rotate-90')
        delete this.expand[id]

      }else{
        svgDom.classList.add('-rotate-90')
        this.expand[id]=true

        document.getElementById(id+'_td').classList.remove('hover:cursor-pointer')

      }
      console.log(event,letter)

    },

    cleanText: function(text){

      return text.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");



    },

    searchSimilarDyanmic: async function(){
        let exactText = window.getSelection().toString(); 
        this.textSearchLoading = true
        window.clearTimeout(this.textSearchOpenTimer)

        let qResult = await fetch('https://3h4c0tgq09.execute-api.us-east-1.amazonaws.com/prod/sba-gpt?' + new URLSearchParams({
            q: exactText             
        }))

        qResult= await qResult.json()
        console.log("DONE")
        this.textSearchLoading = false
        this.textSearchOpen = false



        this.showSimilar(qResult,'correspondence',exactText)

    }

   


 
  },

  watch:{



    // showMLFields(newVal, oldVal){

    //     if (newVal===true){


    //         for (let el of document.querySelectorAll("*")){

    //             if (el.dataset && el.dataset.ml && el.dataset.ml == 'extracted'){
    //                 el.classList.add('dark:bg-fuchsia-600')
    //             }
    //             if (el.dataset && el.dataset.ml && el.dataset.ml == 'summarized'){
    //                 el.classList.add('dark:bg-amber-600')
    //             }

    //         }

    //     }else{



    //     }


    // }


  },

  mounted() {


    this.loadIndex()


    // window.setTimeout(()=>{

    //   this.show=true


      console.log(useToast)

      
    // },1000)



      this.$nextTick(() => {
        
        console.log(this.randomBook)
        let toast = useToast()
        toast.info("Notice: Information on this page has been created through automated machine learning processes. Always check the source documents for each statement to verify accuracy. ", {
            position: "bottom-center",
            timeout: 20000,
            closeOnClick: true,
            pauseOnFocusLoss: true,
            pauseOnHover: true,
            draggable: true,
            draggablePercent: 0.6,
            showCloseButtonOnHover: false,
            hideProgressBar: false,
            closeButton: "button",
            icon: true,
            rtl: false


        });


        document.addEventListener('mouseup', (event) => {  
            if(window.getSelection().toString().length){
               let exactText = window.getSelection().toString(); 
               // console.log(this.$refs.textSearchModal.style.top)
               this.textSearchOpen = true

               this.$nextTick(() => {

                   this.textSearchOpenTimer = window.setTimeout(()=>{
                    this.textSearchOpen = false
                   },2000)
                   if (this.$refs.textSearchModal){
                    this.$refs.textSearchModal.style.left = event.pageX + 'px'
                    this.$refs.textSearchModal.style.top = event.pageY + 'px'    
                    }

                })

            }
        })       


        // document.addEventListener('mousedown', (event) => {  

        //     this.textSearchOpen = false
        // }) 


      })



    // this.$toast("I'm a toast!", {
    //   position: "top-right",
    //   timeout: 5000,
    //   closeOnClick: true,
    //   pauseOnFocusLoss: true,
    //   pauseOnHover: true,
    //   draggable: true,
    //   draggablePercent: 0.6,
    //   showCloseButtonOnHover: false,
    //   hideProgressBar: true,
    //   closeButton: "button",
    //   icon: true,
    //   rtl: false
    // });




  }
}




</script>

<template>



<div class="grid grid-cols-1 sm:grid-cols-10">


    <Teleport to="body">
        <div ref="textSearchModal" @mouseout="textSearchMouseOut()" @mousemove="textSearchMouseMove()" v-if="textSearchOpen" class="p-3 absolute rounded border-2 shadow-2xl dark:border-0 text-slate-700 bg-slate-200" id="text-search-modal">
        

        <template v-if="textSearchLoading">

              <BounceLoader
                :loading="true"
                :color="'#1f96f3'"
                :size="'50px'" />

            
        </template>
        <template v-else>
            <button @click="searchSimilarDyanmic" class="mr-6 hover:bg-sky-200">Search Similar Text</button>
            <button @click="textSearchOpen = false" class="hover:bg-sky-200">X</button>

        </template>
        </div>
    </Teleport>


  <div class="col-span-2">
    <div class="">

      <div v-if="activeFacet===false">
            
          <template v-for="(facet,key) in book.facets">

            <details>
                

                <summary class="cursor-pointer" v-if="key=='all_recipients'">Facet by Recipient</summary>
                <summary class="cursor-pointer" v-if="key=='all_senders'">Facet by Sender</summary>
                <summary class="cursor-pointer" v-if="key=='people'">Facet by People Mentioned</summary>
                <summary class="cursor-pointer" v-if="key=='sent_from'">Facet by Sent From</summary>

                <div class="pr-1" style="max-height: 400px; overflow-y: scroll; overflow-x: hidden;">
                    {{cleanFacetName(key)}}
                  <ul>

                      <li v-for="name in Object.keys(facet).sort()">
                      <div v-on:click.prevent.stop="applyFacet(key,name)" class="relative text-sm pl-2 hover:pl-4 hover:bg-sky-200 dark:hover:bg-sky-600 hover:cursor-pointer">
                        <a href="#" v-on:click.prevent.stop="applyFacet(key,name)">
                        <span class="">{{name}}</span>
                        <span class="absolute right-0">{{facet[name]}}</span>
                        </a>
                      </div>
                    </li>

                  </ul>
                </div>
            </details>
          </template>


      </div>
      <div v-else>
        <button @click="removeFacet()" class="bg-blue-200 mt-4 mb-4 text-sm hover:bg-blue-700 hover:text-white text-slate-600 font-bold py-2 px-2 rounded-full">Remove Facet {{activeFacetValue}}</button>
      </div>

      <div class="mt-2">
        <label >Summarization Level:</label><br>
        <input type="range" name="sumLevel" v-model="sumLevel" max="4" min="1"><br>
        <span>{{sumLevel}} sentences</span>
      </div>

    </div>
  </div>
  <div class="col-span-8">
    <div v-if="loading" class="m-auto">
      <BounceLoader
        :loading="loading"
        :color="'#1f96f3'"
        :size="'120px'" />
    </div>

    <div class="p-2">


      <div class="grid grid-cols-1 sm:grid-cols-10">
        <div class="col-span-8 pb-2 pr-2">
            <div class="mt-0 mb-2 text-2xl font-medium leading-tight">Susan B. Anthony - Correspondence</div>
            <div class="text-sm">Below is extracted data from Susan B. Anthony’s correspondence, a <a href="https://crowd.loc.gov/campaigns/susan-b-anthony-papers/anthony-correspondence/" style="text-decoration:underline;">collection housed at the Library of Congress</a>. Click the summarized text or the triangle in each entry to expand to see more data and functionality. This blog post describes how and why this data was created.</div>

        </div>

        <div class="col-span-2" style="text-align: right;">
                <span class="text-sm">Highlight ML Fields:</span>
                <Vue3ToggleButton v-model:isActive="showMLFields" :handleColor="'#e080e0'" :handleDiameter="'20px'" :trackHeight="'20px'"> </Vue3ToggleButton>
                <template v-if="showMLFields">
                    <div><span style="width:15px; height: 15px; display: inline-block;" class="bg-violet-300 dark:bg-violet-700"></span>=Extracted by GPT 3.5</div>
                    <div><span style="width:15px; height: 15px; display: inline-block;" class="dark:bg-amber-700 bg-amber-300"></span>=Summarized by GPT 3.5</div>
                </template>

        </div>
      </div>
      <hr>

      <table class="table-auto border-collapse">
        <thead>
          <tr>
            <th>Date</th>
            <th>Sender</th>
            <th>Recipient</th>
            <th>Summary</th>
          </tr>
        </thead>

        <tbody>
          <template v-for="(letter,index) in book.letters">

            <!-- <template v-if="activeFacet && "></template> -->

            <tr :class="['', { 'dark:bg-stone-750' : (index%2===0), 'bg-neutral-100 dark:bg-stone-900': (index%2==1)  }]">
              <td class="p-2" style="min-width: 8rem;">
                <span :class="['block',{'dark:bg-violet-700':showMLFields, 'bg-violet-300': showMLFields}]">{{letter.dateFormated}}</span>
              </td>  
              <td class="p-2" style="min-width: 8rem;">
                <span :class="['block',{'dark:bg-violet-700':showMLFields, 'bg-violet-300': showMLFields}]">{{letter.sender}}</span>
                <span :class="['block text-sm',{'dark:bg-violet-700':showMLFields, 'bg-violet-300': showMLFields}]">{{letter.sentFrom}}</span>
              </td>  
              <td class="p-2" style="min-width: 8rem;">
                <span :class="['block',{'dark:bg-violet-700':showMLFields, 'bg-violet-300': showMLFields}]">{{letter.recipient}}</span>
              </td>  
               <td class="p-2 pt-4 pb-4 hover:cursor-pointer" :id="`${letter.digital_id}_${letter.index[1]}_td`" v-on:click="expandEntry($event,letter)">
                
                <span data-ml="summarized" :class="['text-search',{'dark:bg-amber-700':showMLFields, 'bg-amber-300':showMLFields}]">
                 <template v-if="sumLevel==1">{{letter.summarized1Sentence||letter.summarized1Sentences||letter.summerized1Sentences||letter.summerized1Sentence||letter.summery1Sentences}}</template> 
                 <template v-if="sumLevel==2">{{letter.summarized2Sentence||letter.summarized2Sentences||letter.summerized2Sentences||letter.summerized2Sentence||letter.summery2Sentences}}</template> 
                 <template v-if="sumLevel==3">{{letter.summarized3Sentence||letter.summarized3Sentences||letter.summerized3Sentences||letter.summerized3Sentence||letter.summery3Sentences}}</template> 
                 <template v-if="sumLevel==4">{{letter.summarized4Sentence||letter.summarized4Sentences||letter.summerized4Sentences||letter.summerized4Sentence||letter.summery4Sentences}}</template> 


<!--                  <template v-if="sumLevel==2">{{letter.summarized2Sentences}}</template> 
                 <template v-if="sumLevel==3">{{letter.summarized3Sentences}}</template> 
                 <template v-if="sumLevel==4">{{letter.summarized4Sentences}}</template> 
 -->



                </span>
                
              </td> 
              <td class="">
                <a href="#" v-on:click.prevent.stop="expandEntry($event,letter)">
                  <svg width="25px" height="25px" class="transition duration-250 ease-in-out" :id="`${letter.digital_id}_${letter.index[1]}`" version="1.1" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                   <path class="fill-slate-300 hover:fill-sky-400" d="m68.965 98.367-45.84-44.254c-1.1211-1.082-1.7539-2.5703-1.7539-4.1289 0-1.5547 0.63281-3.043 1.7539-4.125l45.84-44.246c1.6562-1.5781 4.0938-2.0195 6.1953-1.125 2.1055 0.89453 3.4766 2.9531 3.4922 5.2422v88.52c-0.015625 2.2891-1.3867 4.3477-3.4922 5.2422-2.1016 0.89453-4.5391 0.45312-6.1953-1.125z"/>
                  </svg>
                </a>              
              </td> 


            </tr>

            <tr :class="['', { 'dark:bg-stone-750' : (index%2===0), 'bg-neutral-100 dark:bg-stone-900': (index%2==1)  }]">
              <td colspan=5>
                <Transition>
                  <div class="pt-4 grid grid-cols-4 gap-1" v-if="expand[`${letter.digital_id}_${letter.index[1]}`]">
                      

                    <div class="col-span-1 text-center">
                        
                        <a class="m-auto block" :href="`https://www.loc.gov/resource/${letter.digital_id}/?sp=${letter.pages[0]}&st=text`" target="_blank">
                          <img :src="`https://crowd-media.loc.gov/susan-b-anthony-papers/anthony-correspondence/mss11049001/${letter.pages[0]}.jpg`" style="min-height: 215px;"/>
                        </a>


<button v-if="letter.similar" @click="showSimilar(letter.similar,'correspondence','text of letter')" class="bg-blue-200 mt-4 mb-4 text-sm hover:bg-blue-700 hover:text-white text-slate-600   font-bold py-2 px-2 rounded-full">
  View Similar Text
</button>


                    </div>
                    <div class="p-1 col-span-3">

                      <div class="grid grid-cols-2 pt-4">
                        <div class="col-span-2">
                          <span data-ml="extracted">People</span>
                          <ul class="list-disc pl-4">
                            <li v-for="p in letter.peopleMentioned.filter((v)=>{return (v.trim()!=='')})"><span :class="[{'dark:bg-violet-700':showMLFields, 'bg-violet-300': showMLFields}]">{{p}}</span></li>
                            <li class="italic" v-if="letter.peopleMentioned.filter((v)=>{return (v.trim()!=='')}).length==0">None</li>
                          </ul>
                        </div>

                      </div>
                    </div>

                  </div>
                </Transition>

              </td>

            </tr>



          </template>


        </tbody>
      </table>







    </div>

  </div>

<RelatedModal ref="modal" v-model="show" :allIndex="index" @confirm="() => {show=false}"/>

<ModalsContainer/>

</div>



<!-- 

     -->






</template>




<style>

body {
  @apply dark:bg-stone-800 dark:text-slate-300 p-2;
}
/*
#text-search-modal{
    position: absolute;
}
*/
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

.v-leave-to {
  transition: opacity 100ms ease;
}

textarea{
  border: none;
  width: 100%;
  height: 5em;
    border: none;
    overflow: auto;
    outline: none;

    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;

    resize: none; /*remove the resize handle on the bottom right*/
    font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
    Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
    font-size: 1.5em;
    padding: 5px;
} 

.mention-item {
  padding: 4px 10px;
  border-radius: 4px;
}

.mention-selected {
  background: rgb(192, 250, 153);
}

.one-half{
  padding: 1rem;
}

.ask-button{
  display: inline-block;
  outline: none;
  cursor: pointer;
  font-weight: 500;
  border-radius: 3px;
  padding: 0 16px;
  border-radius: 4px;
  color: #fff;
  background: #6200ee;
  line-height: 1.15;
  font-size: 14px;
  height: 36px;
  word-spacing: 0px;
  letter-spacing: .0892857143em;
  text-decoration: none;
  text-transform: uppercase;
  min-width: 64px;
  border: none;
  text-align: center;
  box-shadow: 0px 3px 1px -2px rgb(0 0 0 / 20%), 0px 2px 2px 0px rgb(0 0 0 / 14%), 0px 1px 5px 0px rgb(0 0 0 / 12%);
  transition: box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1);              
}
.ask-button:hover {
      background: rgb(98, 0, 238);
      box-shadow: 0px 2px 4px -1px rgb(0 0 0 / 20%), 0px 4px 5px 0px rgb(0 0 0 / 14%), 0px 1px 10px 0px rgb(0 0 0 / 12%);
}
.ask-button:active {
  transform: translateY(4px);
}
</style>
