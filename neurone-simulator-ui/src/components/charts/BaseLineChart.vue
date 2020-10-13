<template>
  <v-card>
    <v-card-title>
      <v-toolbar flat class="mb-1">
        <v-layout>
          <div class="md-title">{{ graphTitle }}</div>
          <v-spacer />
          <v-flex pa-2 mb-0 xs3>
            <v-select
              :items="items"
              v-model="selected"
              label="Select variable to watch"
              small
              dense
            ></v-select>
          </v-flex>
        </v-layout>
      </v-toolbar>
    </v-card-title>

    <v-card-text>
      <div class="md-layout md-gutter">
        <div class="md-layout-item md-size-100">
          <div ref="graph" style="width:90%;" :id="id"></div>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <div class="legend">
        <div :id="legendId"></div>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script>
//import LineChart from "@/chartTypes/LineChart.js";
import { mapState } from "vuex";
import Dygraph from "dygraphs";
import "dygraphs/dist/dygraph.css";

export default {
  props: {
    yAxisLabel: {
      type: String,
      required: true
    },
    graphTitle: {
      type: String,
      required: true
    },
    type: {
      type: String,
      required: true,
      validator: function(str) {
        return ["temporalEvolution"].indexOf(str) != -1;
      }
    }
  },
  components: {
    //LineChart,
  },
  data() {
    return {
      id: 0,
      loading: true,
      datacollection: null,
      options: null,
      noResults: false,
      items: ["Amacrine cells", "Synapse cells"],
      selected: "Amacrine cells",
      data: {}
    };
  },
  watch: {
    selected: {
      handler() {
        if (this.selected === "Synapse cells")
          this.data = this.simulationResponse.plotData.synapseVecs;
        else this.data = this.simulationResponse.plotData.amacVecs;
        this.fillData();
      }
    }
  },
  computed: {
    ...mapState("simulation", ["simulationResponse", "comesFromHistory"]),
    legendId() {
      return this.id + "_legend";
    }
  },
  mounted() {
    //this.getCurrentMetrics();
    this.data = this.simulationResponse.plotData.amacVecs;
    this.id = 1;
    //console.log(this.simulationResponse.plotData);
    this.fillData();
  },
  methods: {
    fillData() {
      //aqui debieran prepararse los graficos
      let currentLabels = ["x"];
      //prepare labels and datasets. 2 decimals
      let currentDatasets = [];

      for (
        let i = 0;
        i < this.simulationResponse.plotData.timeRec.length;
        i++
      ) {
        let currentEntry = [];

        //this is the "X" value
        currentEntry.push(this.simulationResponse.plotData.timeRec[i]);

        for (let j = 0; j < this.data.length; j++) {
          currentEntry.push(this.data[j][i]);
        }

        currentDatasets.push(currentEntry);
      }

      //this sould depend on vectors names
      for (
        let j = 0;
        j < this.simulationResponse.plotData.cellLabels.length;
        j++
      ) {
        currentLabels.push(
          "Cell " + this.simulationResponse.plotData.cellLabels[j] + ". V1"
        );
        currentLabels.push(
          "Cell " + this.simulationResponse.plotData.cellLabels[j] + ". V2"
        );
      }

      this.options = this.getGraphOptions();
      new Dygraph(this.$refs.graph, currentDatasets, {
        labels: currentLabels,
        ylabel: "[mV]",
        xlabel: "Time",
        title: this.selected,
        legend: "always",
        strokeWidth: 1.5
      });
    },
    getGraphOptions() {
      return {};
    }
  }
};
</script>
<style scoped>
.legend {
  display: flex;
  justify-content: center;
  margin-top: 15px;
  vertical-align: bottom;
}
.dygraph-xlabel {
  display: flex;
  justify-content: center;
}
</style>
