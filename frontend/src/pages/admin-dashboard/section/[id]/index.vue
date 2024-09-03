<template>
  <v-main class="h-screen d-flex">
    <aside>
      <SideBar :isAdmin="is_admin" />
    </aside>
    <div class="w-100 h-100 pa-4">
      <v-card flat>
        <v-card-title class="d-flex align-center pe-2">
          <v-icon icon="mdi-book"></v-icon> &nbsp; {{ section_title }} Section

          <v-spacer></v-spacer>
          <v-btn color="orange" @click="openCreateBookDialog"> Add Book </v-btn>

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
        <v-data-table
          v-if="books_new"
          :search="search"
          v-model:page="page"
          :items="books_new"
        >
          <template v-slot:header.title>
            <div>Book Title</div>
          </template>

          <template v-slot:header.document>
            <div>Document URL</div>
          </template>

          <template v-slot:item.image="{ item }">
            <v-img
              class="align-end text-white ma-4"
              height="200"
              :src="getImageSrc(item.image)"
              cover
            >
            </v-img>
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

          <template v-slot:header.document_url>
            <div>Actions</div>
          </template>

          <template v-slot:item.document_url="{ item }">
            <v-icon class="me-2" size="small" @click="openEditBookDialog(item)">
              mdi-pencil
            </v-icon>
            <v-icon size="small" @click="deleteBook(item)"> mdi-delete </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize"> Reset </v-btn>
          </template>

          <template v-slot:bottom>
            <div class="text-center pt-2">
              <v-pagination v-model="page" :length="pageCount"></v-pagination>
            </div>
          </template>
        </v-data-table>
      </v-card>
    </div>

    <v-dialog v-model="isCreateBookDialogOpen" max-width="600">
      <v-card prepend-icon="mdi-account" title="Add a New Book">
        <v-card-text>
          <v-form @submit.prevent>
            <div class="text-subtitle-1 text-medium-emphasis">Book Title</div>

            <v-text-field
              placeholder="Enter Book Title"
              v-model="book_title"
              :rules="bookTitleRules"
            ></v-text-field>

            <v-text-field
              placeholder="Enter Book Genre"
              v-model="genre"
              :rules="bookGenreRules"
            ></v-text-field>

            <v-text-field
              placeholder="Enter Book Author"
              v-model="author"
              :rules="bookAuthorRules"
            ></v-text-field>

            <v-text-field
              placeholder="Enter Book Publisher"
              v-model="publisher"
              :rules="bookPublisherRules"
            ></v-text-field>

            <v-file-input
              accept="image/*"
              label="Upload Cover Photo"
              @change="handleFileChange"
              :rules="bookImageRules"
            ></v-file-input>

            <v-file-input
              accept=".pdf"
              label="Upload Book PDF"
              @change="handlePdfChange"
            ></v-file-input>

            <v-textarea
              v-model="description"
              label="Book Description"
              rows="4"
              variant="filled"
              auto-grow
              :rules="bookDescriptionRules"
            ></v-textarea>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text="Close"
            variant="plain"
            @click="isCreateBookDialogOpen = false"
          ></v-btn>

          <v-btn
            color="primary"
            text="Save"
            variant="tonal"
            @click="addBook"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="isEditBookDialogOpen" max-width="600">
      <v-card prepend-icon="mdi-account" title="Edit Book">
        <v-card-text>
          <v-form @submit.prevent>
            <div class="text-subtitle-1 text-medium-emphasis">Book Title</div>

            <v-text-field
              placeholder="Enter Book Title"
              v-model="editBookOldDetails.title"
              :rules="bookTitleRules"
            ></v-text-field>

            <v-text-field
              placeholder="Enter Book Genre"
              v-model="editBookOldDetails.genre"
              :rules="bookGenreRules"
            ></v-text-field>

            <v-text-field
              placeholder="Enter Book Author"
              v-model="editBookOldDetails.author"
              :rules="bookAuthorRules"
            ></v-text-field>

            <v-text-field
              placeholder="Enter Book Publisher"
              v-model="editBookOldDetails.publisher"
              :rules="bookPublisherRules"
            ></v-text-field>

            <v-file-input
              accept="image/*"
              label="Upload Cover Photo"
              @change="handleFileChange"
              disabled
              :rules="bookImageRules"
            ></v-file-input>

            <!-- <v-file-input
              accept=".pdf"
              label="Upload Book PDF"
              @change="handlePdfChange"
            ></v-file-input> -->

            <v-textarea
              v-model="editBookOldDetails.desc"
              label="Book Description"
              rows="4"
              variant="filled"
              auto-grow
              :rules="bookDescriptionRules"
            ></v-textarea>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text="Close"
            variant="plain"
            @click="isEditBookDialogOpen = false"
          ></v-btn>

          <v-btn
            color="primary"
            text="Save"
            variant="tonal"
            @click="editBook(editBookOldDetails.id)"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-main>
