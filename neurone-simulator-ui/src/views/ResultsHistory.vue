<template>
  <v-container>
    <v-toolbar>
      <v-toolbar-title>Results history</v-toolbar-title>
    </v-toolbar>
    <v-divider />
    <v-card>
      <v-data-table
        :headers="headers"
        :items="resultsHistory"
        :items-per-page="5"
        class="elevation-1"
      >
        <template v-slot:item.id="{ item }">
          <span>{{ resultsHistory.indexOf(item) + 1 }}</span>
        </template>
        <template v-slot:item.elapsedTime="{ item }">
          <span>{{ item.elapsedTime | formatElapsedTime }}</span>
        </template>
        <template v-slot:item.createdDate="{ item }">
          <span>{{ item.createdDate | formatDate }}</span>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-row align="center" justify="center">
            <v-tooltip top>
              <template v-slot:activator="{ on }">
                <v-btn
                  small
                  depressed
                  outlined
                  icon
                  fab
                  dark
                  color="success"
                  @click="showResults(item)"
                  v-on="on"
                >
                  <v-icon>mdi-text-box-check-outline</v-icon>
                </v-btn>
              </template>
              <span>Show results</span>
            </v-tooltip>
            <all-parameters-dialog :results="item.parameters" />
            <confirm-delete-dialog
              :item="item"
              type="Result history"
              :dispatch-route="deleteDispatchRoute"
              :identifier="getParsedDate(item.createdDate)"
            />
          </v-row>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import ConfirmDeleteDialog from "@/components/dialogs/ConfirmDeleteDialog.vue";
import AllParametersDialog from "@/components/dialogs/simulationParametersDialogs/AllParametersDialog.vue";
import moment from "moment";
export default {
  components: {
    AllParametersDialog,
    ConfirmDeleteDialog,
  },
  data() {
    return {
      loading: false,
      deleteDispatchRoute: "simulation/deleteResult",
      headers: [
        {
          text: "Id",
          value: "id",
          align: "center",
          sortable: true,
        },
        {
          text: "Simulation time [s]",
          value: "elapsedTime",
          align: "center",
          sortable: true,
        },
        {
          text: "Created date",
          value: "createdDate",
          align: "center",
          sortable: true,
        },
        {
          text: "Actions",
          value: "actions",
          align: "center",
          sortable: false,
        },
      ],
    };
  },
  computed: {
    ...mapState("simulation", ["resultsHistory"]),
    parsedResultsHistory() {
      return this.resultsHistory.map((item) => {
        moment(item.createdDate).format("MM/DD/YYYY hh:mm");
      });
    },
  },
  methods: {
    fetchResultsHistory() {
      this.loading = true;
      this.$store
        .dispatch("simulation/fetchResults")
        .then(() => {
          this.loading = false;
        })
        .catch((error) => {
          this.loading = false;
          throw error;
        });
    },
    showResults(resultsObject) {
      //console.log("hola");
      //load results to state
      this.loading = true;
      this.$store.dispatch("simulation/loadResults", resultsObject).then(() => {
        this.loading = false;
        this.$router.push({
          name: "show-results",
        });
      });
    },
    getParsedDate(date) {
      return moment(date).format("MM/DD/YYYY hh:mm");
    },
  },
  mounted() {
    this.fetchResultsHistory();
  },
  filters: {
    formatDate: function(value) {
      if (value) {
        return moment(String(value)).format("MM/DD/YYYY hh:mm");
      }
    },
    formatElapsedTime: function(value) {
      if (value) {
        return value.match(/^-?\d+(?:\.\d{0,2})?/)[0];
      }
    },
  },
};
</script>

<style></style>
