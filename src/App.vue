<script>
import Modal from './components/Modal.vue'
import DataField from './components/DataField.vue';
import SideBar from './components/SideBar.vue';
import TaskField from './components/TaskField.vue';
import Annotate from './pages/Annotate.vue';
import DataControls from './components/DataControls.vue';
import FrontPage from './pages/FrontPage.vue';
import { isObjectMatchingStructure } from './Helpers';

export default {

  data() {
    return {
      pages: ['front', 'config', 'annotate'],
      tasks: [],
      data: [],
      dataName: null,
      selectedTaskId: { value: 0 },
      showStrings: { value: false },
      currentSentenceId: { value: 0 },
      label: { text: "" },
      page: { name: 'front' },
      selectedLabelId: { value: 0 },
      selectedWordId: { value: 0 },
      taskTypes: [{ name: 'seq', isWordLevel: true }, { name: 'span', isWordLevel: true }, { name: 'class', isWordLevel: false }, { name: 'seq2seq', isWordLevel: false }],
      searchingSentence: { value: false },
      fileName: { value: null },
      searchBarOpen: { value: false }
    };
  },
  methods: {
    handleKeyDown(event) {
      if (event.keyCode == 39 && this.currentSentenceId.value < this.data.length) {
        this.nextSentence()
      }

      if (event.keyCode == 37 && this.currentSentenceId.value > 0) {
        this.prevSentence()
      }
    },
    clearData() {
      this.data = []
      this.currentSentenceId.value = 0
    },
    async loadHFData() {

      fetch('https://datasets-server.huggingface.co/rows?dataset=fka%2Fawesome-chatgpt-prompts&config=default&split=train&offset=0&limit=100').then(response => {
        return response.text()
      }).then(data => {
        JSON.parse(data).rows.map(row => {
          Object.values(row.row).map(column => {

          })
        })
      })
    },
    nextSentence() {
      if (this.currentSentenceId.value < this.data.length - 1 && !this.searchBarOpen.value) {
        this.currentSentenceId.value++
        this.selectedWordId.value = 0

      }

    },
    prevSentence() {
      if (this.currentSentenceId.value > 0 && !this.searchBarOpen.value) {
        this.currentSentenceId.value--
        this.selectedWordId.value = 0

      }
    },
    searchSentence(e) {
      if (!Number.isInteger(parseInt(e.target.value))) {
        this.searchingSentence.value = false
        return
      }
      if (parseInt(e.target.value) > this.data.length - 1) {
        this.currentSentenceId.value = this.data.length - 1
      } else if (parseInt(e.target.value) < 1) {
        this.currentSentenceId.value = 0
      }
      else {
        this.currentSentenceId.value = parseInt(e.target.value) - 1
      }
      this.searchingSentence.value = false
    },
    updateIDs() {
      this.tasks.map((item, index) => {
        item.id = index;
      });
    },
    addColumn() {
      this.data.map(data => data.words.map(word => ([
        word.push("_")
      ])));
      this.$nextTick(() => (this.$refs.datafield.$refs.scrollToMe.scrollLeft = this.$refs.datafield.$refs.scrollToMe.scrollWidth));
    },
    async addRow() {
      await this.data.map(data => {
        data.strings.push({ name: '_', string: '_' });

      });


      this.$nextTick(() => {
        this.$refs.datafield.$refs.scrollToMe.scrollTop = this.$refs.datafield.$refs.scrollToMe.scrollHeight
        this.$refs.datafield.$refs.input[this.$refs.datafield.$refs.input.length - 1].select()
      });

    },
    updateRowName(args) {
      this.data.map(data => {
        if (data.strings?.[args[0]]?.name) {
          data.strings[args[0]].name = args[1]
        }

      });

    },
    deleteRow(index) {
      this.data.map(data => {
        data.strings.splice(index, 1);
      });
    },
    deleteColumn(index) {
      this.data.map(data => data.words.map(word => ([
        word.splice(index, 1)
      ])));
    },
    addTask() {
      this.tasks.push({ title: "Untitled task", type: this.taskTypes[0], output_index: null, input_index: null, labels: [] });
      this.updateIDs();
      this.selectedTaskId.value = this.tasks.length - 1;
    },
    deleteTask(id) {
      this.tasks = this.tasks.filter((obj) => obj.id !== id);
      this.updateIDs();
      this.selectedTaskId.value = this.tasks.length - 1;
    },
    addLabel() {
      if (this.label.text == "") {
        alert('No labels added. Type in the desired labels to the left of the button')
        return;
      }
      this.tasks[this.selectedTaskId.value].labels.push(...this.label.text.split(',').filter(label => {
        return label != ''
      }));
      this.label.text = "";
    },
    deleteLabel(label) {
      this.tasks[this.selectedTaskId.value].labels = this.tasks[this.selectedTaskId.value].labels.filter(item => {
        return item !== label;
      });
    },
    exportFile() {
      let file = [];
      this.data.flatMap(data => {
        let strings = data.strings.map(string => {
          return `${string.name} = ${string.string}`
        })
        file.push([strings.join('\n'), data.words.map(row => {
          return row.join('\t');
        }).join('\n')].join('\n'))
      });
      file[this.data.length - 1] += '\n'

      this.$refs.myModal.createModal('Export annotation file', `What would you like to name the file?`, [{ text: 'Cancel', action: () => this.$refs.myModal.modal.isOpen = false }, { text: 'Save file', action: () => { this.download(file.join('\n\n'), this.fileName.value + this.$refs.myModal.modal.time + '.conll', 'conll'); this.$refs.myModal.modal.isOpen = false }, color: 'bg-purple-500 hover:bg-purple-600' }], true, 'conll')


    },
    async importTaskFile() {
      let element = document.createElement("input");
      element.setAttribute("type", "file");
      element.setAttribute("accept", ".json");
      element.style.display = "none";
      element.multiple = true;
      document.body.appendChild(element);
      element.click();
      element.addEventListener("change", async (e) => {
        let reader = new FileReader();
        reader.addEventListener("loadend", () => {
          let result = JSON.parse(reader.result)
          if (isObjectMatchingStructure(result[0])) {
            result.map((res, id) => {
              res['id'] = id
            })
            this.tasks = result

            this.selectedTaskId.value = 0
          } else {
            alert('The chosen file does not follow the correct structure of a task file.')
          }
        });
        reader.readAsText(e.target.files[0]);
      });
    },

    async readFile(type) {
      let element = document.createElement("input");
      element.setAttribute("type", "file");
      element.style.display = "none";
      element.multiple = true;
      document.body.appendChild(element);
      element.click();
      element.addEventListener("change", async (e) => {
        let reader = new FileReader();
        reader.addEventListener("loadend", () => {
          if (type == 'txt') {
            try {
              let data = reader.result.split("\n")
              this.data = data.map((sentence, index) => {
                const words = sentence.match(/\w+|[^\w\s]+/g).map((word, index) => {
                  return [index + 1, word]

                });
                const strings = [{ name: '# sent_id', string: index }, { name: '# text', string: sentence }]
                if (!strings.some(string => string.name == '# status')) {
                  strings.push({ name: '# status', string: '{}' })
                }
                if (!strings.some(string => string.name == '# time (ms)')) {
                  strings.push({ name: '# time (ms)', string: 0 })
                }
                return { strings: strings, words: words };
              })
            } catch (error) {
              alert('Could not import the selected file. Make sure the txt file contains one sentence per line with no spaces between lines')
            }

          } else {

            let data = reader.result.split('\n\n')
            data = data.filter(d => d != '')

            this.data = data.map(sentence => {
              const strings = (sentence.split('\n').filter(sent => !sent.match(/.*\t.*/g) && sent != '')?.map(string => {
                return { name: string.split('=')[0]?.trim(), string: string.split('=')[1]?.trim() }
              })) ?? [];


              const rows = sentence.split("\n")
              const words = rows.slice(strings?.length ?? 0).map(row => {
                const cols = row.split("\t");

                return cols;
              });
              if (!strings.some(string => string.name == '# status')) {
                strings.push({ name: '# status', string: '{}' })
              }
              if (!strings.some(string => string.name == '# time (ms)')) {
                strings.push({ name: '# time (ms)', string: 0 })
              }
              return { strings: strings, words: words };
            });
          }


        });
        this.dataName = e.target.files[0].name
        this.fileName.value = e.target.files[0].name.split('.')[0]
        reader.readAsText(e.target.files[0]);
      });
    },
    async download(content, fileName, contentType) {
      var a = document.createElement("a");
      var file = new Blob([content], { type: contentType });
      a.href = URL.createObjectURL(file);
      a.download = fileName;
      a.click();
    },
    exportTaskFile() {
      let file = JSON.stringify(this.tasks, undefined, 2)
      this.$refs.myModal.createModal('Export task file', `What would you like to name the file?`, [{ text: 'Cancel', action: () => this.$refs.myModal.modal.isOpen = false }, { text: 'Save file', action: () => { this.download(file, this.fileName.value + '.json', 'json'); this.$refs.myModal.modal.isOpen = false }, color: 'bg-purple-500 hover:bg-purple-600' }], true, 'json')


    },
  },
  computed: {
    tasksAreFilled() {
      return this.tasks.every(task => {
        if (task.type.isWordLevel) {
          return (task.output_index != '' && task.output_index < this.data[0]?.words[0]?.length && task.output_index >= 0 && task.input_index < this.data[0]?.words[0]?.length && task.input_index >= 0 && task.labels.length > 0 && task.input_index != '')
        } else if (task.type.name == 'seq2seq') {
          return (this.data[0]?.strings.some(string => string.name === task.output_index) && task.input_index < this.data[0]?.words[0]?.length && task.input_index >= 0)
        } else {
          return (this.data[0]?.strings.some(string => string.name === task.output_index) && task.input_index < this.data[0]?.words[0]?.length && task.input_index >= 0 && task.labels.length > 0)
        }

      })
    },
  },
  created() {
    // window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("beforeunload", function (e) {
      e.preventDefault();
      e.returnValue = "";
    });
  },
  // beforeUnmount() {
  //   window.removeEventListener("keydown", this.handleKeyDown);

  // },
  mounted() {
    setInterval(() => {
      this.time++
    }, 1000);
  },

  components: { Modal, SideBar, TaskField, DataField, Annotate, DataControls, FrontPage }
}
</script>

