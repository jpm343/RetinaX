<template>
  <div>
    <v-container>
      <v-card v-show="isWaitingForInput">
        <v-card-title class="headline primary white--text"
          >Build heatmap from simulations history</v-card-title
        >
        <v-card-text>
          <v-subheader class="pa-0"
            >Select a variable and two parameters</v-subheader
          >
          <v-select
            v-model="selectedVariable"
            :items="variables"
            label="Select a variable"
            :counter="60"
            prepend-icon="mdi-function-variant"
            required
            :error-messages="selectedVariableErrors"
            @input="$v.selectedVariable.$touch()"
            @blur="$v.selectedVariable.$touch()"
          >
          </v-select>
          <v-select
            v-model="selectedXParameter"
            :items="parameters"
            :menu-props="{ offsetY: true }"
            chips
            label="first parameter (X axis)"
            required
            prepend-icon="mdi-alpha-x-circle-outline"
            :error-messages="xParameterErrors"
            @input="$v.selectedXParameter.$touch()"
            @blur="$v.selectedXParameter.$touch()"
          >
            <template v-slot:item="{ item }">
              <v-list-item-content>
                <v-list-item-title
                  v-text="item.paramDisplay"
                ></v-list-item-title>
                <v-list-item-subtitle
                  v-text="item.paramLocation"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </template>
            <template v-slot:selection="{ item }">
              {{ item.paramDisplay }}
            </template>
          </v-select>
          <v-select
            v-model="selectedYParameter"
            :items="parameters"
            :menu-props="{ offsetY: true }"
            chips
            label="second parameter (Y axis)"
            required
            prepend-icon="mdi-alpha-y-circle-outline"
            :error-messages="yParameterErrors"
            @input="$v.selectedYParameter.$touch()"
            @blur="$v.selectedYParameter.$touch()"
          >
            <template v-slot:item="{ item }">
              <v-list-item-content>
                <v-list-item-title
                  v-text="item.paramDisplay"
                ></v-list-item-title>
                <v-list-item-subtitle
                  v-text="item.paramLocation"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </template>
            <template v-slot:selection="{ item }">
              {{ item.paramDisplay }}
            </template>
          </v-select>
          <v-btn block color="primary" dark class="mb-2" @click="doFetch()"
            >Go</v-btn
          >
        </v-card-text>
      </v-card>
    </v-container>
    <v-container fluid v-show="loading" class="container-scoped">
      <v-row align="center" justify="center">
        <hash-loader
          :loading="this.loading"
          color="#9C27B0"
          :size="140"
          sizeUnit="px"
        />
        <br />
        <p class="font-weight-light mb-3 pa-4">Loading heatmap data...</p>
      </v-row>
    </v-container>
    <v-container v-show="isDataLoaded" fluid>
      <v-toolbar dark color="primary" class="mb-1">
        <v-btn text @click="goBack">
          <v-icon left>mdi-arrow-left</v-icon>Back to params selection
        </v-btn>
      </v-toolbar>
      <v-card>
        <v-card-title>
          <div class="md-title">{{ heatmapCardTitle }}</div>
          <v-spacer />
          <v-select
            :items="variables"
            v-model="selectedVariable"
            label="Select variable to watch"
            small
          ></v-select>
        </v-card-title>

        <v-card-text>
          <div ref="graph" style="width:100%;" :id="id"></div>
        </v-card-text>
        <v-card-actions>
          <div class="legend">
            <div :id="legendId"></div>
          </div>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>

<script>
//import LineChart from "@/chartTypes/LineChart.js";
import { mapState } from "vuex";
import { HashLoader } from "@saeris/vue-spinners";
import { validationMixin } from "vuelidate";
import { required, sameAs, not } from "vuelidate/lib/validators";
import ApexCharts from "apexcharts";

