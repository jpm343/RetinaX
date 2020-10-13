<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="650px">
      <template v-slot:activator="{ on }">
        <v-banner :color="color" dark single-line>
          <v-avatar slot="icon" color="secondary" size="40">
            <v-icon icon="mdi-atom-variant" color="white"
              >mdi-atom-variant</v-icon
            > </v-avatar
          >Bipolar cells parameters
          <v-spacer />
          <v-icon v-if="bipolarDone" color="success">mdi-check-outline</v-icon>
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
          <span class="headline">Bipolar cells</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="bipolarCells.synapticDistance"
                  label="Distance between synaptic input"
                  type="number"
                  :error-messages="distanceErrors"
                  @input="$v.bipolarCells.synapticDistance.$touch()"
                  @blur="$v.bipolarCells.synapticDistance.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="bipolarCells.excitatoryMax"
                  label="Maximum excitatory conductance"
                  type="number"
                  :error-messages="maxExcErrors"
                  @input="$v.bipolarCells.excitatoryMax.$touch()"
                  @blur="$v.bipolarCells.excitatoryMax.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="bipolarCells.excitatoryMin"
                  label="Minimum excitatory conductance"
                  type="number"
                  :error-messages="minExcErrors"
                  @input="$v.bipolarCells.excitatoryMin.$touch()"
                  @blur="$v.bipolarCells.excitatoryMin.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-select
                  v-model="bipolarCells.synapsisType"
                  :items="synapTypes"
                  attach
                  label="Synapse type"
                  :error-messages="typeErrors"
                  @input="$v.bipolarCells.synapsisType.$touch()"
                  @blur="$v.bipolarCells.synapsisType.$touch()"
                ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="bipolarCells.synapseTimeConstant"
                  label="Time constants of synapse"
                  hint="Add values one by one (Press Enter key to add)"
                  type="number"
                  multiple
                  chips
                  :error-messages="synapseTimeErrors"
                  @input="$v.bipolarCells.synapseTimeConstant.$touch()"
                  @blur="$v.bipolarCells.synapseTimeConstant.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="bipolarCells.BPTimeConstant"
                  label="Time constants of BPexc"
                  hint="Add values one by one (Press Enter key to add)"
                  type="number"
                  multiple
                  chips
                  :error-messages="BPTimeErrors"
                  @input="$v.bipolarCells.BPTimeConstant.$touch()"
                  @blur="$v.bipolarCells.BPTimeConstant.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="bipolarCells.BPTimeConstant2"
                  label="Time constants of BPexc 2"
                  hint="Add values one by one (Press Enter key to add)"
                  type="number"
                  multiple
                  chips
                  :error-messages="BPTimeErrors2"
                  @input="$v.bipolarCells.BPTimeConstant2.$touch()"
                  @blur="$v.bipolarCells.BPTimeConstant2.$touch()"
                ></v-combobox>
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
import {
  required,
  integer,
  //numeric,
  //between,
  //maxLength,
  minValue,
  maxValue
} from "vuelidate/lib/validators";
import { mapState } from "vuex";

