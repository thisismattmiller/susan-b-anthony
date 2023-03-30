<script>
  import { VueFinalModal } from 'vue-final-modal'
  import VueDragResize from 'vue3-drag-resize'

  let randomArray = (length, max) => [...new Array(length)]
      .map(() => Math.round(Math.random() * max));

  export default {
    components: {
      VueFinalModal,
      VueDragResize,
    },
    props:{

      allIndex: Object,

    },

    data() {
      return {
        width: (window.innerWidth>700) ? 700 : window.innerWidth - 20,
        height: 0,
        top: 100,



        activeCat: 'daybook',

        show: false,

        initalHeight: 400,
        left: (window.innerWidth>700) ? 50 : 0,

        similarFullText:'',

        similarParsed: {
          daybook:[...new Array(100)].map(()=>{return ''}),
          correspondence:[...new Array(100)].map(()=>{return ''}),
          writings: [...new Array(100)].map(()=>{return ''})

        },
        similar:[...new Array(100)].map(()=>{return ''}),
        displaySimilar:[...new Array(100)].map(()=>{return ''})



      }
    },
    computed: {




    },

    watch: {
      // // whenever question changes, this function will run
      // showPrefModal(newVal, oldVal) {
        

      //   // if (newVal === true){
      //   //   this.loadPrefGroup()
      //   // }
      // },

      // similar(newVal,oldVal){
      //   console.log("Change")
      //   if (this.left <0){
      //     this.left=0
      //   }

      //   // }
      //   // this.loadSimilar()


      // }

    },

    methods: {
        

        load: function(entrySimilar,source,sourceText){
          console.log(entrySimilar,source,sourceText)

          if (this.left <0){
            this.left=0
          }
          // this.similarParsed.daybook= randomArray(100,10000)
          this.$refs.preferenceContent.style.height = this.initalHeight + 'px'

          this.similarFullText=sourceText
          console.log("LOAD ",entrySimilar)
          this.similar = entrySimilar
          this.loadSimilar()
          this.activeCat = source
        },

        dragResize: function(newRect){

          this.width = newRect.width
          this.height = newRect.height
          this.top = newRect.top
          this.left = newRect.left

          this.$refs.preferenceContent.style.height = newRect.height + 'px'

        },
        cleanText: function(text){

            return text.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");



        },

        
        onSelectElement (event) {
          const tagName = event.target.tagName

          if (tagName === 'INPUT' || tagName === 'BUTTON' || tagName === 'TEXTAREA' || tagName === 'SELECT') {
            event.stopPropagation()
          }
        },


        async loadSimilar(){

          if (!this.activeCat){
            this.activeCat=this.loadFirst
          }

          console.log(this.similar)
          //daybooks

          let daybook =[]

          for (let d of this.similar.daybook){
            let filename = `/susan-b-anthony/json/daybooks/daybooks_${d[1][1]}_${d[1][2]}.json`

            let response = await fetch(filename)
            let data = await response.json()

            daybook.push({
              id: `${data.digital_id}_${data.file_id}_${data.entry_id}`,
              meta:data.dateFormated + ' - ' + parseFloat(d[0]).toFixed(2) * 100 + '%',
              text: this.cleanText(data.fullText),
              link: [
                {
                  label:'view',
                  url: `https://www.loc.gov/resource/${data.digital_id}/?sp=${data.file_id}&st=text`
                }
              ]

            })


          }

          let correspondence = []          
          let response = await fetch('/susan-b-anthony/json/correspondences.json')
          let data = await response.json()
          console.log(data)

          for (let c of this.similar.correspondence){

            for (let letter of data.letters){
              if (c[1][1] == letter.digital_id && c[1][2] == letter.index[1]){

                correspondence.push({
                  id: `${letter.digital_id}_${letter.index[1]}`,
                  meta: `${letter.sender} -> ${letter.recipient} - ${letter.dateFormated}` + ' - ' + parseFloat(c[0]).toFixed(2) * 100 + '%',
                  text: letter.summerized4Sentences || letter.summarized4Sentences || letter.summery4Sentences,
                  link: letter.pages.map((p,idx) =>{

                    return {
                      label:`page ${idx+1}`,
                      url: `https://www.loc.gov/resource/${letter.digital_id}/?sp=${p}&st=text`
                    }

                  })

                })
              }
            }
 
          }


          let writing =[]

          for (let w of this.similar.writings){

            // console.log('w',w[1][1])

            for (let key in this.allIndex.writingsToDigitalId){

              if (this.allIndex.writingsToDigitalId[key] == w[1][1]){

                let response = await fetch('/susan-b-anthony/json/'+key)
                let data = await response.json()

                for (let b of data.blocks){
                  if (b.pages == w[1][2]){

                    writing.push({
                      id: `${data.digital_id}_${b.pages}`,
                      meta:  data.title.replace('Susan B. Anthony Papers: Speeches and Writings, 1848-1895;','') + ' - ' + parseFloat(w[0]).toFixed(2) * 100 + '%',
                      text: b.text,
                      link: b.pages.split('_').map((p,idx) =>{

                        return {
                          label:`page ${idx+1}`,
                          url: `https://www.loc.gov/resource/${data.digital_id}/?sp=${p}&st=text`
                        }

                      })

                    })


                  }
                }

              }

            }




          }







          // this.similarParsed.correspondence = correspondence

          this.similarParsed.correspondence = correspondence.concat([...new Array(20-correspondence.length)].map(()=>{return ''}));

          this.similarParsed.daybook = daybook.concat([...new Array(20-daybook.length)].map(()=>{return ''}));

          this.similarParsed.writing = writing.concat([...new Array(20-writing.length)].map(()=>{return ''}));



          this.displaySimilar = this.similarParsed[this.activeCat]


        },

        switchCat: function(cat){

          console.log(this.displaySimilar.length, this.similarParsed[cat].length)

          this.displaySimilar = this.similarParsed[cat]
          console.log(this.displaySimilar)

          // if (cat === 'daybook'){
          //   this.displaySimilar = this.similarParsed.daybook
          // }if (cat === 'correspondence'){
          //   this.displaySimilar = this.similarParsed.correspondence
          // }
          
          console.log(cat)
          // this.activeCat=cat

          
        },

        closeModal(){

          this.$emit('confirm')


        }

    

    },

     mounted()  {



      // await this.loadSimilar()
    }
  }



