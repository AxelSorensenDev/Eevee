<template>
  <div>
    <div v-if="data.length != 0" class="w-full p-4 flex justify-between bg-gray-200">
      <div class="flex cursor-pointer">
        <p @click="showStrings.value = !showStrings.value"
          :class="{ 'bg-purple-200 pointer-events-none ring-1 ring-purple-300': !showStrings.value, 'bg-white hover:bg-gray-100 ring-1 ring-gray-300': showStrings.value }"
          class="rounded-l-md p-1 text-sm px-4">Token</p>
        <p @click="showStrings.value = !showStrings.value"
          :class="{ 'bg-purple-200 pointer-events-none ring-1 ring-purple-300': showStrings.value, 'bg-white hover:bg-gray-100 ring-1 ring-gray-300': !showStrings.value }"
          class=" p-1 text-sm px-4 rounded-r-md">Sentence</p>
      </div>
      <div class="flex items-center gap-4 justify-between select-none">
        <div
          :class="{ 'text-gray-500 hover:text-gray-700': currentSentenceId.value > 0, 'text-gray-300 pointer-events-none': currentSentenceId.value == 0 }"
          class="cursor-pointer group p-2 m-[-8px]" @click="$emit('prevSentence')">
          <font-awesome-icon icon="fa-solid fa-chevron-left" class="" />
        </div>
        <p v-if="!searchingSentence.value" @click="searchingSentence.value = true; $nextTick(() => {
          $refs.sentenceSearch.focus()
        })" class="flex">{{ currentSentenceId.value + 1 }} / {{ data.length }}</p>
        <input @keydown.enter="event => $emit('searchSentence', event)" @blur="event => $emit('searchSentence', event)"
          ref="sentenceSearch" class="w-16 rounded-md outline-none bg-gray-300 text-center"
          @change="event => $emit('searchSentence', event)" v-if="searchingSentence.value" type="text">
        <div class="cursor-pointer group p-2 m-[-8px]"
          :class="{ 'text-gray-500 hover:text-gray-700': currentSentenceId.value < data.length - 1, 'text-gray-300 pointer-events-none': currentSentenceId.value == data.length - 1 }"
          @click="$emit('nextSentence')">
          <font-awesome-icon icon="fa-solid fa-chevron-right" />

        </div>
      </div>
      <div @click="showStrings.value ? $emit('addRow') : $emit('addColumn')"
        class="flex items-center group cursor-pointer p-2 m-[-8px] gap-2 hover:bg-gray-300 rounded-md">
        <p v-if="!showStrings.value" class="text-sm">Add column</p>
        <p v-else class="text-sm">Add row</p>
        <font-awesome-icon class="text-purple-800" icon="fa-solid fa-plus" />
      </div>
    </div>
  </div>
</template>

<script>
export default {

  props: {
    data: Array,
    showStrings: Boolean,
    currentSentenceId: Object,
    searchingSentence: Object,
  }
}
</script>
