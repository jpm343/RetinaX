<template>
  <v-container fluid>
    <v-data-iterator
      :items="simulationResponse.parsedResults"
      :items-per-page.sync="itemsPerPage"
      :page="page"
      :search="search"
      :sort-by="sortBy.toLowerCase()"
      :sort-desc="sortDesc"
      hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar dark color="primary" class="mb-1">
          <template v-if="comesFromHistory">
            <v-btn text @click="goBackToHistory">
              <v-icon left>mdi-arrow-left</v-icon>Back to history
            </v-btn>
            <v-spacer />
          </template>
          <template v-else>
            <v-btn text @click="goBackToSimulate">
              <v-icon left>mdi-arrow-left</v-icon>Start another
            </v-btn>
            <v-spacer />
          </template>
          <v-text-field
            v-model="search"
            clearable
            flat
            solo-inverted
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
          ></v-text-field>
          <template v-if="$vuetify.breakpoint.mdAndUp">
            <v-spacer></v-spacer>
            <v-select
              v-model="sortBy"
              flat
              solo-inverted
              hide-details
              :items="parsedResultsKeys"
              prepend-inner-icon="mdi-magnify"
              label="Sort by"
            ></v-select>
            <v-spacer></v-spacer>
            <v-btn-toggle v-model="sortDesc" mandatory>
              <v-btn large depressed color="primary" :value="false">
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn large depressed color="primary" :value="true">
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
            </v-btn-toggle>
          </template>
        </v-toolbar>
      </template>

      <template v-slot:default="props">
        <v-row>
          <v-col
            v-for="item in props.items"
            :key="item.name"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card>
              <v-card-title class="subheading font-weight-bold"
                >Recorded cell N°{{ item.name }}</v-card-title
              >

              <v-divider></v-divider>

              <v-list dense>
                <v-list-item v-for="(key, index) in filteredKeys" :key="index">
                  <v-list-item-content :class="{ 'blue--text': sortBy === key }"
                    >{{ key }}:</v-list-item-content
                  >
                  <v-list-item-content
                    class="align-end"
                    :class="{ 'blue--text': sortBy === key }"
                    >{{ item[key] }}</v-list-item-content
                  >
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <template v-slot:footer>
        <v-toolbar class="mb-1">
          <span class="text">Items per page</span>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn text class="ml-2" v-bind="attrs" v-on="on">
                {{ itemsPerPage }}
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(number, index) in itemsPerPageArray"
                :key="index"
                @click="updateItemsPerPage(number)"
              >
                <v-list-item-title>{{ number }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <v-spacer></v-spacer>
          <span>
            Simulation executed at
            <strong>{{ simulationResponse.createdDate | formatDate }}</strong>
          </span>
          <v-spacer></v-spacer>
          <span>
            Simulation time:
            <strong>
              {{ simulationResponse.elapsedTime | formatElapsedTime }}
              seconds
            </strong>
          </span>

          <v-spacer></v-spacer>
          <template>
            <all-parameters-dialog
              class="mr-2"
              :results="simulationResponse.parameters"
            />
          </template>

          <span class="mr-4 text">Page {{ page }} of {{ numberOfPages }}</span>
          <v-btn fab dark color="primary" class="mr-1" @click="formerPage">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn fab dark color="primary" class="ml-1" @click="nextPage">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-toolbar>
      </template>
    </v-data-iterator>
    <base-line-chart
      v-if="!loading && !comesFromHistory"
      yAxisLabel="prueba"
      graphTitle="Temporal evolution of variable"
      id="1"
      type="temporalEvolution"
    />
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import AllParametersDialog from "@/components/dialogs/simulationParametersDialogs/AllParametersDialog.vue";
import BaseLineChart from "@/components/charts/BaseLineChart.vue";
import moment from "moment";
export default {
  components: {
    AllParametersDialog,
    BaseLineChart
  },
  data() {
    return {
      itemsPerPageArray: [3, 6, 9],
      search: "",
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 3,
      sortBy: "name",
      loading: false
    };
  },
  mounted() {
    //console.log(this.simulationResponse);
    this.fetchFullSimulationDetails();
    //console.log(this.simulationResponse);
    //check if state is loaded
  },
  computed: {
    ...mapState("simulation", ["simulationResponse", "comesFromHistory"]),
    parsedResultsKeys() {
      if (this.simulationResponse.parsedResults)
        return Object.keys(this.simulationResponse.parsedResults[0]);
      else return null;
    },
    numberOfPages() {
      if (this.simulationResponse.parsedResults) {
        return Math.ceil(
          this.simulationResponse.parsedResults.length / this.itemsPerPage
        );
      } else return null;
    },
    filteredKeys() {
      return this.parsedResultsKeys.filter(key => key !== `Name`);
    },
    simulationInfoDisplay() {
      return `<span>Simulation executed at {{ simulationResponse.createdDate | formatDate }}</span>`;
    }
  },
  methods: {
    fetchFullSimulationDetails() {
      //this should be executed only when coming from history
      if (!this.comesFromHistory) return;

      this.loading = true;
      this.$store
        .dispatch(
          "simulation/fetchSingleResultDetails",
          this.simulationResponse
        )
        .then(() => {
          this.loading = false;
          //console.log(this.simulationResponse);
        });
    },
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1;
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1;
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number;
    },
    goBackToHistory() {
      this.$router.push({
        name: "results-history"
      });
    },
    goBackToSimulate() {
      //reset data first
      this.$router.push({
        name: "simulate"
      });
    }
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
    }
  }
};
</script>

<style></style>
