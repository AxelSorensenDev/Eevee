<script>
export default {
  data() {
    return {
      modal: { isOpen: false, primaryText: null, secondaryText: null, buttons: [], input: null },
      appendDate: false,
    }
  },
  props: {
    dataName: String,
    fileName: Object,
  },
  methods: {
    addDate() {
      if (this.appendDate) {
        const date = new Date()

        let dateString = ' ('
        dateString += date.toLocaleDateString().replaceAll('.', '-');
        dateString += ' - '
        dateString += date.toLocaleTimeString().replaceAll('.', ':');
        dateString += ')'
        this.modal.time = dateString
        return dateString
      } else {
        this.modal.time = ''
        return ''
      }

    },
    createModal(primaryText, secondaryText, buttons, input, filetype = null) {
      this.modal.primaryText = primaryText;
      this.modal.secondaryText = secondaryText;
      this.modal.buttons = buttons;
      this.modal.isOpen = true;
      this.modal.input = input
      this.modal.input_text = this.fileName.value
      this.modal.filetype = filetype
      this.modal.time = this.appendDate ? this.addDate() : ''
    },
  },

}

</script>

<template>
  <div v-if="modal.isOpen" class="w-full flex justify-center items-center h-screen absolute bg-black bg-opacity-20 z-[1]">
    <div class="bg-white w-[60%] max-w-[400px] rounded-md z-[2]">
      <div class="gap-2 p-4 flex flex-col">
        <p class="font-bold text-gray-700">{{ modal.primaryText }}</p>
        <p class="text-sm text-gray-500  wrap">{{ modal.secondaryText }}</p>
      </div>
      <div v-if="modal.input" class="p-4 pt-0 w-full flex items-center gap-2">
        <input v-model="fileName.value" class="bg-gray-100 outline-none p-2 rounded-sm w-full truncate" type="text"
          placeholder="File name">
        <div v-if="appendDate && modal.filetype == 'conll'"
          class="pointer-events-none rounded-sm whitespace-nowrap text-gray-500 text-xs">{{ addDate() }}
        </div>
        <p class="text-gray-500">.{{ modal.filetype }}</p>

      </div>
      <div v-if="modal.input && modal.filetype == 'conll'" class="px-4 flex gap-2 pb-4">
        <p class="text-xs text-gray-500">Append date and time</p>
        <input type="checkbox" v-model="appendDate" @change="addDate">
      </div>

      <div class="bg-gray-100 rounded-md flex justify-between p-4 w-full">
        <button
          class="bg-white px-4 p-2 rounded-md ring-inset ring-1 text-sm ring-gray-300 font-semibold text-gray-700 hover:bg-gray-100"
          @click="modal.buttons[0]?.action">{{ modal.buttons[0]?.text }}</button>
        <button :class="modal.buttons[1]?.color"
          class="px-4 p-2 rounded-md ring-gray-300 text-white font-semibold text-sm" @click="modal.buttons[1]?.action">{{
            modal.buttons[1]?.text }}</button>
      </div>
    </div>
  </div>
</template>

<style>
/* Your component styles here */
</style>