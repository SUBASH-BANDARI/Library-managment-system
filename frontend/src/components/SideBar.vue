<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        permanent
        @click="rail = false"
      >
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
          nav
        >
          <template v-slot:append>
            <v-btn
              icon="mdi-chevron-left"
              variant="text"
              @click.stop="rail = !rail"
            ></v-btn>
          </template>
        </v-list-item>

        <v-divider></v-divider>
        <v-list density="compact" nav v-if="isAdmin">
          <router-link to="/admin-dashboard">
            <v-list-item
              prepend-icon="mdi-book"
              title="Dashboard"
              value="dashboard"
            ></v-list-item>
          </router-link>

          <router-link to="/admin-dashboard/pending-requests">
            <v-list-item
              prepend-icon="mdi-bookshelf"
              title="Pending Requests"
              value="pending-requests"
            ></v-list-item>
          </router-link>
        </v-list>

        <v-list density="compact" nav v-if="!isAdmin">
          <router-link to="/library">
            <v-list-item
              prepend-icon="mdi-bookshelf"
              title="My Library"
              value="library"
            ></v-list-item>
          </router-link>
          <router-link to="/bookstore">
            <v-list-item
              prepend-icon="mdi-store"
              title="Book Store"
              value="book-store"
            ></v-list-item>
          </router-link>
        </v-list>

        <template v-slot:append>
          <div class="pa-4">
            <v-btn
              density="compact"
              @click="logoutUser"
              icon="mdi-logout"
            ></v-btn>
          </div>
        </template>
      </v-navigation-drawer>
      <v-main style="height: 100vh"></v-main>
    </v-layout>
  </v-card>
</template>
<script>
import { useAppStore } from "@/stores/app";
import { mapStores } from "pinia";
export default {
  props: {
    isAdmin: String,
  },
  data() {
    return {
      drawer: true,
      rail: true,
    };
  },

  methods: {
    logoutUser() {
      this.appStore.logout();
      this.$router.push("/");
    },
  },

  // async mounted() {
  //   await axios
  //     .get("http://127.0.0.1:5000/current_user", {
  //       headers: {
  //         Authorization: `Bearer ${localStorage.getItem("token")}`,
  //       },
  //     })
  //     .then((response) => {
  //       this.username = response.data.username;
  //     });
  // },

  computed: {
    ...mapStores(useAppStore),
  },
};
</script>
