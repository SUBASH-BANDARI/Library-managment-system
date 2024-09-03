<template>
  <div>
    <v-main class="h-screen d-flex">
      <aside>
        <SideBarVue :isAdmin="is_admin" />
      </aside>
      <div class="pa-3 w-100 d-flex flex-column justify-center">
        <h1 class="my-4" v-if="isSectionThere">
          All Sections - {{ sections.length }}
        </h1>
        <v-btn
          class="btn-class"
          color="indigo"
          icon="mdi-plus"
          @click="openCreateSectionDialog"
          v-if="isSectionThere"
        ></v-btn>
        <v-btn
          class="export-btn-class"
          color="indigo"
          icon="mdi-export-variant"
          @click="exportBooks"
          v-if="isSectionThere"
        ></v-btn>
        <div
          class="d-flex flex-column align-center ga-2 align-self-center"
          v-if="!isSectionThere"
        >
          <v-btn
            class="ma-2"
            color="indigo"
            icon="mdi-plus"
            @click="openCreateSectionDialog"
          ></v-btn>
          <p class="text-h5 text-medium-emphasis">Create a new section</p>
        </div>
        <v-row v-if="isSectionThere">
          <v-col v-for="(section, index) in sections" :key="index" cols="2">
            <SectionCard
              :id="section.id"
              :title="section.title"
              :desc="section.desc"
              :image="section.image"
              @sectionDeleted="handleSectionDeleted"
              @editSection="handleSectionEdited"
            />
          </v-col>
        </v-row>
        <div class="pa-4 text-center">
          <v-dialog
            v-model="isCreateSectionDialogOpen"
            max-width="600"
            activator="parent"
          >
            <v-card prepend-icon="mdi-account" title="Create a New Section">
              <v-card-text>
                <v-form @submit.prevent>
                  <div class="text-subtitle-1 text-medium-emphasis">
                    Section Title
                  </div>

                  <v-text-field
                    placeholder="Enter Section Title"
                    prepend-inner-icon="mdi-email-outline"
                    v-model="section_title"
                    :rules="sectionTitleRules"
                  ></v-text-field>

                  <v-file-input
                    accept="image/*"
                    label="Upload Cover Photo"
                    @change="handleFileChange"
                  ></v-file-input>

                  <v-textarea
                    v-model="section_description"
                    label="Section Description"
                    :rules="sectionDescriptionRules"
                    rows="4"
                    variant="filled"
                    auto-grow
                  ></v-textarea>
                </v-form>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                  text="Close"
                  variant="plain"
                  @click="isCreateSectionDialogOpen = false"
                ></v-btn>

                <v-btn
                  color="primary"
                  text="Save"
                  variant="tonal"
                  @click="handleSubmit"
                ></v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-dialog
            v-model="isEditSectionDialogOpen"
            max-width="600"
            activator="parent"
          >
            <v-card prepend-icon="mdi-account" title="Create a New Section">
              <v-card-text>
                <v-form @submit.prevent>
                  <div class="text-subtitle-1 text-medium-emphasis">
                    Section Title
                  </div>

                  <v-text-field
                    placeholder="Enter Section Title"
                    prepend-inner-icon="mdi-email-outline"
                    v-model="oldSectionDetails.title"
                    :rules="sectionTitleRules"
                  ></v-text-field>

                  <v-file-input
                    accept="image/*"
                    label="Upload Cover Photo"
                    @change="handleFileChange"
                    disabled
                  ></v-file-input>

                  <v-textarea
                    v-model="oldSectionDetails.desc"
                    label="Section Description"
                    :rules="sectionDescriptionRules"
                    rows="4"
                    variant="filled"
                    auto-grow
                  ></v-textarea>
                </v-form>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                  text="Close"
                  variant="plain"
                  @click="isEditSectionDialogOpen = false"
                ></v-btn>

                <v-btn
                  color="primary"
                  text="Save"
                  variant="tonal"
                  @click="handleEditSubmit(oldSectionDetails.id)"
                ></v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </div>
    </v-main>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import SectionCard from "@/components/SectionCard.vue";
import ChartComponent from "@/components/ChartComponent.vue";
import SideBarVue from "../../components/SideBar.vue";

const isSectionThere = ref(false);

const isCreateSectionDialogOpen = ref(false);
const section_description = ref("");
const section_title = ref("");
const fileInput = ref(null);

const sections = ref([]);

const is_admin = ref(false);

const isEditSectionDialogOpen = ref(false);

const sectionTitleRules = [
  (v) => !!v || "Section Title is required",
  (v) =>
    (v && v.length <= 50) || "Section Title must be less than 50 characters",
];

const sectionDescriptionRules = [
  (v) => !!v || "Section Description is required",
  (v) =>
    (v && v.length <= 200) ||
    "Section Description must be less than 200 characters",
];

const getSections = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/section", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    sections.value = response.data;
    if (sections.value.length > 0) {
      isSectionThere.value = true;
    }
  } catch (error) {
    console.error("Error fetching sections:", error.message);
  }
};

const exportBooks = async() => {
  try{
    const response =await axios.get("http://127.0.0.1:5000/books/export", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  })
  if(response.status === 200){
    alert("Books exported successfully");
  }else{
    alert("Error exporting books");
  }
  }catch(err){
    console.log(err);
    console.log("this err");
  }
};

const handleFileChange = (event) => {
  // Read the file as a base64-encoded string
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    fileInput.value = reader.result.split(",")[1]; // Extract base64-encoded data
  };
  reader.readAsDataURL(file);
};

async function handleSectionDeleted() {
  await getSections();
}

const oldSectionDetails = ref({});

const handleSectionEdited = async (id) => {
  await axios
    .get(`http://127.0.0.1:5000/section/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      oldSectionDetails.value = response.data;
    })
    .catch((error) => {
      console.error("Error fetching section details:", error.message);
    });

  isEditSectionDialogOpen.value = true;
};

const openCreateSectionDialog = () => {
  isCreateSectionDialogOpen.value = true;
};

async function handleSubmit() {
  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/section",
      {
        title: section_title.value,
        desc: section_description.value,
        image: fileInput.value,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    await getSections();
    console.log(response.data); // Log the response from the backend
    isCreateSectionDialogOpen.value = false;
  } catch (error) {
    console.error("Error uploading file:", error.message);
  }
}

async function handleEditSubmit(id) {
  try {
    const response = await axios.put(
      `http://127.0.0.1:5000/section/${id}`,
      {
        title: oldSectionDetails.value.title,
        desc: oldSectionDetails.value.desc,
        image: oldSectionDetails.value.image,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    await getSections();
    console.log(response.data); // Log the response from the backend
    isEditSectionDialogOpen.value = false;
  } catch (error) {
    console.error("Error uploading file:", error.message);
  }
}

onMounted(async () => {
  is_admin.value = localStorage.getItem("is_admin");
  try {
    await getSections();
    console.log(sections.value);
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

.export-btn-class {
  position: fixed;
  bottom: 20px;
  right: 80px;
}
</style>
