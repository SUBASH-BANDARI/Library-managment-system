<template>
  <div>
    <v-main class="h-screen d-flex">
      <aside>
        <SideBar :isAdmin="is_admin" />
      </aside>
      <div class="w-50 h-100 pa-4">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-book"></v-icon> &nbsp; Pending Requests

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
          <v-data-table :search="search" v-model:page="page" :items="books">
            <template v-slot:header.book_title>
              <div>Book Title</div>
            </template>

            <template v-slot:header.stock>
              <div class="text-end">Stock</div>
            </template>

            <!-- <template v-slot:item.rating="{ item }">
              <v-rating
                :model-value="item.rating"
                color="orange-darken-2"
                density="compact"
                size="small"
                readonly
              ></v-rating>
            </template> -->

            <template v-slot:item.image="{ item }">
              <v-img
                class="align-end text-white ma-4"
                height="200"
                :src="getImageSrc(item.image)"
                cover
              >
              </v-img>
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
              <!-- <v-chip
            :color="item.status === 'completed' ? 'green' : 'orange'"
            :text="item.status"
            class="text-uppercase"
            size="small"
            label
          ></v-chip> -->
              <v-btn
                size="small"
                variant="tonal"
                color="amber"
                v-if="item.grant"
                >Revoke</v-btn
              >
              <v-btn
                size="small"
                variant="tonal"
                color="blue"
                @click="grantBook(item.id)"
                v-else
                >Grant</v-btn
              >
            </template>

            <template v-slot:bottom>
              <div class="text-center pt-2">
                <v-pagination v-model="page" :length="pageCount"></v-pagination>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </div>

      <div class="w-50 h-100 pa-4">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-book"></v-icon> &nbsp; Granted Books

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
          <v-data-table
            :search="search"
            v-model:page="page"
            :items="books_granted"
          >
            <template v-slot:header.book_title>
              <div>Book Title</div>
            </template>

            <template v-slot:header.stock>
              <div class="text-end">Stock</div>
            </template>

            <!-- <template v-slot:item.rating="{ item }">
              <v-rating
                :model-value="item.rating"
                color="orange-darken-2"
                density="compact"
                size="small"
                readonly
              ></v-rating>
            </template> -->

            <template v-slot:item.image="{ item }">
              <v-img
                class="align-end text-white ma-4"
                height="200"
                :src="getImageSrc(item.image)"
                cover
              >
              </v-img>
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
              <!-- <v-chip
            :color="item.status === 'completed' ? 'green' : 'orange'"
            :text="item.status"
            class="text-uppercase"
            size="small"
            label
          ></v-chip> -->
              <v-btn
                size="small"
                variant="tonal"
                color="amber"
                v-if="item.grant"
                @click="revokeBook(item.id)"
                >Revoke</v-btn
              >
              <v-btn
                size="small"
                variant="tonal"
                color="blue"
                @click="grantBook(item.id)"
                v-else
                >Grant</v-btn
              >
            </template>

            <template v-slot:bottom>
              <div class="text-center pt-2">
                <v-pagination v-model="page" :length="pageCount"></v-pagination>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </div>
    </v-main>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import SideBar from "@/components/SideBar.vue";

const books = ref([]);
const books_granted = ref([]);
const search = ref("");
const itemPerPage = 10;
const page = ref(1);

const pageCount = computed(() => {
  return Math.ceil(books.value.length / itemPerPage);
});

const is_admin = ref(false);

async function getPendingRequests() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/books/pending", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    books.value = response.data.books;
    console.log("books: ", books.value);
  } catch (error) {
    console.error("Error fetching sections", error);
  }
}

async function getGrantedBooks() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/books/granted", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    books_granted.value = response.data.books;
    console.log("books: ", books.value);
  } catch (error) {
    console.error("Error fetching sections", error);
  }
}

async function grantBook(bookId) {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/books/grant/${bookId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    console.log(response.data);
    if (response.status === 200) {
      await getPendingRequests();
      await getGrantedBooks();
    }
  } catch (error) {
    console.error("Error granting book", error);
  }
}

async function revokeBook(bookId) {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/books/revoke/${bookId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    console.log(response.data);
    if (response.status === 200) {
      await getGrantedBooks();
      await getPendingRequests();
    }
  } catch (error) {
    console.error("Error revoking book", error);
  }
}

onMounted(async () => {
  is_admin.value = localStorage.getItem("is_admin") === "true";
  try {
    await getPendingRequests();
    await getGrantedBooks();
  } catch (error) {
    console.error("Error fetching sections:", error.message);
  }
});
</script>
<style scoped>
.btn-class {
  position: fixed;
  bottom: 20px;
  right: 20px;
}
</style>
