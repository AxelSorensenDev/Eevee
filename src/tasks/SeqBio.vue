

<template>
  <div v-if="searchBarOpen.value" class=" bg-white z-[1] rounded-md absolute shadow-lg p-4 pb-0" ref="search"
    :style="{ top: position.y + 'px', left: position.x + 'px' }">
    <div class="flex justify-between items-center">

      <p class="text-gray-400 text-xs mb-2" for="">Select a label</p>
      <div class="flex gap-2 items-center">
        <p @click="searchContains.value = false; $refs.search_input.focus()"
          :class="!searchContains.value ? 'bg-purple-400 text-white' : 'hover:bg-gray-100'"
          class="text-gray-400 cursor-pointer  text-xs mb-2 p-1 rounded-md" for="">a..
        </p>
        <p @click="searchContains.value = true; $refs.search_input.focus()"
          :class="searchContains.value ? 'bg-purple-400 text-white' : 'hover:bg-gray-100'"
          class="text-gray-400 cursor-pointer text-xs mb-2 p-1 rounded-md" for="">..a..
        </p>
      </div>
    </div>
    <input @input="listIndex.value = 0" ref="search_input" v-model="search.value" type="text"
      class="w-[87%] outline-none border-b-2 border-purple-500 h-10 mb-4">
    <div class="divide-y flex flex-col h-32 overflow-scroll w-max-[100px]">
      <div @mouseover="listIndex.value = index" v-for="label, index in  filteredLabels "
        class="flex justify-between items-center text-sm p-2 w-[90%] cursor-pointer" @click="addLabel" :ref="index"
        :class="index == listIndex.value ? 'bg-gray-100 font-bold' : null">
        <div class="bg-purple-100 text-xs w-6 rounded-full flex justify-center items-center h-6 mr-2">{{
          label[0].toLowerCase()
        }}
        </div>
        <p class="truncate whitespace-nowrap"> {{
          label }}</p>

      </div>
    </div>
  </div>

  <div class="grid grid-rows-[fit-content] rounded-md mx-auto w-[calc(100vw-250px-64px)]">
    <div class="bg-purple-500 flex justify-between p-2 rounded-t-md min-h-[40px]">
      <div class="flex gap-2 flex-wrap">
        <div v-if="!searchMode" class="rounded-md p-2 px-6 border border-white border-1 font-bold text-center relative"
          :class="index == selectedLabelId.value ? 'bg-white text-purple-500' : 'text-white hover:bg-purple-400 cursor-pointer'"
          v-for="   label, index  in  tasks[selectedTaskId.value]?.labels.sort()   "
          @click="this.selectedLabelId.value = index">
          <p class="absolute text-xs top-0 left-1 p-1">{{ index + 1 }}</p>
          {{ label }}
        </div>


      </div>
      <div v-if="this.tasks[this.selectedTaskId.value]?.labels.length <= 9"
        class="items-center justify-center flex gap-2">
        <div class="group cursor-pointer " @click="searchMode = false">
          <font-awesome-icon class="mr-2 text-lg"
            :class="!searchMode ? 'text-purple-200' : 'group-hover:text-purple-400 text-purple-800'"
            icon="fa-solid fa-rectangle-list" />
        </div>
        <div class="group cursor-pointer" @click="searchMode = true">
          <font-awesome-icon class="mr-2 text-lg"
            :class="searchMode ? 'text-purple-200' : 'group-hover:text-purple-400 text-purple-800'"
            icon="fa-solid fa-search" />
        </div>
      </div>
    </div>
    <div @click.stop="" @mouseup.stop="mouseUp" class="justify-center items-center flex bg-white rounded-b-md ">
      <div v-if="data.length > 0" class="flex justify-center items-center  rounded-b-md gap-2 flex-wrap gap-y-4 m-8">
        <span @mousedown="spanClicked = true" v-for="   word, index    in    data[currentSentenceId.value]?.words   "
          class="relative flex">
          <span
            v-if="word[tasks[selectedTaskId.value].output_index][0] == 'B' && tasks[selectedTaskId.value]?.labels.includes((word[tasks[selectedTaskId.value].output_index]).slice(2))">
            <div @mouseup.stop="" @click.stop="deleteBioLabel(index)"
              class="relative group cursor-pointer w-2 bg-yellow-200 h-full ml-2">
              <font-awesome-icon icon="fa-solid fa-xmark"
                class="text-gray-400 group-hover:bg-gray-300 flex w-2 h-2 p-1 left-[-8px] absolute top-[-8px] bg-gray-200 rounded-full" />
            </div>
          </span>
          <span :id="index"
            @click.stop="tasks[selectedTaskId.value]?.labels.includes((word[tasks[selectedTaskId.value].output_index]).slice(2)) ? changeLabel(index) : null"
            :name="tasks[selectedTaskId.value]?.labels.includes((word[tasks[selectedTaskId.value].output_index]).slice(2)) ? 'selected' : null"
            :class="tasks[selectedTaskId.value]?.labels.includes((word[tasks[selectedTaskId.value].output_index]).slice(2)) ? 'bg-yellow-200 p-1 mx-[-4px]' : (start !== null && end !== null && index >= start && index <= end) ? 'bg-yellow-400 bg-opacity-50 p-1 mx-[-4px] ' : null">
            {{ word[tasks[selectedTaskId.value].input_index] }}</span>
          <span
            @click.stop="tasks[selectedTaskId.value]?.labels.includes((word[tasks[selectedTaskId.value].output_index]).slice(2)) ? changeLabel(index) : null"
            v-if="word[tasks[selectedTaskId.value].output_index][0] == 'I' && data[currentSentenceId.value]?.words[index + 1]?.[tasks[selectedTaskId.value].output_index][0] != 'I' || word[tasks[selectedTaskId.value].output_index][0] == 'B' && data[currentSentenceId.value]?.words[index + 1]?.[tasks[selectedTaskId.value].output_index][0] != 'I' && tasks[selectedTaskId.value]?.labels.includes((word[tasks[selectedTaskId.value].output_index]).slice(2))"
            class="text-xs text-purple-700 font-semibold text-ellipsis bg-yellow-200">
            <p class="p-2 truncate max-w-[20ch]">{{
              word[tasks[selectedTaskId.value].output_index].slice(2) }}
            </p>
          </span>


        </span>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      spanClicked: false,
      position: { x: 0, y: 0 },
      start: null,
      end: null,
      searchMode: this.tasks[this.selectedTaskId.value]?.labels.length > 9,
      changingLabel: false,

    }
  },
  props: {
    data: Array,
    tasks: Array,
    selectedTaskId: Object,
    selectedLabelId: Object,
    currentSentenceId: Object,
    selectedWordId: Object,
    searchBarOpen: Object,
    listIndex: Object,
    searchContains: Object,
    search: Object,
    filteredLabels: Array,
  },
  methods: {
    clickAway(event) {
      const elementToCheck = this.$refs?.search;

      if (!elementToCheck?.contains(event.target)) {
        this.start = null
        this.end = null
        this.search.value = ''
        this.searchBarOpen.value = false

      }


    },

    setBioLabel(start, end, currentSentenceId, label) {
      for (let i = start; i <= end; i++) {
        if (i == start) {
          this.data[currentSentenceId.value].words[i][this.tasks[this.selectedTaskId.value].output_index] = 'B-' + label
          console.log(label)
        } else {
          this.data[currentSentenceId.value].words[i][this.tasks[this.selectedTaskId.value].output_index] = 'I-' + label
        }
      }


    },
    deleteBioLabel(index) {
      this.searchBarOpen.value = false
      this.spanClicked = false
      this.start = null
      this.end = null
      this.data[this.currentSentenceId.value].words[index][this.tasks[this.selectedTaskId.value].output_index] = 'O'
      if (this.data[this.currentSentenceId.value].words.length == 1) {
        return
      }
      if (index != this.data[this.currentSentenceId.value].words.length - 1) {
        index++;
      }

      while (this.data[this.currentSentenceId.value].words[index][this.tasks[this.selectedTaskId.value].output_index][0] != 'O' && this.data[this.currentSentenceId.value].words[index]?.[this.tasks[this.selectedTaskId.value].output_index][0] != 'B') {
        this.data[this.currentSentenceId.value].words[index][this.tasks[this.selectedTaskId.value].output_index] = 'O'
        index++;
      }
      if (index == this.data[this.currentSentenceId.value].words.length - 1 && this.data[this.currentSentenceId.value].words[index]?.[this.tasks[this.selectedTaskId.value].output_index][0] != 'B') {
        this.data[this.currentSentenceId.value].words[index][this.tasks[this.selectedTaskId.value].output_index] = 'O'
      }

    },
    changeLabel(index) {
      this.changingLabel = true
      this.end = index;

      this.start = index;
      while (this.data[this.currentSentenceId.value].words[this.start][this.tasks[this.selectedTaskId.value].output_index][0] != 'O' && this.data[this.currentSentenceId.value].words?.[this.start]?.[this.tasks[this.selectedTaskId.value]?.output_index][0] != 'B' && this.start >= 0) {
        this.start--;
      }
      while (this.data[this.currentSentenceId.value].words[this.end + 1]?.[this.tasks[this.selectedTaskId.value].output_index][0] != 'O' && this.data[this.currentSentenceId.value].words?.[this.end + 1]?.[this.tasks[this.selectedTaskId.value]?.output_index][0] != 'B' && this.end < this.data[this.currentSentenceId.value].words.length - 1) {
        this.end++;
      }

      if (!this.searchMode) {
        this.setBioLabel(Math.min(this.start, this.end), Math.max(this.start, this.end), this.currentSentenceId, this.tasks[this.selectedTaskId.value].labels[this.selectedLabelId.value])
      } else {
        this.searchBarOpen.value = true
        this.$nextTick(() => {

          this.spanClicked = false
          const modal = this.$refs.search;
          const padding = 50
          const modalWidth = modal.offsetWidth + padding;
          const modalHeight = modal.offsetHeight + padding;
          const viewportWidth = window.innerWidth;
          const viewportHeight = window.innerHeight;
          const maxX = viewportWidth - modalWidth;
          const maxY = viewportHeight - modalHeight;

          // Calculate the new position
          const x = Math.min(maxX, event.clientX);
          const y = Math.min(maxY, event.clientY + 30);

          // Update the position
          this.position = { x, y };
          this.$refs.search_input.focus();
        })
      }


    },
    mouseUp(event) {
      if (!this.spanClicked || event.target.attributes?.name?.value == 'selected') {
        return
      }

      this.start = undefined;
      this.end = undefined;
      try {
        this.start = window.getSelection().anchorNode.parentElement.attributes.id.value

        this.end = window.getSelection().extentNode.parentElement.attributes.id.value
      } catch (error) {
        if (this.start && this.end == undefined) {
          this.end = window.getSelection().extentNode.id - 1
        }
      }
      if (!this.searchMode) {
        this.setBioLabel(Math.min(this.start, this.end), Math.max(this.start, this.end), this.currentSentenceId, this.tasks[this.selectedTaskId.value].labels[this.selectedLabelId.value])
        window.getSelection().removeAllRanges()
        return
      }

      this.searchBarOpen.value = true
      this.$nextTick(() => {

        this.spanClicked = false
        const modal = this.$refs.search;
        const padding = 50
        const modalWidth = modal.offsetWidth + padding;
        const modalHeight = modal.offsetHeight + padding;
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        const maxX = viewportWidth - modalWidth;
        const maxY = viewportHeight - modalHeight;

        // Calculate the new position
        const x = Math.min(maxX, event.clientX);
        const y = Math.min(maxY, event.clientY + 30);

        // Update the position
        this.position = { x, y };
        this.$refs.search_input.focus();

      });



    },
    addLabel() {
      if (this.filteredLabels[this.listIndex.value]) {
        if (this.changingLabel) {
          this.setBioLabel(Math.min(this.start, this.end), Math.max(this.start, this.end), this.currentSentenceId, this.filteredLabels[this.listIndex.value])
          this.changingLabel = false;

        } else {
          this.setBioLabel(Math.min(this.start, this.end), Math.max(this.start, this.end), this.currentSentenceId, this.filteredLabels[this.listIndex.value])
        }

        this.search.value = ''
        this.searchBarOpen.value = false
        this.listIndex.value = 0
        this.start = undefined;
        this.end = undefined;
      }

    },
    handleKeyDown(event) {
      if (event.keyCode == 13) {
        if (this.searchMode) {
          if (this.searchBarOpen.value) {
            this.addLabel()
          }

        }



      }
      if (event.keyCode == 27) {
        this.start = null
        this.end = null
        this.search.value = ''
        this.searchBarOpen.value = false
      }

    },

  },

  created() {
    window.addEventListener("click", this.clickAway);
    window.addEventListener("keydown", this.handleKeyDown);

  },
  beforeUnmount() {
    window.removeEventListener("click", this.clickAway);
    window.removeEventListener("keydown", this.handleKeyDown);

  },
}

</script>

<style scoped>
::-moz-selection {
  /* Code for Firefox */
  background: #FDE694
}

::selection {
  background: #FDE694
}
</style>