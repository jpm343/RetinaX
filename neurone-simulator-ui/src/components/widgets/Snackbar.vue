<template>
  <div>
    <v-snackbar
      v-model="show"
      :color="snackbar_color"
      multi-line
      :timeout="snackbar_timeout"
      top
      right
      style="opacity: 0.90"
    >
      <strong>{{ snackbar_message }}</strong>
      <v-btn text @click="show = false">
        <strong>X</strong>
      </v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState(["snackbar_message", "snackbar_color", "snackbar_timeout"]),
    show: {
      get() {
        return this.$store.state.snackbar_show;
      },
      set() {
        return this.$store.dispatch("closeSnackbar");
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
