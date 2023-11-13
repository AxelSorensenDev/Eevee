<script>
export default {
  props: {
    page: Object,
  }
}
</script>

<template>
  <div class="flex flex-col justify-center h-screen bg-gray-100 gap-20">
    <div>
      <div class="flex items-center gap-2 justify-center">
        <h1 class="text-3xl text-purple-600 font-bold">Eevee:</h1>

        <h1 class="text-3xl text-gray-700">An Easy Annotation Tool</h1>
        <img class="w-10" src="../assets/Eevee.png" alt="">
      </div>
      <p class="text-center text-gray-400 text-sm mt-2 font-medium">Version 0.1.0</p>
    </div>
    <div class="flex justify-center items-center flex-col gap-2">
      <div
        class="bg-purple-500 p-4 px-8 rounded-md cursor-pointer  text-white font-medium hover:bg-purple-600 w-56 text-center"
        @click="page.name = 'config'">
        Start Annotating</div>
      <a href="https://github.com/AxelSorensenDev/Eevee#readme" target="_blank"
        class="bg-gray-200 p-4 px-8 rounded-md cursor-pointer font-medium text-gray-500 hover:bg-gray-300 hover:text-gray-700 w-56 text-center">
        Learn more
      </a>
    </div>
  </div>
</template>