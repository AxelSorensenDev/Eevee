<script>
export default {
  data() {
    return {
      emptyValue: null,
    }
  },
  props: {
    tasks: Array,
    selectedTaskId: Number,
    rows: Array,
    columns: Array,
    label: Object,
    data: Array,
    taskTypes: Array,
    showStrings: Object,
  },
  methods: {
    setValue() {
      if (this.tasks[this.selectedTaskId.value].type.isWordLevel) {
        this.data.map(data => data.words.map(word => ([
          word[this.tasks[this.selectedTaskId.value].output_index] = this.emptyValue
        ])));
      } else {
        this.data.map(data => data.strings.find(string => string.name == this.tasks[this.selectedTaskId.value].output_index
        ).string = this.emptyValue);
      }
    },
    setDefaultValue() {
      let values = []
      this.data.map(data => {
        data.words.map(word => {
          values.push(word[this.tasks[this.selectedTaskId.value].output_index])

        })
      })
      values = new Set(values)
      if (values.size < 2) {
        this.setValue()

      } else {
        this.$parent.$refs.myModal.createModal('Set default value', `Column ${this.tasks[this.selectedTaskId.value].output_index} already contains annotations (${values.size} unique values). Are you sure you want to overwrite them?`, [{ text: 'Cancel', action: () => this.$parent.$refs.myModal.modal.isOpen = false }, { text: 'Set value', action: () => { this.setValue(); this.$parent.$refs.myModal.modal.isOpen = false }, color: 'bg-purple-500 hover:bg-purple-600' }])

      }
    }

  },
  computed: {
    inputInRange() {
      return this.tasks[this.selectedTaskId.value].input_index > this.data[0]?.words[0]?.length - 1 || this.tasks[this.selectedTaskId.value].input_index < 0
    },
    outputInRange() {
      if (this.tasks[this.selectedTaskId.value].type.isWordLevel) {
        return this.tasks[this.selectedTaskId.value].output_index > this.data[0]?.words[0]?.length - 1 || this.tasks[this.selectedTaskId.value].output_index < 0
      } else {
        return (!(this.data[0]?.strings.some(string => string.name === this.tasks[this.selectedTaskId.value].output_index)) && this.tasks[this.selectedTaskId.value].output_index)
      }

    },
    importLabels() {
      const labels = []
      this.data.map(data => {
        data.words.map(word => {
          if (word[this.tasks[this.selectedTaskId.value].output_index] != '_' && word[this.tasks[this.selectedTaskId.value].output_index] != undefined) {

            if (this.tasks[this.selectedTaskId.value].type.name == 'span') {
              const label = word[this.tasks[this.selectedTaskId.value].output_index].split('|')
              let bio_labels = []
              label.map(l => {
                if (l != 'O') {
                  bio_labels.push(l.slice(2))
                }

              })
              labels.push(...bio_labels)
            } else {
              const label = word[this.tasks[this.selectedTaskId.value].output_index].split('|')
              labels.push(...label)
            }

          }
        })
      })
      if (this.tasks[this.selectedTaskId.value].output_index != '') {
        this.tasks[this.selectedTaskId.value].labels.push(...new Set(labels))
      }

    }
  },
  // Your JavaScript logic here
}
</script>

