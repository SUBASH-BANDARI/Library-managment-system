<template>
  <div>
    <v-main class="h-screen d-flex">
      <aside>
        <SideBar />
      </aside>
      <div class="pa-3 w-100">
        <LibraryDataTable />
      </div>
    </v-main>
  </div>
</template>

<script setup>
import LibraryDataTable from '@/components/LibraryDataTable.vue';
import SideBar from '@/components/SideBar.vue';

</script>
