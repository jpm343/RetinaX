<template>
  <v-app id="inspire" class="app dashboard">
    <!-- Barra lateral navegación -->
    <app-drawer class="app--drawer" :show-drawer="showDrawer"></app-drawer>
    <!-- Toolbar superior -->
    <app-toolbar
      class="app--toolbar"
      @side-icon-click="handleDrawerVisiable"
    ></app-toolbar>
    <v-content>
      <div class="page-wrapper">
        <router-view></router-view>
      </div>
      <!-- App Footer -->
      <v-footer app height="auto" class="white pa-3 app--footer">
        <span class="caption mr-1">
          Universidad de Santiago de Chile.
          {{ new Date().getFullYear() }}
        </span>
      </v-footer>
    </v-content>
    <Snackbar></Snackbar>
  </v-app>
</template>

<script>
import AppDrawer from "@/components/AppDrawer";
import AppToolbar from "@/components/AppToolbar";
import Snackbar from "@/components/widgets/Snackbar";
export default {
  components: {
    AppDrawer,
    AppToolbar,
    Snackbar
  },
  data() {
    return {
      showDrawer: true
    };
  },
  methods: {
    handleDrawerVisiable() {
      this.showDrawer = !this.showDrawer;
    }
  }
};
</script>

<style>
.page-wrapper {
  min-height: calc(100vh - 64px - 50px - 81px);
}
</style>
