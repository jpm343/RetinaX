<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="650px">
      <template v-slot:activator="{ on }">
        <v-banner :color="color" dark single-line>
          <v-avatar slot="icon" color="secondary" size="40">
            <v-icon icon="mdi-brain" color="white">mdi-brain</v-icon> </v-avatar
          >Amacrine Cells Parameters
          <v-spacer />
          <v-icon v-if="amacrineDone" color="success">mdi-check-outline</v-icon>
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
          <span class="headline">Amacrine cells</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.dendritesNumber"
                  label="Dendrites number"
                  type="number"
                  :error-messages="numberErrors"
                  @input="$v.amacrineCells.dendritesNumber.$touch()"
                  @blur="$v.amacrineCells.dendritesNumber.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.dendritesSegments"
                  label="Dendrites segments"
                  type="number"
                  :error-messages="segmentsErrors"
                  @input="$v.amacrineCells.dendritesSegments.$touch()"
                  @blur="$v.amacrineCells.dendritesSegments.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.minDiameter"
                  label="Minimum dendrite diameter"
                  type="number"
                  :error-messages="minErrors"
                  @input="$v.amacrineCells.minDiameter.$touch()"
                  @blur="$v.amacrineCells.minDiameter.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.maxDiameter"
                  label="Maximum dendrite diameter"
                  type="number"
                  :error-messages="maxErrors"
                  @input="$v.amacrineCells.maxDiameter.$touch()"
                  @blur="$v.amacrineCells.maxDiameter.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.preferedDendrite"
                  label="Preferred dendrite"
                  type="number"
                  :error-messages="preferedErrors"
                  @input="$v.amacrineCells.preferedDendrite.$touch()"
                  @blur="$v.amacrineCells.preferedDendrite.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.nullDendrite"
                  label="Null dendrite (opposite to preferred)"
                  type="number"
                  readonly
                  disabled
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="amacrineCells.segmentsWithBipolarInput"
                  label="Segments with bipolar input"
                  hint="Add values one by one (Press Enter key to add)"
                  type="number"
                  multiple
                  chips
                  :error-messages="bipolarErrors"
                  @input="$v.amacrineCells.segmentsWithBipolarInput.$touch()"
                  @blur="$v.amacrineCells.segmentsWithBipolarInput.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="amacrineCells.segmentsWithSacInput"
                  label="Segments with SAC input"
                  hint="Add values one by one (Press Enter key to add)"
                  type="number"
                  multiple
                  chips
                  :error-messages="sacErrors"
                  @input="$v.amacrineCells.segmentsWithSacInput.$touch()"
                  @blur="$v.amacrineCells.segmentsWithSacInput.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="amacrineCells.threshold"
                  label="Threshold of area overlap for SAC-SAC synapse"
                  type="number"
                  :error-messages="threshErrors"
                  @input="$v.amacrineCells.threshold.$touch()"
                  @blur="$v.amacrineCells.threshold.$touch()"
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

import {
  required,
  integer,
  decimal,
  between,
  minValue
} from "vuelidate/lib/validators";
import { mapState } from "vuex";