<template>
  <div v-if="page.name == 'front'">
    <FrontPage :page="page" />
  </div>
  <div v-else>
    <Modal ref="myModal" :dataName="dataName" :fileName="fileName" />
    <div class="w-full h-[100vh] bg-white grid grid-cols-[250px,1fr] grid-rows-1 overflow-hidden">
      <SideBar :tasks="tasks" :selectedLabelId="selectedLabelId" :selectedTaskId="selectedTaskId" @addTask="addTask"
        @exportTaskFile="exportTaskFile" @deleteTask="deleteTask" @exportFile="exportFile"
        @importTaskFile="importTaskFile" :data="data" :page="page" :pages="pages" :tasksAreFilled="tasksAreFilled"
        :fileName="fileName" :currentSentenceId="currentSentenceId" />
      <div v-if="page.name == 'config'" class="grid grid-rows-[1fr,60px,minmax(0,1fr)]">
        <TaskField ref="taskfield" :tasks="tasks" :selectedTaskId="selectedTaskId" @addLabel="addLabel" :label="label"
          @deleteLabel="deleteLabel" :data="data" :taskTypes="taskTypes" @importLabels="importLabels"
          :showStrings="showStrings" />
        <DataControls :data="data" :searchingSentence="searchingSentence" :showStrings="showStrings"
          :currentSentenceId="currentSentenceId" @addRow="addRow" @addColumn="addColumn" @nextSentence="nextSentence"
          @prevSentence="prevSentence" @searchSentence="searchSentence" />

        <DataField ref="datafield" :data="data" @clearData="clearData" :showStrings="showStrings" @readFile="readFile"
          @addRow="addRow" @addColumn="addColumn" :refs="$refs" @deleteColumn="deleteColumn" @deleteRow="deleteRow"
          @updateRowName="updateRowName" :currentSentenceId="currentSentenceId" :tasks="tasks" @loadHFData="loadHFData"
          :dataName="dataName" />
      </div>
      <div v-if="page.name == 'annotate'">
        <Annotate ref="annotate" :selectedWordId="selectedWordId" :searchingSentence="searchingSentence" :page="page"
          :data="data" :tasks="tasks" :selectedTaskId="selectedTaskId" @setLabel="setLabel"
          :selectedLabelId="selectedLabelId" @nextSentence="nextSentence" @prevSentence="prevSentence"
          :currentSentenceId="currentSentenceId" @nextTask="nextTask" @prevTask="prevTask"
          @searchSentence="searchSentence" :searchBarOpen="searchBarOpen" />
      </div>
    </div>
  </div>
</template>

