<template>
  <div class="h-screen d-flex align-center justify-center">
    <v-card
      class="mx-auto"
      color="blue-grey-darken-1"
      max-width="420"
      width="420"
    >
      <template v-slot:loader="{ isActive }">
        <v-progress-linear
          :active="isActive"
          color="green-lighten-3"
          height="4"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-img
        height="200"
        src="https://cdn.vuetifyjs.com/images/cards/dark-beach.jpg"
        cover
      >
        <v-row class="pa-3 mt-16">
          <v-row>
            <v-col class="text-center">
              <h3 class="text-h5">Library</h3>

              <span class="text-grey-lighten-1">{{ title }}</span>
            </v-col>
          </v-row>
        </v-row>
      </v-img>

      <v-form @submit.prevent class="pa-12">
        <div class="text-subtitle-1 text-medium-emphasis">Account</div>

        <v-text-field
          placeholder="Enter your email"
          label="Email"
          :rules="emailRules"
          v-model="email"
          prepend-inner-icon="mdi-email-outline"
        ></v-text-field>

        <div
          class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
        >
          Password
        </div>

        <v-text-field
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'"
          label="Password"
          placeholder="Enter your password"
          prepend-inner-icon="mdi-lock-outline"
          v-model="password"
          :rules="passwordRules"
          @click:append-inner="visible = !visible"
        ></v-text-field>

        <div class="px-12">
          <v-btn
            class="mb-8"
            type="submit"
            color="blue"
            size="large"
            variant="tonal"
            block
            @click="loginUser"
          >
            Log In
          </v-btn>
        </div>
      </v-form>

      <v-card-text class="text-center">
        <a
          class="text-blue text-decoration-none"
          href="/signup"
          rel="noopener noreferrer"
        >
          Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
        </a>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { useAppStore } from "@/stores/app";
import { mapStores } from "pinia";
export default {
  data() {
    return {
      title: "The summer breeze",
      invalid_login_message: "Invalid login credentials",

      username: "",
      usernameRules: [
        (value) => {
          if (value) return true;

          return "Username is required!";
        },
      ],
      email: "",
      emailRules: [
        (value) => {
          if (value) return true;

          return "Email is required!";
        },
      ],
      password: "",
      passwordRules: [
        (value) => {
          if (value) return true;

          return "Password is required!";
        },
      ],

      visible: false,
    };
  },

  methods: {
    async loginUser() {
      try{
        await this.appStore.login(this.email, this.password);
      }catch(err) {
        console.log(err);
      }
      if (this.appStore.user && this.appStore.is_admin) {
        this.$router.push("/admin-dashboard");
      } else if (this.appStore.user && !this.appStore.is_admin) {
        this.$router.push("/bookstore");
      } else {
        console.log('Invalid login credentials');
        alert(this.invalid_login_message);
      }
    },
  },

  computed: {
    ...mapStores(useAppStore),
  },
};
</script>