//custom validator
const segmentsRange = dendritesSegments => value => {
  return value.length <= dendritesSegments;
};

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
      amacrineCells: {
        dendritesNumber: { required, integer, between: between(1, 20) },
        dendritesSegments: { required, integer, between: between(1, 20) },
        minDiameter: {
          required,
          decimal,
          between: between(0, this.amacrineCells.maxDiameter)
        },
        maxDiameter: {
          required,
          decimal,
          between: between(this.amacrineCells.minDiameter, 1e10)
        },
        preferedDendrite: {
          required,
          integer,
          between: between(0, this.amacrineCells.dendritesSegments - 1)
        },
        segmentsWithBipolarInput: {
          required,
          segmentsRange: segmentsRange(this.amacrineCells.dendritesSegments),
          $each: { integer }
        },
        segmentsWithSacInput: {
          required,
          segmentsRange: segmentsRange(this.amacrineCells.dendritesSegments),
          $each: { integer }
        },
        threshold: { required, decimal, minValue: minValue(1e-100) }
      }
    };
  },
  computed: {
    numberErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.dendritesNumber.$dirty) return errors;
      !this.$v.amacrineCells.dendritesNumber.integer &&
        errors.push("Must be a numeric value");
      !this.$v.amacrineCells.dendritesNumber.between &&
        errors.push("Min: 1. Max: 20");
      !this.$v.amacrineCells.dendritesNumber.required &&
        errors.push("Required field.");
      return errors;
    },
    segmentsErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.dendritesSegments.$dirty) return errors;
      !this.$v.amacrineCells.dendritesSegments.integer &&
        errors.push("Must be a numeric value");
      !this.$v.amacrineCells.dendritesSegments.between &&
        errors.push("Min: 1. Max: 20");
      !this.$v.amacrineCells.dendritesSegments.required &&
        errors.push("Required field.");
      return errors;
    },
    minErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.minDiameter.$dirty) return errors;
      !this.$v.amacrineCells.minDiameter.decimal &&
        errors.push("Must be a numeric value");
      !this.$v.amacrineCells.minDiameter.between &&
        errors.push("Min: 0, Max: max setted value");
      !this.$v.amacrineCells.minDiameter.required &&
        errors.push("Required field.");
      return errors;
    },
    maxErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.maxDiameter.$dirty) return errors;
      !this.$v.amacrineCells.maxDiameter.decimal &&
        errors.push("Must be a numeric value");
      !this.$v.amacrineCells.maxDiameter.between &&
        errors.push("Min: minimum setted value");
      !this.$v.amacrineCells.maxDiameter.required &&
        errors.push("Required field.");
      return errors;
    },
    threshErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.threshold.$dirty) return errors;
      !this.$v.amacrineCells.threshold.decimal &&
        errors.push("Must be a numeric value");
      !this.$v.amacrineCells.threshold.minValue &&
        errors.push("Must be a non-zero positive value");
      !this.$v.amacrineCells.threshold.required &&
        errors.push("Required field.");
      return errors;
    },
    preferedErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.preferedDendrite.$dirty) return errors;
      !this.$v.amacrineCells.preferedDendrite.required &&
        errors.push("Required field.");
      !this.$v.amacrineCells.preferedDendrite.integer &&
        errors.push("Must be a numeric value");
      !this.$v.amacrineCells.preferedDendrite.between &&
        errors.push("Muste be between 0 and {dendrites segments - 1}");
      return errors;
    },
    bipolarErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.segmentsWithBipolarInput.$dirty) return errors;
      !this.$v.amacrineCells.segmentsWithBipolarInput.required &&
        errors.push("Required field.");
      //!this.$v.amacrineCells.segmentsWithBipolarInput.integer && errors.push("Debe ingresar valores numéricos")
      !this.$v.amacrineCells.segmentsWithBipolarInput.segmentsRange &&
        errors.push("Dendrites segments quantity exceeded");
      return errors;
    },
    sacErrors() {
      const errors = [];
      if (!this.$v.amacrineCells.segmentsWithSacInput.$dirty) return errors;
      !this.$v.amacrineCells.segmentsWithSacInput.required &&
        errors.push("Required field.");
      //!this.$v.amacrineCells.segmentsWithBipolarInput.integer && errors.push("Debe ingresar valores numéricos")
      !this.$v.amacrineCells.segmentsWithSacInput.segmentsRange &&
        errors.push("Dendrites segments quantity exceeded");
      return errors;
    },
    preferedDendrite() {
      return this.amacrineCells.preferedDendrite;
    },
    ...mapState("parameters", ["amacrineDone"])
  },
  //prop in case of passing a default item
  data() {
    return {
      dialog: false,
      amacrineCells: this.getEmptyItem(),
      useDefault: false
    };
  },
  watch: {
    useDefault() {
      if (this.useDefault) {
        this.amacrineCells = this.getDefaultItem();

        this.$store.dispatch("parameters/setAmacrineCells", this.amacrineCells);

        this.$store.dispatch("parameters/amacrineDone", true);
      } else {
        this.amacrineCells = this.getEmptyItem();
        this.$store.dispatch("parameters/amacrineDone", false);
      }
    },
    preferedDendrite: {
      inmediate: true,
      deep: true,
      handler() {
        this.amacrineCells.nullDendrite = parseInt(
          this.preferedDendrite +
            (this.amacrineCells.dendritesNumber / 2.0 + 0.5)
        );
      }
    }
  },
  mounted() {
    this.amacrineCells = this.getEmptyItem();
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //this.amacrineCells = this.useDefault
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
      if (!this.$v.$invalid) {
        //parse integer strings inside the arrays
        for (
          let i = 0;
          i < this.amacrineCells.segmentsWithBipolarInput.length;
          i++
        ) {
          this.amacrineCells.segmentsWithBipolarInput[i] = Number(
            this.amacrineCells.segmentsWithBipolarInput[i]
          );
        }

        for (
          let i = 0;
          i < this.amacrineCells.segmentsWithSacInput.length;
          i++
        ) {
          this.amacrineCells.segmentsWithSacInput[i] = Number(
            this.amacrineCells.segmentsWithSacInput[i]
          );
        }

        this.$store
          .dispatch("parameters/setAmacrineCells", this.amacrineCells)
          .then(() => {
            this.$v.$reset();
            this.dialog = false;
          });
      } else {
        this.$store.dispatch("parameters/amacrineDone", false);
      }
    },
    //case1: creating empty item
    getEmptyItem() {
      return {
        dendritesNumber: "",
        dendritesSegments: "",
        minDiameter: "",
        maxDiameter: "",
        segmentsWithBipolarInput: [],
        segmentsWithSacInput: [],
        preferedDendrite: "",
        nullDendrite: "",
        threshold: ""
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
        dendritesNumber: 4, //entre 1 y 20
        dendritesSegments: 3, //entre 1 y 20
        minDiameter: 0.5, //entre 0+ e infinito
        maxDiameter: 1.5, //entre 0+ e infinito
        segmentsWithBipolarInput: [0, 1], //entre 0 y cantidad de dentritesSegments
        segmentsWithSacInput: [0], //entre 0 y cantidad de denritesSegments
        preferedDendrite: 0, //entre 0 y dendritesNumber - 1
        nullDendrite: 2, //opuseto a prefered. Calculo: preferedDent + int(dendritesNumber / 2.0 + 0.5)
        threshold: 600 //entre 0 e infinito
      };
    }
  }
};
</script>

<style></style>