export default {
  mixins: [validationMixin],
  props: {},
  components: {
    //LineChart,
    HashLoader
  },
  data() {
    return {
      //HEATMAP SELECTION DATA:
      variables: ["DSsc", "DSsca", "DSvd", "scp", "scpa", "vp"],
      parameters: [
        {
          paramKey: "ndend",
          paramLocation: "amacrine",
          paramDisplay: "Dendrites number"
        },
        {
          paramKey: "dendseg",
          paramLocation: "amacrine",
          paramDisplay: "Dendrites segments"
        },
        {
          paramKey: "diam_min",
          paramLocation: "amacrine",
          paramDisplay: "Minimum dendrite diameter"
        },
        {
          paramKey: "diam_max",
          paramLocation: "amacrine",
          paramDisplay: "Maximum dendrite diameter"
        },
        {
          paramKey: "area_thresh",
          paramLocation: "amacrine",
          paramDisplay: "Threshold of area overlap for SAC-SAC synapse"
        },
        {
          paramKey: "k1",
          paramLocation: "gabaeric",
          paramDisplay: "K1 variable"
        },
        {
          paramKey: "k2",
          paramLocation: "gabaeric",
          paramDisplay: "K2 variable"
        },
        {
          paramKey: "th1",
          paramLocation: "gabaeric",
          paramDisplay: "TH1 variable"
        },
        {
          paramKey: "th2",
          paramLocation: "gabaeric",
          paramDisplay: "TH2 variable"
        },
        {
          paramKey: "gabaGmin",
          paramLocation: "gabaeric",
          paramDisplay: "Minimum GABA conductance"
        },
        {
          paramKey: "gabaGmax",
          paramLocation: "gabaeric",
          paramDisplay: "Maximum GABA conductance"
        },
        {
          paramKey: "d_is",
          paramLocation: "bipolar",
          paramDisplay: "Distance between synaptic input"
        },
        {
          paramKey: "excGmax",
          paramLocation: "bipolar",
          paramDisplay: "Maximum excitatory conductance"
        },
        {
          paramKey: "excGmin",
          paramLocation: "bipolar",
          paramDisplay: "Minimum excitatory conductance"
        },
        {
          paramKey: "bar_speed",
          paramLocation: "stimmulus.stim_param",
          paramDisplay: "bar_speed"
        },
        {
          paramKey: "bar_width",
          paramLocation: "stimmulus.stim_param",
          paramDisplay: "bar_width"
        },
        {
          paramKey: "bar_x_init",
          paramLocation: "stimmulus.stim_param",
          paramDisplay: "bar_x_init"
        },
        {
          paramKey: "t_stop",
          paramLocation: "neuron",
          paramDisplay: "Simulation time"
        },
        {
          paramKey: "cvode_tolerance",
          paramLocation: "neuron",
          paramDisplay: "CVODE tolerance"
        },
        {
          paramKey: "v_init",
          paramLocation: "neuron",
          paramDisplay: "Initial membrane voltage"
        }
      ],

      selectedVariable: "",
      selectedXParameter: {
        paramKey: "",
        paramLocation: "",
        paramDisplay: ""
      },
      selectedYParameter: {
        paramKey: "",
        paramLocation: "",
        paramDisplay: ""
      },

      isWaitingForInput: true,
      loading: false,
      isDataLoaded: false,

      id: 0,
      datacollection: null,
      noResults: false,
      items: ["Amacrine cells", "Synapse cells"],
      selected: "Amacrine cells",
      data: {},
      options: {
        chart: {
          height: 350,
          type: "heatmap"
        },
        title: {
          text: "HeatMap Chart (Single color)"
        },
        plotOptions: {
          heatmap: {
            colorScale: {
              ranges: []
            }
          }
        }
      },
      chart: {}
    };
  },
  validations() {
    return {
      selectedVariable: { required },
      selectedXParameter: {
        required,
        notEqual: not(sameAs("selectedYParameter"))
      },
      selectedYParameter: {
        required,
        notEqual: not(sameAs("selectedXParameter"))
      }
    };
  },
  watch: {
    selectedVariable() {
      if (!this.isWaitingForInput && !this.loading) {
        this.refreshHeatMapVariables();
      }
    }
  },
  computed: {
    ...mapState("simulation", ["currentHeatMapData"]),
    heatmapTitle() {
      return (
        "Showing heatmap for parameters: " +
        this.selectedYParameter.paramDisplay +
        " (" +
        this.selectedYParameter.paramKey +
        ") and " +
        this.selectedXParameter.paramDisplay +
        " (" +
        this.selectedXParameter.paramKey +
        ")"
      );
    },
    heatmapCardTitle() {
      return "Heatmap for " + this.selectedVariable + " variable.";
    },
    legendId() {
      return this.id + "_legend";
    },
    selectedVariableErrors() {
      const errors = [];
      if (!this.$v.selectedVariable.$dirty) return errors;
      !this.$v.selectedVariable.required && errors.push("Required field.");
      return errors;
    },
    xParameterErrors() {
      const errors = [];
      if (!this.$v.selectedXParameter.$dirty) return errors;
      !this.$v.selectedXParameter.notEqual &&
        errors.push("X and Y must be different parameters");
      !this.$v.selectedXParameter.required && errors.push("Required field.");
      return errors;
    },
    yParameterErrors() {
      const errors = [];
      if (!this.$v.selectedYParameter.$dirty) return errors;
      !this.$v.selectedYParameter.notEqual &&
        errors.push("X and Y must be different parameters");
      !this.$v.selectedYParameter.required && errors.push("Required field.");
      return errors;
    }
  },
  mounted() {
    this.loading = false;
  },
  methods: {
    getGraphOptions() {
      return {};
    },
    doFetch() {
      this.$v.$touch();
      if (this.$v.$invalid) return;
      //COMMENTED MEANWHILE
      let payload = {
        variable: this.selectedVariable,
        xParameter: this.selectedXParameter.paramKey,
        xParameterLocation: this.selectedXParameter.paramLocation,
        yParameter: this.selectedYParameter.paramKey,
        yParameterLocation: this.selectedYParameter.paramLocation
      };
      this.isWaitingForInput = false;
      this.loading = true;
      this.$store.dispatch("simulation/fetchHeatMapData", payload).then(() => {
        this.loading = false;
        this.isDataLoaded = true;
        this.buildHeatMap();
      });
    },
    buildHeatMap() {
      this.currentHeatMapData.sort((a, b) => a.ylabel - b.ylabel);
      this.currentHeatMapData.map(value => {
        value.data.sort((a, b) => a.x - b.x);
      });
      this.options.title.text = this.heatmapTitle;
      let totalValues = [];
      this.options.series = this.currentHeatMapData.map(value => {
        return {
          name: this.selectedYParameter.paramKey + ": " + value.ylabel,
          data: value.data.map(dataValue => {
            let yVal =
              dataValue.y[this.selectedVariable] !== undefined
                ? dataValue.y[this.selectedVariable].reduce(
                    (a, b) => a + b,
                    0
                  ) / dataValue.y[this.selectedVariable].length
                : 0;

            totalValues.push(yVal);

            return {
              x: this.selectedXParameter.paramKey + ": " + dataValue.x,
              y: yVal
            };
          })
        };
      });

      this.setMinAndMax(totalValues);

      this.chart = new ApexCharts(this.$refs.graph, this.options);
      this.chart.render();
    },
    setMinAndMax(values) {
      let min = Math.min.apply(Math, values);
      let max = Math.max.apply(Math, values);

      let step = (max - min) / 3;
      let firstStep = min + step;
      let secondStep = max - step;

      this.options.plotOptions.heatmap.colorScale.ranges = [
        {
          from: min,
          to: firstStep,
          color: "#00A100",
          name: "low"
        },
        {
          from: firstStep,
          to: secondStep,
          color: "#128FD9",
          name: "medium"
        },
        {
          from: secondStep,
          to: max,
          color: "#FFB200",
          name: "high"
        }
      ];
    },
    refreshHeatMapVariables() {
      let totalValues = [];
      this.options.series = this.currentHeatMapData.map(value => {
        return {
          name: this.selectedYParameter.paramKey + ": " + value.ylabel,
          data: value.data.map(dataValue => {
            let yVal =
              dataValue.y[this.selectedVariable] !== undefined
                ? dataValue.y[this.selectedVariable].reduce(
                    (a, b) => a + b,
                    0
                  ) / dataValue.y[this.selectedVariable].length
                : 0;

            totalValues.push(yVal);
            return {
              x: this.selectedXParameter.paramKey + ": " + dataValue.x,
              y: yVal
            };
          })
        };
      });

      this.setMinAndMax(totalValues);
      this.chart.updateOptions(this.options);
    },
    goBack() {
      this.$store.dispatch("simulation/flushHeatmapData").then(() => {
        this.chart.destroy();
        this.selectedVariable = "";
        this.selectedYParameter = {};
        this.selectedXParameter = {};
        this.$v.$reset();
        this.isDataLoaded = false;
        this.loading = false;
        this.isWaitingForInput = true;
      });
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
.container-scoped {
  position: absolute;
  bottom: 50%;
}
</style>