export default {
  props: {
    color: {
      type: String,
      required: false
    }
  },
  //validation stuff
  mixins: [validationMixin],
  validations() {
    return {
      bipolarCells: {
        synapticDistance: { required, integer, minValue: minValue(0) },
        excitatoryMin: {
          required,
          maxValue: maxValue(this.bipolarCells.excitatoryMax)
        },
        excitatoryMax: {
          required,
          minValue: minValue(this.bipolarCells.excitatoryMin)
        },
        synapsisType: { required },
        synapseTimeConstant: { required },
        BPTimeConstant: { required },
        BPTimeConstant2: { required }
      }
    };
  },
  computed: {
    distanceErrors() {
      const errors = [];
      if (!this.$v.bipolarCells.synapticDistance.$dirty) return errors;
      !this.$v.bipolarCells.synapticDistance.integer &&
        errors.push("Must be a numeric value");
      !this.$v.bipolarCells.synapticDistance.minValue && errors.push("Min: 0");
      !this.$v.bipolarCells.synapticDistance.required &&
        errors.push("Required field.");
      return errors;
    },
    minExcErrors() {
      const errors = [];
      if (!this.$v.bipolarCells.excitatoryMin.$dirty) return errors;
      //!this.$v.bipolarCells.excitatoryMin.numeric &&
      //  errors.push("Must be a numeric value");
      !this.$v.bipolarCells.excitatoryMin.maxValue &&
        errors.push("Minimum must be lower than maximum setted value");
      !this.$v.bipolarCells.excitatoryMin.required &&
        errors.push("Required field.");
      return errors;
    },
    maxExcErrors() {
      const errors = [];
      if (!this.$v.bipolarCells.excitatoryMax.$dirty) return errors;
      //!this.$v.bipolarCells.excitatoryMax.numeric &&
      //  errors.push("Must be a numeric value");
      !this.$v.bipolarCells.excitatoryMax.minValue &&
        errors.push("Maximum should be greater than minimum setted value");
      !this.$v.bipolarCells.excitatoryMax.required &&
        errors.push("Required field.");
      return errors;
    },
    typeErrors() {
      const errors = [];
      if (!this.$v.bipolarCells.synapsisType.$dirty) return errors;
      !this.$v.bipolarCells.synapsisType.required && errors.push("Select one.");
      return errors;
    },
    synapseTimeErrors() {
      const errors = [];
      if (!this.$v.bipolarCells.synapseTimeConstant.$dirty) return errors;
      !this.$v.bipolarCells.synapseTimeConstant.required &&
        errors.push("Enter at least one value");
      return errors;
    },
    BPTimeErrors() {
      const errors = [];
      if (!this.$v.bipolarCells.BPTimeConstant.$dirty) return errors;
      !this.$v.bipolarCells.BPTimeConstant.required &&
        errors.push("Enter at least one value");
      return errors;
    },
    BPTimeErrors2() {
      const errors = [];
      if (!this.$v.bipolarCells.BPTimeConstant2.$dirty) return errors;
      !this.$v.bipolarCells.BPTimeConstant2.required &&
        errors.push("Enter at least one value");
      return errors;
    },
    ...mapState("parameters", ["bipolarDone"])
  },
  //prop in case of passing a default item
  data() {
    return {
      dialog: false,
      bipolarCells: this.getEmptyItem(),
      useDefault: false,
      synapTypes: ["BPexc", "eCsyn", "aCsyn"]
    };
  },
  watch: {
    useDefault() {
      if (this.useDefault) {
        this.bipolarCells = this.getDefaultItem();

        this.$store.dispatch("parameters/setBipolarCells", this.bipolarCells);

        this.$store.dispatch("parameters/bipolarDone", true);
      } else {
        this.bipolarCells = this.getEmptyItem();
        this.$store.dispatch("parameters/bipolarDone", false);
      }
    }
  },
  mounted() {
    this.bipolarCells = this.getEmptyItem();
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //this.bipolarCells = this.useDefault
      //  ? this.getDefaultItem()
      //  : this.getEmptyItem();
      this.dialog = true;
    },
    closeDialog() {
      this.$v.$reset();
      this.dialog = false;
    },
    confirmParams() {
      //aqui asociar el param
      this.$v.$touch();
      //console.log(this.$v);
      if (!this.$v.$invalid) {
        //parse integer strings inside arrays
        for (let i = 0; i < this.bipolarCells.synapseTimeConstant.length; i++) {
          this.bipolarCells.synapseTimeConstant[i] = Number(
            this.bipolarCells.synapseTimeConstant[i]
          );
        }
        for (let i = 0; i < this.bipolarCells.BPTimeConstant.length; i++) {
          this.bipolarCells.BPTimeConstant[i] = Number(
            this.bipolarCells.BPTimeConstant[i]
          );
        }
        for (let i = 0; i < this.bipolarCells.BPTimeConstant2.length; i++) {
          this.bipolarCells.BPTimeConstant2[i] = Number(
            this.bipolarCells.BPTimeConstant2[i]
          );
        }

        this.$store
          .dispatch("parameters/setBipolarCells", this.bipolarCells)
          .then(() => {
            this.$v.$reset();
            this.dialog = false;
          });
      } else {
        this.$store.dispatch("parameters/bipolarDone", false);
      }
    },
    //case1: creating empty item
    getEmptyItem() {
      return {
        synapticDistance: "",
        excitatoryMin: "",
        excitatoryMax: "",
        synapsisType: "",
        synapseTimeConstant: [],
        BPTimeConstant: [],
        BPTimeConstant2: []
      };
    },
    //case2: getting item from vuex
    /*
    getItemCopy() {
      return Object.assign({}, this.state.default)  
    }*/
    //case3: the default item is stored locally
    getDefaultItem() {
      return {
        synapticDistance: 15, //entero positivo
        excitatoryMin: 0.0000001, //float que puede ser negativo
        excitatoryMax: 0.000001, //idem
        synapsisType: "BPexc", // entre: BPexc, eCsyn y aCsyn
        synapseTimeConstant: [2, 10], //arreglo de floats de tiempo (positivos)
        BPTimeConstant: [20, 2], //idem
        BPTimeConstant2: [1000, 10]
      };
    }
  }
};
</script>

<style></style>