<template>
  <div class="grid-rows-[40px,1fr] px-10">
    <div class="divide-y pb-2" v-if="tasks.length > 0">

      <div class="h-6"></div>
      <div class="text-center flex justify-center items-center">
        <input ref="title" @change="e => e.target.blur()" v-model="tasks[selectedTaskId.value].title"
          @click="this.$refs.title.select();" class="text-center outline-none p-4" type="text">
        <div class="group right-10 cursor-pointer p-2 absolute" @click="this.$refs.title.select();"><font-awesome-icon
            class="text-gray-400 group-hover:text-gray-600" icon="fa-solid fa-pencil" /></div>
      </div>
      <div class="divide-y flex flex-col">
        <div class="flex flex-col py-4">
          <label class="text-center text-sm font-semibold text-gray-500 mb-2" for="">Task type</label>

          <div class="flex justify-center">
            <p @click="tasks[selectedTaskId.value].type = task_type; showStrings.value = !tasks[selectedTaskId.value].type.isWordLevel; tasks[selectedTaskId.value].output_index = ''; emptyValue = ''"
              v-for="task_type in    taskTypes   "
              :class="tasks[selectedTaskId.value]?.type.name == task_type.name ? 'bg-purple-200 pointer-events-none ring-1 ring-purple-300' : 'bg-white hover:bg-gray-100 ring-gray-300'"
              class=" p-1 text-sm px-4 cursor-pointer ring-1">{{ task_type.name }}</p>
          </div>
        </div>
        <div class="flex gap-16 justify-center">
          <div class="flex flex-col py-4">
            <label class="text-center justify-center text-sm font-semibold flex text-gray-500 mb-2" for="">
              Input text
            </label>


            <div class="flex gap-2 text-sm justify-evenly w-full">
              <div class="flex gap-2 items-center relative">
                <label class="flex">
                  <p v-if="!tasks[selectedTaskId.value].input_index" class="text-red-500 pr-1">
                    *</p>Column index:
                </label>
                <input @input="" v-model="tasks[selectedTaskId.value].input_index" :class="inputInRange ? 'text-red-500'
                  : null" class="bg-gray-100 outline-none w-10 p-2 rounded-sm text-center" type="text" placeholder="0">
              </div>

            </div>
            <p v-if="inputInRange" class="text-xs text-red-500 mt-2">Out
              of range</p>
          </div>
          <div class="flex flex-col py-4">
            <div class="flex justify-center">
              <label class="text-center text-sm font-semibold text-gray-500 mb-2 flex" for="">Output
              </label>
            </div>
            <div class="flex gap-2 text-sm justify-evenly w-full">
              <div class="flex gap-2 items-center relative">
                <label class="flex">
                  <p v-if="!tasks[selectedTaskId.value].output_index" class="text-red-500 pr-1">
                    *</p>{{ this.tasks[selectedTaskId.value].type.isWordLevel ? 'Column index:' : 'Name:' }}
                </label>
                <input v-if="this.tasks[selectedTaskId.value].type.isWordLevel"
                  v-model="tasks[selectedTaskId.value].output_index" :class="outputInRange ? 'text-red-500' : null"
                  class="bg-gray-100 outline-none w-10 p-2 rounded-sm text-center" type="text" placeholder="0">
                <input v-else v-model="tasks[selectedTaskId.value].output_index"
                  class="bg-gray-100 outline-none w-24 p-2 rounded-sm" :class="outputInRange ? 'text-red-500' : null"
                  type="text" placeholder="# something">

              </div>

            </div>
            <p v-if="outputInRange && tasks[selectedTaskId.value].type.isWordLevel" class="text-xs text-red-500 mt-2">
              Out
              of range
            </p>
            <p v-if="outputInRange && !tasks[selectedTaskId.value].type.isWordLevel" class="text-xs text-red-500 mt-2">
              Name doesn't exist</p>
          </div>
          <div class="flex flex-col py-4">
            <div class="flex relative justify-center">
              <label class=" relative text-center text-sm font-semibold text-gray-500 mb-2" for="">Default label</label>

            </div>
            <div class="flex gap-2 text-sm justify-evenly w-full">
              <div class="flex gap-2 items-center relative">
                <label>Value:</label>
                <input v-model="emptyValue" class="bg-gray-100 outline-none w-10 p-2 rounded-sm text-center" type="text"
                  :placeholder="tasks[selectedTaskId.value].type.name == 'span' ? 'O' : '_'">
                <div @click="setDefaultValue"
                  class="text-sm bg-gray-200 text-gray-500 p-2 rounded-sm hover:bg-gray-300 cursor-pointer whitespace-nowrap"
                  :class="{ 'opacity-50 pointer-events-none': !emptyValue }">
                  Set label</div>
              </div>


            </div>
            <p v-if="tasks[selectedTaskId.value].type.name == 'span'" class="text-xs text-gray-500 mt-2 w-[20ch]">
              *Should be 'O' for span</p>
          </div>
        </div>
        <div>
          <div v-if="tasks[selectedTaskId.value].type.name != 'seq2seq'" class=" flex flex-col py-4">
            <label class="text-center text-sm font-semibold text-gray-500 mb-2 flex justify-center" for="">
              Labels
            </label>
            <div class="flex items-center gap-4">
              <div class="flex w-full">
                <p v-if="tasks[selectedTaskId.value].labels.length == 0" class="text-red-500 pr-1">
                  *</p>
                <input v-model="label.text" class="bg-gray-100 outline-none w-full rounded-sm p-2 text-sm"
                  @keydown.enter="$emit('addLabel')" placeholder="Comma separated labels (Press ENTER to add)"
                  type="text">
              </div>
              <div class="flex gap-2">
                <div @click="$emit('addLabel')"
                  class="text-sm text-gray-500 bg-gray-200 p-2 rounded-sm hover:bg-gray-300 cursor-pointer whitespace-nowrap">
                  Add Labels</div>
                <div @click="importLabels"
                  class="text-sm bg-gray-200 text-gray-500 p-2 rounded-sm hover:bg-gray-300 cursor-pointer whitespace-nowrap">
                  Import from column</div>
                <div @click="this.tasks[selectedTaskId.value].labels = []"
                  class="text-sm text-red-500 bg-red-100 p-2 rounded-sm hover:bg-red-200 cursor-pointer whitespace-nowrap">
                  Delete all</div>
              </div>
            </div>

            <div class="flex gap-2 mt-4 flex-wrap overflow-scroll w-full max-h-[72px]">
              <div v-if="tasks[selectedTaskId.value].labels.length > 0"
                class="group text-white bg-purple-500 text-sm p-1 px-2 rounded-md h-7 hover:bg-purple-600 cursor-pointer whitespace-pre"
                @click="$emit('deleteLabel', label)" v-for="label in tasks[selectedTaskId.value].labels">
                {{ label
                }}<font-awesome-icon class="text-purple-800 ml-2 group-hover:text-purple-300" icon="fa-solid fa-xmark" />
              </div>

            </div>

          </div>
        </div>
      </div>
    </div>
    <div class="text-sm text-center flex justify-center items-center h-full text-gray-500" v-else>
      <div>
        <p class="">There are currently no tasks<br>Add new task or import a task file in the left panel</p>
      </div>
    </div>
  </div>
</template>

<style>
/* Your component styles here */
</style>