</template>
<script setup>
import SideBar from "@/components/SideBar.vue";
import axios from "axios";
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

const isCreateBookDialogOpen = ref(false);
const isEditBookDialogOpen = ref(false);

const book_title = ref("");
const author = ref("");
const genre = ref("");
const publisher = ref("");
const description = ref("");
const fileInput = ref(null);
const selectedPdfFile = ref(null);

function getImageSrc(imageData) {
  return `data:image/png;base64,${imageData}`;
}

const handleFileChange = (event) => {
  // Read the file as a base64-encoded string
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    fileInput.value = reader.result.split(",")[1]; // Extract base64-encoded data
  };
  reader.readAsDataURL(file);
};

const handlePdfChange = (event) => {
  // Read the file as a base64-encoded string
  selectedPdfFile.value = event.target.files[0];
};

const search = ref("");
const itemPerPage = 10;
const page = ref(1);

const pageCount = computed(() => {
  return Math.ceil(books_new.value.length / itemPerPage);
});

const openCreateBookDialog = () => {
  isCreateBookDialogOpen.value = true;
};

const editBookOldDetails = ref([]);

const openEditBookDialog = async (book) => {
  await axios
    .get(`http://127.0.0.1:5000/books/${book.id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
    .then((res) => {
      editBookOldDetails.value = res.data.book;
    })
    .catch((err) => {
      console.log(err);
    });
  isEditBookDialogOpen.value = true;
};

const deleteBook = async (book) => {
  await axios
    .delete(`http://127.0.0.1:5000/books/${book.id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.log(err);
    });

  await getBooks();
};

const bookTitleRules = [
  (v) => !!v || "Book title is required",
  (v) => (v && v.length <= 50) || "Book title must be less than 50 characters",
];

const bookGenreRules = [
  (v) => !!v || "Book genre is required",
  (v) => (v && v.length <= 50) || "Book genre must be less than 50 characters",
];

const bookAuthorRules = [
  (v) => !!v || "Book author is required",
  (v) => (v && v.length <= 50) || "Book author must be less than 50 characters",
];

const bookPublisherRules = [
  (v) => !!v || "Book publisher is required",
  (v) =>
    (v && v.length <= 50) || "Book publisher must be less than 50 characters",
];

const bookDescriptionRules = [
  (v) => !!v || "Book description is required",
  (v) =>
    (v && v.length <= 500) ||
    "Book description must be less than 500 characters",
];

const bookImageRules = [(v) => !!v || "Book image is required"];

const bookPdfRules = [(v) => !!v || "Book PDF is required"];

const books_new = ref([]);

const section_title = ref("");
const route = useRoute();

async function getSectionDetails() {
  console.log("getSec");
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/section/${route.params.id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    section_title.value = response.data.title;
  } catch (error) {
    console.error("Error fetching section details", error);
  }
}

async function getBooks() {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/books/section/${route.params.id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    books_new.value = response.data.books;
    console.log("Books: ", books_new.value);
  } catch (error) {
    console.error("Error fetching books", error);
  }
}

async function addBook() {
  try {
    const formData = new FormData();
    formData.append("title", book_title.value);
    formData.append("author", author.value);
    formData.append("genre", genre.value);
    formData.append("publisher", publisher.value);
    formData.append("desc", description.value);
    formData.append("image", fileInput.value);
    formData.append("section_id", route.params.id);
    formData.append("document", selectedPdfFile.value);

    // Add additional form data here if needed

    const response = await axios.post(`http://127.0.0.1:5000/books`, formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "multipart/form-data",
      },
    });
    console.log(response.data);
    await getBooks();
    isCreateBookDialogOpen.value = false;
  } catch (error) {
    console.error("Error adding book", error);
  }
}

async function editBook(id) {
  try {
    const response = await axios.put(
      `http://127.0.0.1:5000/books/${id}`,
      {
        title: editBookOldDetails.value.title,
        author: editBookOldDetails.value.author,
        genre: editBookOldDetails.value.genre,
        publisher: editBookOldDetails.value.publisher,
        desc: editBookOldDetails.value.desc,
        image: editBookOldDetails.value.image,
        section_id: route.params.id,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    console.log(response.data);
    await getBooks();
    isEditBookDialogOpen.value = false;
  } catch (error) {
    console.error("Error editing book", error);
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

const is_admin = ref(false);

onMounted(async () => {
  is_admin.value = localStorage.getItem("is_admin") === "true";
  try {
    await getSectionDetails();
    await getBooks();
  } catch (error) {
    console.error("Error fetching sections:", error.message);
  }
});
</script>