</script>

<template>


    <VueFinalModal
      :display-directive="'if'"
      :v-model="show"
      :lock-scroll="false"
      :hide-overlay="true"
      background="interactive"
    >


        <VueDragResize
          
          :is-active="true"
          :w="width"
          :h="initalHeight"
          :y="top"
          :x="left"
          class="dark:bg-stone-900 bg-stone-100 shadow-xl"
          @resizing="dragResize"
          @dragging="dragResize"
          :sticks="['br']"
          :stickSize="22"
        >
          <div id="preference-content" class="p-4"  ref="preferenceContent" @mousedown="onSelectElement($event)" @touchstart="onSelectElement($event)">


            <div class="grid grid-cols-1 sm:grid-cols-4 pt-1">

              <div class="col-span-1 pt-1 text-center text-lg">
                <!-- <span class="text-sm" v-if="activeCat=='daybook'">&check;&nbsp;</span> -->
                <a href="#" v-on:click.prevent.stop="switchCat('daybook'); activeCat='daybook'" :class="['underline', 'hover:bg-sky-200', 'dark:hover:text-slate-800', 'rounded-lg', {'bg-sky-200 text-slate-800':(activeCat=='daybook')}]">Daybooks</a>
              </div>

              <div class="col-span-1 pt-1 text-center text-lg">
                <!-- <span class="text-sm" v-if="activeCat=='correspondence'">&check;&nbsp;</span> -->
                <a href="#" v-on:click.prevent.stop="switchCat('correspondence'); activeCat='correspondence'" :class="['underline', 'hover:bg-sky-200', 'dark:hover:text-slate-800', 'rounded-lg', {'bg-sky-200  text-slate-800':(activeCat=='correspondence')}]">Correspondence</a>
              </div>
              <div class="col-span-1 pt-1 text-center text-lg">
                <!-- <span class="text-sm" v-if="activeCat=='writing'">&check;&nbsp;</span> -->
                <a href="#" v-on:click.prevent.stop="switchCat('writing'); activeCat='writing'" :class="['underline', 'hover:bg-sky-200', 'dark:hover:text-slate-800', 'rounded-lg', {'bg-sky-200  text-slate-800':(activeCat=='writing')}]">Writings</a>
              </div>
              <div class="col-span-1">

                <button class="ml-auto p-1  border rounded-lg float-right" @click="closeModal">
                  Close
                </button>


              </div>



            </div>

            <!-- {{similar}} -->

            <div class="pl-4 pr-4 pt-4 text-sm" >
              <details class="cursor-pointer">
                {{similarFullText}}
                <summary>Show source text</summary>
              </details>
            </div>
            
            <table class="table-auto border-collapse">
              <tr v-for="aS in displaySimilar" class="dark:even:bg-stone-800 even:bg-white" >

                  <td>
                    <div class="pt-4">{{aS.meta}}</div>
                    <div class="pb-4 text-sm">{{aS.text}}</div>
                  </td>
                  <td>
                    <template v-for="l in aS.link">
                      <a class="text-sm block hover:underline" style="white-space: nowrap" target="_blank" :href="l.url">{{l.label}}</a>
                    </template>
                  </td>

 

              </tr>
<!--               <tr v-for="t in test" class="" >
     
                <td>{{t}}</td>

              </tr> -->
            </table>



          </div>


        </VueDragResize>
    </VueFinalModal>




</template>

<style scoped>

  h3{
    margin-bottom: 2em;
  }

  .checkbox-option{
    width: 20px;
    height: 20px;
  }

  .option{
    display: flex;
  }
  .option-title{
    flex:2;
  }
  .option-title-header{
    font-weight: bold;
  }
  .option-title-desc{
    font-size: 0.8em;
    color:gray;
  }
  #preference-content{
    overflow: hidden;
    overflow-y: auto;
  }
  .close-button{
    position: absolute;
    right: 5px;
    top: 5px;
    background-color: white;
    border-radius: 5px;
    border: solid 1px black;
    cursor: pointer;
  }
/*  .preference-modal{
    background-color: white;
    -webkit-box-shadow: 0px 10px 13px -7px #000000, 5px 5px 15px 5px rgba(0,0,0,0.27); 
    box-shadow: 0px 10px 13px -7px #000000, 5px 5px 15px 5px rgba(0,0,0,0.27);
    border-radius: 1em;
    padding:1em;
    border: solid 1px black;
  }*/


</style>
