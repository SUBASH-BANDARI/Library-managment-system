<template>
  <v-card class="mx-auto" max-width="300">
    <v-img
      class="align-end text-white"
      height="200"
      :src="getImageSrc(image)"
      cover
    >
    </v-img>
    <v-card-title>{{ title }}</v-card-title>

    <v-card-subtitle class="pt-4"> {{ author }} </v-card-subtitle>

    <v-card-text>
      <div>Publisher: {{ publisher }}</div>

      <div>{{ description }}</div>
    </v-card-text>

    <v-card-actions>
      <v-btn color="orange" @click="requestBook" v-if="!requested">
        Request
      </v-btn>
      <v-btn color="grey" v-else disabled> Requested </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script setup>
import axios from "axios";
import { ref } from "vue";

const props = defineProps({
  author: String,
  description: String,
  genre: String,
  id: Number,
  image: String,
  publisher: String,
  title: String,
});

function getImageSrc(imageData) {
  return `data:image/png;base64,${imageData}`;
}

const requested = ref(false);

async function requestBook() {
  const response = await axios.post(
    `http://127.0.0.1:5000/books/request/${props.id}`,
    {
      days: 7,
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    }
  );

  console.log(response.data);
  if (response.status === 201) {
    alert("Book requested successfully");
    requested.value = true;
  }
}

async function isBookRequested(bookId) {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/books/requested/${bookId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    return response.data.requested;
  } catch (error) {
    console.error("Error fetching book request status", error);
  }
}

onMounted(async () => {
  requested.value = await isBookRequested(props.id);
  console.log(requested.value);
});
</script>
