<template>
  <v-card class="mx-auto" max-width="300">
    <v-img
      class="align-end text-white"
      height="200"
      :src="getImageSrc(image)"
      cover
    >
    </v-img>

    <v-card-subtitle class="pt-4">{{ title }}</v-card-subtitle>

    <v-card-text>
      <div>{{ desc }}</div>
    </v-card-text>

    <v-card-actions class="d-flex justify-space-between">
      <v-btn
        color="orange"
        @click="() => $router.push(`/admin-dashboard/section/${props.id}`)"
      >
        View Books
      </v-btn>
      <div>
        <v-btn
          color="blue-lighten-2"
          icon="mdi-pencil"
          variant="text"
          @click="editSection"
        ></v-btn>
        <v-btn :disabled="title == 'Miscellaneous'"
          color="blue-lighten-2"
          icon="mdi-delete"
          variant="text"
          @click="deleteSection"
        ></v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>
<script setup>
import axios from "axios";
import { defineProps } from "vue";

const emit = defineEmits(["section-deleted", 'edit-section']);

const props = defineProps({
  id: Number,
  title: String,
  desc: String,
  image: String,
});

function getImageSrc(imageData) {
  return `data:image/png;base64,${imageData}`;
}

async function deleteSection() {
  try {
    await axios.delete(`http://localhost:5000/section/${props.id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    console.log("Section deleted successfully");
    emit("section-deleted");
  } catch (error) {
    console.error("Error deleting section", error);
  }
}

function editSection() {
  emit("edit-section", props.id);
}
</script>
