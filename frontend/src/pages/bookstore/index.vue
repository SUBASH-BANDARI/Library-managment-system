<template>
  <div>
    <v-main class="h-screen d-flex">
      <aside>
        <SideBar :isAdmin="is_admin" />
      </aside>
      <div class="pa-3 w-100">
        <div class="mb-4 w-full py-6 d-flex justify-space-between align-center">
          <h1>Book Store</h1>
          <div class="d-flex align-center w-50">
            <!-- <v-combobox
              clearable
              chips
              label="Select Genre"
              density="compact"
              class="mr-4"
              :items="[
                'California',
                'Colorado',
                'Florida',
                'Georgia',
                'Texas',
                'Wyoming',
              ]"
              variant="outlined"
            ></v-combobox> -->
            <v-text-field
              v-model="search"
              density="compact"
              placeholder="Search books..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
            ></v-text-field>
          </div>
        </div>
        <v-row>
          <v-col v-for="(book, index) in books" :key="index" cols="2">
            <UserBookCard
              :author="book.author"
              :description="book.desc"
              :genre="book.genre"
              :id="book.id"
              :image="book.image"
              :publisher="book.publisher"
              :title="book.title"
            />
          </v-col>
        </v-row>
      </div>
    </v-main>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import axios from "axios";
import SideBar from "@/components/SideBar.vue";
import UserBookCard from "@/components/UserBookCard.vue";

const books = ref([]);

const is_admin = ref(false);

const search = ref("");

async function getBooks() {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/books`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    books.value = response.data.books;
    console.log(books.value);
  } catch (error) {
    console.error("Error fetching section details", error);
  }
}

watch(search, async (value) => {
  books.value = books.value.filter((book) =>
    book.title.toLowerCase().includes(value.toLowerCase())
  );
  if (value === "") {
    await getBooks();
  }
});

onMounted(async () => {
  is_admin.value = localStorage.getItem("is_admin") === "true";
  await getBooks();
});
</script>
