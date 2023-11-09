

<template>
  <div class="grid grid-rows-[fit-content] rounded-md mx-auto w-[calc(100vw-250px-64px)]">
    <div class="bg-purple-500 flex justify-end p-2 rounded-t-md">
      <div v-if="this.tasks[this.selectedTaskId.value]?.labels.length <= 9"
        class="items-center justify-center flex gap-2">
        <div class="group cursor-pointer " @click="searchMode = false; searchBarOpen.value = false">
          <font-awesome-icon class="mr-2 text-lg"
            :class="!searchMode ? 'text-purple-200' : 'group-hover:text-purple-400 text-purple-800'"
            icon="fa-solid fa-rectangle-list" />
        </div>
        <div class="group cursor-pointer" @click="searchMode = true;">
          <font-awesome-icon class="mr-2 text-lg"
            :class="searchMode ? 'text-purple-200' : 'group-hover:text-purple-400 text-purple-800'"
            icon="fa-solid fa-search" />
        </div>
      </div>
    </div>
    <div :class="!searchMode ? 'rounded-b-md' : null" class="justify-center items-center flex bg-white flex-col">
      <div v-if="data.length > 0" class="flex justify-center items-end  rounded-b-md gap-1 flex-wrap gap-y-4 m-8">
        <span v-for="word in data[currentSentenceId.value]?.words" class="text-center">
          {{ word[tasks[selectedTaskId.value].input_index] }}
        </span>
      </div>

      <div v-if="!searchMode" class="flex flex-wrap gap-4 w-full p-4">
        <div
          class="rounded-md p-2 px-6 ring-purple-500 ring-2 font-bold text-center text-purple-500 relative select-none flex-grow"
          :class="tasks[selectedTaskId.value].labels[index] == data[currentSentenceId.value]?.strings.find(string => string.name == tasks[selectedTaskId.value].output_index).string ? 'bg-purple-500 text-white' : ' hover:bg-purple-100 cursor-pointer'"
          @click="data[currentSentenceId.value].strings.find(string => string.name == tasks[selectedTaskId.value].output_index).string = tasks[selectedTaskId.value].labels[index]"
          v-for="label, index in tasks[selectedTaskId.value]?.labels.sort()">
          <p class="absolute text-xs top-0 left-1 p-1">{{ index + 1 }}</p>
          {{ label }}
        </div>

      </div>
    </div>
    <div v-if="searchMode" class="px-6 bg-white">
      <div
        :class="(tasks[selectedTaskId.value].labels.includes(data[currentSentenceId.value].strings.find(string => string.name
          ==
          tasks[selectedTaskId.value].output_index).string)) && !inputFocused ? 'bg-purple-500 text-white' : 'bg-white text-purple-500 ring-purple-500 ring-2'"
        class="rounded-md p-2 px-6 font-bold text-center relative select-none max-w-[400px] mx-auto truncate">
        {{ tasks[selectedTaskId.value].labels.includes(data[currentSentenceId.value].strings.find(string => string.name
          ==
          tasks[selectedTaskId.value].output_index).string) ?

          data[currentSentenceId.value].strings.find(string => string.name ==
            tasks[selectedTaskId.value].output_index).string : '?' }}
      </div>
    </div>
    <div v-if="searchMode" ref="search_container" class="justify-center flex-col">
      <div class=" bg-white z-[1] rounded-b-md p-4" ref="search">
        <div class="flex justify-between items-center relative">

          <p class="text-gray-400 text-xs mb-2 mx-auto" for="">Search for label</p>


        </div>
        <div class="max-w-[400px] mx-auto">
          <div class="flex gap-4 items-center relative">
            <div v-if="!inputFocused" class="group cursor-pointer absolute" @click="searchMode = true;">
              <font-awesome-icon class="pb-3 text-purple-300" icon=" fa-solid fa-search" />
            </div>
            <input @focus="inputFocused = true; searchBarOpen.value = true" @input="listIndex.value = 0"
              ref="search_input" v-model="search.value" type="text"
              class="w-full outline-none border-b-2 border-purple-500 h-10 mb-4">
            <div v-if="inputFocused" class="flex gap-2 items-center">
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
          <div v-if="inputFocused" class="divide-y flex flex-col h-32 overflow-scroll w-full">
            <div @mouseover="listIndex.value = index" v-for="label, index in  filteredLabels "
              class="flex justify-between items-center text-sm p-2 w-full cursor-pointer"
              @click="$nextTick(() => { data[currentSentenceId.value].strings.find(string => string.name == tasks[selectedTaskId.value].output_index).string = filteredLabels[index]; search.value = '' }); inputFocused = false; this.searchBarOpen.value = false"
              :ref="index" :class="index == listIndex.value ? 'bg-gray-100 font-bold' : null">
              <div class="bg-purple-100 text-xs w-6 rounded-full flex justify-center items-center h-6">{{
                label[0].toLowerCase()
              }}
              </div>
              {{
                label }}
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      searchMode: this.tasks[this.selectedTaskId.value]?.labels.length > 9,
      inputFocused: false,
    }
  },
  props: {
    data: Array,
    tasks: Array,
    selectedTaskId: Object,
    selectedLabelId: Object,
    currentSentenceId: Object,
    listIndex: Object,
    searchBarOpen: Object,
    searchContains: Object,
    search: Object,
    filteredLabels: Array,

  },
  methods: {
    clickAway(event) {
      const elementToCheck = this.$refs?.search_container;

      if (!elementToCheck?.contains(event.target)) {
        this.start = null
        this.end = null
        this.search.value = ''
        this.inputFocused = false
        this.searchBarOpen.value = false

      }


    },
    handleKeyDown(event) {
      if (event.keyCode == 13 && this.searchMode) {
        if (this.filteredLabels[this.listIndex.value]) {
          this.data[this.currentSentenceId.value].strings.find(string => string.name == this.tasks[this.selectedTaskId.value].output_index).string = this.filteredLabels[this.listIndex.value]
        }
        this.search.value = ''
        this.$refs.search_input.blur()
        this.inputFocused = false
        this.searchBarOpen.value = false

      }
      if (event.keyCode == 27) {
        this.search.value = ''
        this.$refs.search_input.blur()
        this.inputFocused = false;
        this.searchBarOpen.value = false;
      }

      if (event.keyCode == 9) {
        event.preventDefault();

        this.$refs.search_input.focus()
      }

    }
  },
  created() {
    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("click", this.clickAway);



  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("click", this.clickAway);

  },
}
</script>

<style>
/* Your component styles here */
</style>