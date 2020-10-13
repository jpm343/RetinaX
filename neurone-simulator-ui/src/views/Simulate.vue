<template>
  <div>
    <v-container v-show="!loading">
      <v-card>
        <v-card-title class="mb-5"
          >Please set Simulation parameters first</v-card-title
        >
        <v-card-text>
          <amacrine-cells-form color="primary" />
          <br />
          <bipolar-cells-form color="primary" />
          <br />
          <gabaeric-function-form color="primary" />
          <br />
          <stimmulus-form color="primary" />
          <br />
          <recording-vector-form color="primary" />
          <br />
          <neuron-form color="primary" />
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="secondary"
            :disabled="!this.paramsLoaded"
            class="mb-2"
            @click="startSimulation"
            >Start Simulation</v-btn
          >
        </v-card-actions>
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
        <p class="font-weight-light mb-3 pa-4">
          Running simulation, please wait...
        </p>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
import AmacrineCellsForm from "@/components/dialogs/simulationParametersDialogs/AmacrineCellsForm.vue";
import BipolarCellsForm from "@/components/dialogs/simulationParametersDialogs/BipolarCellsForm.vue";
import GabaericFunctionForm from "@/components/dialogs/simulationParametersDialogs/GabaergicFunctionForm.vue";
import NeuronForm from "@/components/dialogs/simulationParametersDialogs/NueronForm.vue";
import RecordingVectorForm from "@/components/dialogs/simulationParametersDialogs/RecordingVectorForm.vue";
import StimmulusForm from "@/components/dialogs/simulationParametersDialogs/StimmulusForm.vue";
import { HashLoader } from "@saeris/vue-spinners";

export default {
  components: {
    AmacrineCellsForm,
    BipolarCellsForm,
    GabaericFunctionForm,
    NeuronForm,
    RecordingVectorForm,
    StimmulusForm,
    HashLoader
  },
  computed: {
    ...mapState("parameters", [
      "amacrineDone",
      "bipolarDone",
      "gabaericDone",
      "neuronDone",
      "recordingDone",
      "stimmulusDone",
      "params"
    ]),
    paramsLoaded() {
      return (
        this.amacrineDone &&
        this.bipolarDone &&
        this.gabaericDone &&
        this.neuronDone &&
        this.recordingDone &&
        this.stimmulusDone
      );
    }
  },
  data() {
    return {
      loading: false
    };
  },
  methods: {
    startSimulation() {
      this.loading = true;
      this.$store
        .dispatch("simulation/setParams", this.params)
        .then(() => {
          this.loading = false;
          this.$router.push({
            name: "show-results"
          });
        })
        .catch(error => {
          this.loading = false;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  mounted() {
    this.$store.dispatch("parameters/flushParameters");
  }
};
</script>

<style></style>
