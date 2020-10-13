<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="650px">
      <template v-slot:activator="{ on }">
        <v-banner :color="color" dark single-line>
          <v-avatar slot="icon" color="secondary" size="40">
            <v-icon icon="mdi-alpha-n" color="white"
              >mdi-alpha-n</v-icon
            > </v-avatar
          >Neuron parameters
          <v-spacer />
          <v-icon v-if="neuronDone" color="success">mdi-check-outline</v-icon>
          <template v-slot:actions>
            <v-switch
              v-model="useDefault"
              label="Set default params"
            ></v-switch>
            <v-btn color="secondary" class="mb-2" @click="openDialog" v-on="on"
              >Set parameters</v-btn
            >
          </template>
        </v-banner>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Neuron</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="neuron.simulationTime"
                  label="Simulation time (ms)"
                  type="number"
                  :error-messages="timeErrors"
                  @input="$v.neuron.simulationTime.$touch()"
                  @blur="$v.neuron.simulationTime.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex>
                <v-switch
                  v-model="neuron.cvodeActive"
                  :label="
                    `Is CVODE active?: ${neuron.cvodeActive ? 'yes' : 'no'}`
                  "
                ></v-switch>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="neuron.cvodeTolerance"
                  label="CVODE Tolerance"
                  type="number"
                  :error-messages="cvodeErrors"
                  @input="$v.neuron.cvodeTolerance.$touch()"
                  @blur="$v.neuron.cvodeTolerance.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="neuron.initialVoltage"
                  label="Initial membrane voltage"
                  type="number"
                  :error-messages="voltageErrors"
                  @input="$v.neuron.initialVoltage.$touch()"
                  @blur="$v.neuron.initialVoltage.$touch()"
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="closeDialog">Cancel</v-btn>
          <v-btn color="success" text @click="confirmParams">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, decimal, integer, minValue } from "vuelidate/lib/validators";
import { mapState } from "vuex";
export default {
  mixins: [validationMixin],
  validations() {
    return {
      neuron: {
        simulationTime: { required, integer, minValue: minValue(0) },
        cvodeTolerance: { required, decimal, minValue: minValue(0) },
        initialVoltage: { required, decimal }
      }
    };
  },
  props: {
    color: {
      type: String,
      required: false
    }
  },
  computed: {
    timeErrors() {
      const errors = [];
      if (!this.$v.neuron.simulationTime.$dirty) return errors;
      !this.$v.neuron.simulationTime.required && errors.push("Required field.");
      !this.$v.neuron.simulationTime.integer &&
        errors.push("Must be a positive integer");
      !this.$v.neuron.simulationTime.minValue &&
        errors.push("Must be a positive integer");
      return errors;
    },
    cvodeErrors() {
      const errors = [];
      if (!this.$v.neuron.cvodeTolerance.$dirty) return errors;
      !this.$v.neuron.cvodeTolerance.required && errors.push("Required field.");
      !this.$v.neuron.cvodeTolerance.decimal &&
        errors.push("Must be a positive intger");
      !this.$v.neuron.cvodeTolerance.minValue &&
        errors.push("Must be a positive integer");
      return errors;
    },
    voltageErrors() {
      const errors = [];
      if (!this.$v.neuron.initialVoltage.$dirty) return errors;
      !this.$v.neuron.initialVoltage.required && errors.push("Required field.");
      !this.$v.neuron.initialVoltage.decimal &&
        errors.push("Must be a numeric value");
      return errors;
    },
    ...mapState("parameters", ["neuronDone"])
  },
  data() {
    return {
      dialog: false,
      neuron: {},
      useDefault: false
    };
  },
  watch: {
    useDefault() {
      if (this.useDefault) {
        this.neuron = this.getDefaultItem();

        this.$store.dispatch("parameters/setNeuron", this.neuron);

        this.$store.dispatch("parameters/neuronDone", true);
      } else {
        this.neuron = this.getEmptyItem();
        this.$store.dispatch("parameters/neuronDone", false);
      }
    }
  },
  mounted() {
    this.neuron = this.getEmptyItem();
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //this.neuron = this.useDefault
      //  ? this.getDefaultItem()
      //  : this.getEmptyItem();
      this.dialog = true;
    },
    closeDialog() {
      this.$v.$reset();
      this.dialog = false;
    },
    confirmParams() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        this.$store.dispatch("parameters/setNeuron", this.neuron).then(() => {
          this.$v.$reset();
          this.dialog = false;
        });
      } else {
        this.$store.dispatch("parameters/neuronDone", false);
      }
    },
    //case1: creating empty item
    getEmptyItem() {
      return {
        simulationTime: "",
        cvodeActive: 0,
        cvodeTolerance: "",
        initialVoltage: ""
      };
    },
    getDefaultItem() {
      return {
        simulationTime: 1500, //entero positivo
        cvodeActive: 1, //1 o 0
        cvodeTolerance: 1e-5, //float positivo
        initialVoltage: -60.0 //float positivo o negativo
      };
    }
  }
};
</script>

<style></style>
