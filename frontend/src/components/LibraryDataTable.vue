<template>
  <v-card flat>
    <v-card-title class="d-flex align-center pe-2">
      <v-icon icon="mdi-book"></v-icon> &nbsp; Library

      <v-spacer></v-spacer>

      <v-text-field
        v-model="search"
        density="compact"
        label="Search books..."
        prepend-inner-icon="mdi-magnify"
        variant="solo-filled"
        flat
        hide-details
        single-line
      ></v-text-field>
    </v-card-title>

    <v-divider></v-divider>
    <v-data-table v-model:search="search" v-model:page="page" :items="books">
      <template v-slot:header.book_title>
        <div>Book Title</div>
      </template>

      <template v-slot:header.stock>
        <div class="text-end">Stock</div>
      </template>

      <template v-slot:header.grant>
        <div class="text-start">Status</div>
      </template>

      <template v-slot:item.document="{ item }">
        <v-btn
          color="primary"
          @click="downloadPdf(item.document)"
          class="text-white"
        >
          Download PDF
        </v-btn>
      </template>

      <template v-slot:item.stock="{ item }">
        <div class="text-end">
          <v-chip
            :color="item.stock ? 'green' : 'red'"
            :text="item.stock ? 'In stock' : 'Out of stock'"
            class="text-uppercase"
            size="small"
            label
          ></v-chip>
        </div>
      </template>

      <template v-slot:item.grant="{ item }">
        <v-btn
          size="small"
          variant="tonal"
          color="amber"
          @click="returnBook(item)"
          >Return</v-btn
        >
      </template>

      <template v-slot:bottom>
        <div class="text-center pt-2">
          <v-pagination v-model="page" :length="pageCount"></v-pagination>
        </div>
      </template>
    </v-data-table>
  </v-card>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";

const search = ref("");
const itemPerPage = 10;
const page = ref(1);

const pageCount = computed(() => {
  return Math.ceil(books.value.length / itemPerPage);
});

import axios from "axios";

const books = ref([]);

const returnBook = async (book) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/books/return/${book.id}`,
      {
        username: book.username,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    await getBooks();
  } catch (error) {
    console.error("Error returning book", error);
  }
};

async function getBooks() {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/mybooks`, {
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

async function downloadPdf(pdf_url) {
  try {
    const parts = pdf_url.split("\\");
    const filename = parts[parts.length - 1];

    const response = await axios.get(`http://127.0.0.1:5000/pdf/${filename}`, {
      responseType: "blob",
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "book.pdf");
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    console.error("Error downloading PDF", error);
  }
}

onMounted(async () => {
  try {
    await getBooks();
  } catch (error) {
    console.error("Error fetching books", error);
  }
});
</script>
