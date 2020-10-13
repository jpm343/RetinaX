<template>
  <v-app-bar color="primary" fixed dark app>
    <v-app-bar-nav-icon @click="handleDrawerToggle"></v-app-bar-nav-icon>

    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-menu
        offset-y
        origin="center center"
        class="elelvation-1"
        :nudge-bottom="14"
        transition="scale-transition"
      ></v-menu>
    </v-toolbar-items>
  </v-app-bar>
</template>
<script>
export default {
  name: "AppToolbar",
  components: {
    //NotificationList
  },
  data() {
    return {
      items: [
        {
          icon: "exit_to_app",
          title: "Logout"
        }
      ]
    };
  },
  computed: {
    toolbarColor() {
      return this.$vuetify.options.extra.mainNav;
    }
  },
  methods: {
    handleDrawerToggle() {
      this.$emit("side-icon-click");
    }
  }
};
</script>

<style lang="stylus" scoped></style>
