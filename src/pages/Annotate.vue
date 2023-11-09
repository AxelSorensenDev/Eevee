<script>
import Class from '../tasks/Class.vue';
import Seq from '../tasks/Seq.vue';
import SeqBio from '../tasks/SeqBio.vue';
import Seq2Seq from '../tasks/Seq2Seq.vue';
export default {
  data() {
    return {
      time: null,
      listIndex: { value: 0 },
      flag: false,
      timer_start: new Date(),
      timer_stop: null,
      searchMode: false,
      searchContains: { value: false },
      search: { value: '' }
    }
  },
  props: {
    page: String,
    data: Array,
    tasks: Array,
    selectedTaskId: Object,
    selectedLabelId: Object,
    currentSentenceId: Object,
    selectedWordId: Object,
    searchingSentence: Object,
    searchBarOpen: Object,
  },
  methods: {
    jumpToProgress() {
      for (let i = 0; i < this.data.length - 1; i++) {
        const status = JSON.parse(this.data[i].strings.find(string => string.name == '# status').string)[this.selectedTaskId.value.toString()]
        console.log(status)
        if (status != 'accepted') {
          this.currentSentenceId.value = i
          return
        }
      }


    },
    setStatus(value) {
      let new_val = JSON.parse(this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string)
      new_val[this.selectedTaskId.value] = value
      this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string = JSON.stringify(new_val)
      if (this.currentSentenceId.value == this.data.length - 1) {
        this.timer_stop = new Date()
        try {
          let time = parseInt(this.data[oldVal?.value].strings.find(string => string.name == '# time (ms)').string)
          time += this.timer_stop - this.timer_start
          this.data[oldVal?.value].strings.find(string => string.name == '# time (ms)').string = time.toString()
        } catch (error) {

        }
      }
      if (value != '_' && this.currentSentenceId.value != this.data.length - 1) {
        window.removeEventListener('keydown', this.handleKeyDown);
        setTimeout(() => {
          if (this.selectedTaskId.value < this.tasks.length - 1) {
            this.selectedTaskId.value++
          } else {
            if (this.currentSentenceId.value != this.data.length - 1) {
              this.selectedTaskId.value = 0
              this.currentSentenceId.value++
            }

          }

          window.addEventListener('keydown', this.handleKeyDown);
        }, 200);
      }

    },
    handleKeyDown(event) {

      if (event.keyCode == 32 && this.currentSentenceId.value < this.data.length) {
        if (!this.searchBarOpen.value) {
          this.setStatus('accepted')
        }

      }

      // Do something
      if (event.keyCode == 39 && this.currentSentenceId.value < this.data.length) {
        this.$emit('nextSentence')
      }

      if (event.keyCode == 37 && this.currentSentenceId.value > 0) {
        this.$emit('prevSentence')
      }



      if (event.keyCode == 38) {
        if (this.searchBarOpen.value) {
          if (this.listIndex.value > 0) {
            this.listIndex.value--
            this.$refs?.span?.$refs?.[(this.listIndex.value).toString()][0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
            this.$refs?.class?.$refs?.[(this.listIndex.value).toString()][0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
            this.$refs?.seq?.$refs?.[(this.listIndex.value).toString()][0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });

          }
        } else if (this.selectedTaskId.value > 0) {
          this.selectedLabelId.value = 0;
          this.selectedTaskId.value--
        }

      }

      if (event.keyCode == 40) {
        if (this.searchBarOpen.value) {
          if (this.listIndex.value < this.filteredLabels.length - 1) {
            this.listIndex.value++
            this.$refs?.span?.$refs?.[(this.listIndex.value).toString()][0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
            this.$refs?.class?.$refs?.[(this.listIndex.value).toString()][0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
            this.$refs?.seq?.$refs?.[(this.listIndex.value).toString()][0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });



          }
        } else if (this.selectedTaskId.value < this.tasks.length - 1) {
          this.selectedLabelId.value = 0;
          this.selectedTaskId.value++
        }

      }

      if (0 < parseInt(event.key) && parseInt(event.key) < this.tasks[this.selectedTaskId.value]?.labels.length + 1 && !this.searchMode.value) {
        this.selectedLabelId.value = event.key - 1;
        if (!this.tasks[this.selectedTaskId.value].type.isWordLevel) {
          this.data[this.currentSentenceId.value].strings.find(string => string.name == this.tasks[this.selectedTaskId.value].output_index).string = this.tasks[this.selectedTaskId.value].labels[event.key - 1]
        }
      }


    },
  },

  watch: {
    lastSentId: {
      handler(newVal, oldVal) {  // here having access to the new and old value
        // do stuff
        this.timer_stop = new Date()


        try {
          let time = parseInt(this.data[oldVal?.value].strings.find(string => string.name == '# time (ms)').string)
          time += this.timer_stop - this.timer_start
          this.data[oldVal?.value].strings.find(string => string.name == '# time (ms)').string = time.toString()
        } catch (error) {
          console.log(error)
        }
        this.timer_start = new Date()

      },
      deep: true,
    }
  },
  computed: {

    lastSentId() {
      return Object.assign({}, this.currentSentenceId)
    },
    filteredLabels() {
      if (!this.searchContains.value) {
        return this.tasks[this.selectedTaskId.value].labels.filter(label => label.toLowerCase().startsWith(this.search.value.toLowerCase()))
      }
      return this.tasks[this.selectedTaskId.value].labels.filter(label => label.toLowerCase().includes(this.search.value.toLowerCase()))

    }
  },
  created() {
    // this.timer = setInterval(() => {
    //   alert("Remember to export the annotation file continuously so you don't risk loosing your progress")
    // }, 600000)
    window.addEventListener("keydown", this.handleKeyDown);


  },
  beforeUnmount() {
    clearInterval(this.timer);
    window.removeEventListener('keydown', this.handleKeyDown);

  },
  components: { Seq, Class, SeqBio, Seq2Seq }
}
</script>

<template>
  <div class="grid grid-rows-[fit-content(20px),1fr,200px] items-center bg-gray-200 h-screen justify-between">
    <div class="flex gap-8 p-4 px-8 items-center">
      <div class="flex gap-2 flex-1 items-center">
        <p class="text-xs text-gray-400">Progress:</p>
        <div class="bg-gray-300 overflow-hidden rounded-full flex-1 h-4 flex">
          <div @click="this.currentSentenceId.value = index"
            :class="index == currentSentenceId.value ? 'bg-white' : JSON.parse(this.data[index].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'accepted' ? 'bg-green-400' : JSON.parse(this.data[index].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'rejected' ? 'bg-red-400' : JSON.parse(this.data[index].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'unsure' ? 'bg-yellow-400' : null"
            v-for="(item, index) in  data" class="flex-grow bg-gray-300">
          </div>


        </div>
        <div @click="jumpToProgress" class="text-xs text-gray-600 rounded-md px-2 p-1 hover:bg-gray-300 cursor-pointer">
          <font-awesome-icon icon="fa-solid fa-angles-right" class="" size="lg" />

        </div>
      </div>

    </div>
    <div class="flex flex-col gap-6 w-[calc(100vw-250px)] overflow-hidden">
      <div class="border-4 m-auto rounded-xl"
        :class="JSON.parse(this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'accepted' ? 'border-green-400 border-4 rounded-sm' : JSON.parse(this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'rejected' ? 'border-red-400 border-4 rounded-sm' : JSON.parse(this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'unsure' ? 'border-yellow-400 border-4 rounded-sm' : null">
        <Seq ref="seq" v-if="tasks[selectedTaskId.value]?.type.name == 'seq'" :data="data" :tasks="tasks"
          :selectedLabelId="selectedLabelId" :selectedTaskId="selectedTaskId" :selectedWordId="selectedWordId"
          :currentSentenceId="currentSentenceId" :searchBarOpen="searchBarOpen" :listIndex="listIndex"
          :searchMode="searchMode" :search="search" :searchContains="searchContains" :filteredLabels="filteredLabels" />
        <SeqBio v-if="tasks[selectedTaskId.value]?.type.name == 'span'" ref="span" :data="data" :tasks="tasks"
          :listIndex="listIndex" :selectedLabelId="selectedLabelId" :selectedTaskId="selectedTaskId"
          :selectedWordId="selectedWordId" :currentSentenceId="currentSentenceId" :searchBarOpen="searchBarOpen"
          :searchMode="searchMode" :search="search" :searchContains="searchContains" :filteredLabels="filteredLabels" />
        <Class ref="class" v-if="tasks[selectedTaskId.value]?.type.name == 'class'" :data="data" :tasks="tasks"
          :selectedLabelId="selectedLabelId" :selectedTaskId="selectedTaskId" :currentSentenceId="currentSentenceId"
          :searchMode="searchMode" :listIndex="listIndex" :searchBarOpen="searchBarOpen" :search="search"
          :searchContains="searchContains" :filteredLabels="filteredLabels" />
        <Seq2Seq v-if="tasks[selectedTaskId.value]?.type.name == 'seq2seq'" :data="data" :tasks="tasks"
          :selectedLabelId="selectedLabelId" :selectedTaskId="selectedTaskId" :currentSentenceId="currentSentenceId" />

      </div>
    </div>
    <div class="flex flex-col justify-center gap-4 bg-white p-4 rounded-md m-auto">
      <div class="flex justify-center gap-4 bg-gray-100 p-2 rounded-md select-none">
        <div
          :class="{ 'text-gray-500 hover:text-gray-700': currentSentenceId.value > 0, 'text-gray-300 pointer-events-none': currentSentenceId.value == 0 }"
          class="cursor-pointer group p-2 m-[-8px]" @click="$emit('prevSentence')">
          <font-awesome-icon icon="fa-solid fa-chevron-left" class="" />
        </div>
        <p v-if="!searchingSentence.value" @click="searchingSentence.value = true; $nextTick(() => {
          $refs.sentenceSearch.focus()
        })" class="flex">{{
  currentSentenceId.value + 1 }} / {{
    data.length }}</p>
        <input @keydown.enter="event => $emit('searchSentence', event)" @blur="event => $emit('searchSentence', event)"
          ref="sentenceSearch" class="w-16 rounded-md outline-none bg-gray-300 text-center"
          @change="event => $emit('searchSentence', event)" v-if="searchingSentence.value" type="text">
        <div class="cursor-pointer group p-2 m-[-8px]"
          :class="{ 'text-gray-500 hover:text-gray-700': currentSentenceId.value < data.length - 1, 'text-gray-300 pointer-events-none': currentSentenceId.value == data.length - 1 }"
          @click="$emit('nextSentence')">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />
        </div>
      </div>
      <div class="flex gap-4 justify-between">
        <div @click="setStatus('accepted')">
          <font-awesome-icon title="Correct" icon="fa-solid fa-check"
            class="bg-green-400 p-4 rounded-md hover:bg-green-300 cursor-pointer text-green-900"
            :class="{ 'ring ring-offset-2 ring-green-400 hover:bg-green-400': JSON.parse(this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'accepted' }" />
        </div>
        <div @click="setStatus('rejected')">
          <font-awesome-icon title="Wrong" icon="fa-solid fa-xmark"
            class="bg-red-400 p-4 rounded-md hover:bg-red-300 cursor-pointer text-red-900"
            :class="{ 'ring ring-offset-2 ring-red-400 hover:bg-red-400': JSON.parse(this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string)[selectedTaskId.value.toString()] == 'rejected' }" />
        </div>
        <div @click="setStatus('unsure')">
          <font-awesome-icon title="Unsure" icon="fa-solid fa-question"
            class="bg-yellow-400 p-4 rounded-md hover:bg-yellow-300 cursor-pointer text-yellow-900"
            :class="{ 'ring ring-offset-2 ring-yellow-400 hover:bg-yellow-400': this.data[this.currentSentenceId.value].strings.find(string => string.name == '# status').string == 'unsure' }" />
        </div>
        <div @click="setStatus('_')">
          <font-awesome-icon title="Clear" icon="fa-solid fa-ban"
            class="bg-gray-100 p-4 rounded-md hover:bg-gray-200 cursor-pointer text-gray-600" />
        </div>

      </div>

    </div>

  </div>
</template>