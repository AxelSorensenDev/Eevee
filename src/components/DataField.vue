<template>
  <div class="bg-gray-200 w-[calc(100vw-250px)] flex flex-col ">
    <div v-if="data.length == 0" class="flex flex-col h-full justify-center items-center p-4 px-20 gap-2">

      <div
        class="cursor-pointer border-2 border-gray-400 text-gray-500 p-4 rounded-md border-dashed  hover:bg-gray-300 text-center w-full"
        @click="$emit('readFile', 'conll')">Import "Conll-like" file</div>
      <p class="text-xs text-gray-500 font-bold">- OR -</p>
      <div
        class="cursor-pointer border-2 border-gray-400 text-gray-500 p-4 rounded-md border-dashed hover:bg-gray-300 text-center w-full"
        @click="$emit('readFile', 'txt')">Import txt file (Sentences seperated by new line character)</div>

    </div>
    <div v-if="data.length > 0" class="p-2 bg-purple-200 w-full text-xs text-gray-700 flex gap-2">File: {{ dataName
    }}

      <div
        @click="refs.myModal.createModal('Remove data', `Are you sure you want to remove the imported data?`, [{ text: 'Cancel', action: () => refs.myModal.modal.isOpen = false }, { text: 'Remove', action: () => { $emit('clearData', index); refs.myModal.modal.isOpen = false }, color: 'bg-red-600 hover:bg-red-700' }])"
        class="group cursor-pointer"><font-awesome-icon class="text-gray-600 group-hover:text-red-500"
          icon="fa-solid fa-trash-can" /></div>

    </div>
    <div v-if="data.length > 0" class="overflow-scroll" ref="scrollToMe">
      <table v-if="!showStrings.value" class="bg-white w-full text-center text-sm">
        <thead class="bg-purple-500 text-white top-0 sticky">
          <tr class="text-center divide-x divide-purple-700">
            <th class="font-normal whitespace-nowrap" :class="index == 0 ? ' w-10' : null"
              v-for="item, index in data[0].words[0]">
              <div class="flex justify-between gap-2 items-center px-2">
                <p class="">{{ index }}</p>
                <div
                  @click="refs.myModal.createModal('Delete column', `Are you sure you want to delete column at index: ${index} ?`, [{ text: 'Cancel', action: () => refs.myModal.modal.isOpen = false }, { text: 'Delete', action: () => { $emit('deleteColumn', index); refs.myModal.modal.isOpen = false }, color: 'bg-red-600 hover:bg-red-700' }])"
                  class="group cursor-pointer"><font-awesome-icon class="text-purple-800 group-hover:text-purple-300"
                    icon="fa-solid fa-xmark" /></div>
              </div>
            </th>

          </tr>
        </thead>

        <tbody class="divide-y">
          <template v-for="row in data.slice(currentSentenceId.value, currentSentenceId.value + 1)">
            <tr class="divide-x" v-for="item in row.words ">
              <td v-for="item, index in item" class="p-2">
                <p>{{ item }}</p>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      <table v-else class="w-full text-center text-sm">
        <thead class="bg-purple-500 text-white top-0 sticky">
          <tr class="text-center divide-x divide-purple-700">
            <th class="font-normal whitespace-nowrap w-[2px] px-2">Idx</th>
            <th class="font-normal whitespace-nowrap w-[82px]">Name</th>
            <th class="font-normal whitespace-nowrap">String</th>
            <th class="font-normal whitespace-nowrap"><font-awesome-icon icon="fa-solid fa-trash-can"
                class="text-purple-400" /></th>
          </tr>
        </thead>
        <tbody class="divide-y">

          <tr v-for="string, index in      data[currentSentenceId.value]?.strings     " class="bg-white divide-x">
            <td class="bg-white text-left p-2 whitespace-nowrap text-center">{{ index }}
            </td>
            <td class=" text-left p-2 ">
              <div class="flex items-center">
                <input ref="input" class="outline-none pointer-events-none" type="text" :value="string.name"
                  @change="event => { $emit('updateRowName', [index, event.target.value]); event.target.blur() }">
                <div class="group cursor-pointer" @click="this.$refs.input[index].select();">
                  <font-awesome-icon class="text-gray-400 group-hover:text-gray-600" icon="fa-solid fa-pencil" />
                </div>
              </div>
            </td>
            <td class="bg-white text-left p-2">
              {{ string.string }}
            </td>
            <td
              @click="refs.myModal.createModal('Delete row', `Are you sure you want to delete row at index: ${index} ?`, [{ text: 'Cancel', action: () => refs.myModal.modal.isOpen = false }, { text: 'Delete', action: () => { $emit('deleteRow', index); refs.myModal.modal.isOpen = false }, color: 'bg-red-600' }])"
              class="p-2 cursor-pointer group w-2"><font-awesome-icon icon="fa-solid fa-xmark"
                class="text-gray-400 group-hover:text-red-500" /></td>
          </tr>
        </tbody>
      </table>


    </div>
  </div>
</template>



<script>
export default {
  props: {
    data: Array,
    showStrings: Object,
    currentSentenceId: Object,
    refs: Object,
    newRowIndex: Number,
    tasks: Array,
    dataName: String,
  }

}
</script>
