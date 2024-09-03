<template>
  <div>
    <div class="mb-4 w-full text-center py-6">
      <h1>Book Store</h1>
    </div>
    <button @click="toggleMicrophone">
      {{ isRecording ? "Stop" : "Start" }} recording
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const sr = new SpeechRecognition();
const isRecording = ref(false);

onMounted(() => {
  console.log("mounted");
  sr.continuous = true;
  sr.interimResults = true;

  sr.onstart = () => {
    console.log("Voice recognition started...");
    isRecording.value = true;
  };

  sr.onend = () => {
    console.log("Voice recognition stopped...");
    isRecording.value = false;
  };

  sr.onresult = (event) => {
    console.log(event);
  };
});

const toggleMicrophone = () => {
  console.log(isRecording.value);
  if (isRecording.value) {
    sr.stop();
  } else {
    sr.start();
  }
};
</script>
