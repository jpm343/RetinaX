<template>
  <div>
    <v-dialog v-model="dialog" max-width="650px">
      <v-card>
        <v-card-title>
          <span class="headline">Confirm delete of: {{ type }}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model="identifier"
                  label="Identifier"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false"
            >Cancel</v-btn
          >
          <v-btn color="error darken-1" text @click="confirmDelete"
            >Confirm</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-tooltip top>
      <template v-slot:activator="{ on }">
        <v-btn
          small
          depressed
          outlined
          icon
          fab
          dark
          color="pink"
          @click="dialog = true"
          v-on="on"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
      <span>Delete</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  props: {
    //object to be deleted
    item: {
      type: Object,
      required: true,
    },
    //type to display strings
    type: {
      type: String,
      required: true,
    },
    //where to dispatch method
    dispatchRoute: {
      type: String,
      required: true,
    },
    //field to recognize what is being deleted
    identifier: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    confirmDelete() {
      this.$store.dispatch(this.dispatchRoute, this.item).then(() => {
        this.dialog = false;
      });
    },
  },
};
</script>

<style></style>
