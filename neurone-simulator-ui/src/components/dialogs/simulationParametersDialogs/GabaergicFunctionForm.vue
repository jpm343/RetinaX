<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="650px">
      <template v-slot:activator="{ on }">
        <v-banner :color="color" dark single-line>
          <v-avatar slot="icon" color="secondary" size="40">
            <v-icon icon="mdi-function-variant" color="white"
              >mdi-function-variant</v-icon
            > </v-avatar
          >Gabaergic function parameters
          <v-spacer />
          <v-icon v-if="gabaericDone" color="success">mdi-check-outline</v-icon>
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
          <span class="headline">Gabaergic function</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="gabaericFunction.k1Variable"
                  label="K1 variable"
                  type="number"
                  :error-messages="k1Errors"
                  @input="$v.gabaericFunction.k1Variable.$touch()"
                  @blur="$v.gabaericFunction.k1Variable.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="gabaericFunction.k2Variable"
                  label="K2 variable"
                  type="number"
                  :error-messages="k2Errors"
                  @input="$v.gabaericFunction.k2Variable.$touch()"
                  @blur="$v.gabaericFunction.k2Variable.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="gabaericFunction.th1Variable"
                  label="TH1 variable"
                  type="number"
                  :error-messages="th1Errors"
                  @input="$v.gabaericFunction.th1Variable.$touch()"
                  @blur="$v.gabaericFunction.th1Variable.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="gabaericFunction.th2Variable"
                  label="TH2 variable"
                  type="number"
                  :error-messages="th2Errors"
                  @input="$v.gabaericFunction.th2Variable.$touch()"
                  @blur="$v.gabaericFunction.th2Variable.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="gabaericFunction.gabaGmin"
                  label="Minimum GABA conductance"
                  type="number"
                  :error-messages="minErrors"
                  @input="$v.gabaericFunction.gabaGmin.$touch()"
                  @blur="$v.gabaericFunction.gabaGmin.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="gabaericFunction.gabaGmax"
                  label="Maximum GABA conductance"
                  type="number"
                  :error-messages="maxErrors"
                  @input="$v.gabaericFunction.gabaGmax.$touch()"
                  @blur="$v.gabaericFunction.gabaGmax.$touch()"
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
  decimal,
  required,
  maxValue,
  minValue
} from "vuelidate/lib/validators";
import { mapState } from "vuex";
export default {
  mixins: [validationMixin],
  validations() {
    return {
      gabaericFunction: {
        k1Variable: { required, decimal },
        k2Variable: { required, decimal },
        th1Variable: { required, decimal },
        th2Variable: { required, decimal },
        gabaGmin: {
          required,
          decimal,
          maxValue: maxValue(this.gabaericFunction.gabaGmax)
        },
        gabaGmax: {
          required,
          decimal,
          minValue: minValue(this.gabaericFunction.gabaGmin)
        }
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
    k1Errors() {
      const errors = [];
      if (!this.$v.gabaericFunction.k1Variable.$dirty) return errors;
      !this.$v.gabaericFunction.k1Variable.required &&
        errors.push("Required field.");
      !this.$v.gabaericFunction.k1Variable.decimal &&
        errors.push("Must be a numeric value");
      return errors;
    },
    k2Errors() {
      const errors = [];
      if (!this.$v.gabaericFunction.k2Variable.$dirty) return errors;
      !this.$v.gabaericFunction.k2Variable.required &&
        errors.push("Required field.");
      !this.$v.gabaericFunction.k2Variable.decimal &&
        errors.push("Must be a numeric value");
      return errors;
    },
    th1Errors() {
      const errors = [];
      if (!this.$v.gabaericFunction.th1Variable.$dirty) return errors;
      !this.$v.gabaericFunction.th1Variable.required &&
        errors.push("Required field.");
      !this.$v.gabaericFunction.th1Variable.decimal &&
        errors.push("Must be a numeric value");
      return errors;
    },
    th2Errors() {
      const errors = [];
      if (!this.$v.gabaericFunction.th2Variable.$dirty) return errors;
      !this.$v.gabaericFunction.th2Variable.required &&
        errors.push("Required field.");
      !this.$v.gabaericFunction.th2Variable.decimal &&
        errors.push("Must be a numeric value");
      return errors;
    },
    minErrors() {
      const errors = [];
      if (!this.$v.gabaericFunction.gabaGmin.$dirty) return errors;
      !this.$v.gabaericFunction.gabaGmin.required &&
        errors.push("Required field.");
      !this.$v.gabaericFunction.gabaGmin.decimal &&
        errors.push("Must be a numeric value");
      !this.$v.gabaericFunction.gabaGmin.maxValue &&
        errors.push(
          "Minimmum value should be lower than maximmum setted value"
        );
      return errors;
    },
    maxErrors() {
      const errors = [];
      if (!this.$v.gabaericFunction.gabaGmax.$dirty) return errors;
      !this.$v.gabaericFunction.gabaGmax.required &&
        errors.push("Required field.");
      !this.$v.gabaericFunction.gabaGmax.decimal &&
        errors.push("Must be a numeric value");
      !this.$v.gabaericFunction.gabaGmax.minValue &&
        errors.push("Maximmum should be greater than minimmum setted value");
      return errors;
    },
    ...mapState("parameters", ["gabaericDone"])
  },
  data() {
    return {
      dialog: false,
      gabaericFunction: {},
      useDefault: false
    };
  },
  mounted() {
    this.gabaericFunction = this.getEmptyItem();
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //this.gabaericFunction = this.useDefault
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
        this.$store
          .dispatch("parameters/setGabaericFunction", this.gabaericFunction)
          .then(() => {
            this.$v.$reset();
            this.dialog = false;
          });
      } else {
        this.$store.dispatch("parameters/gabaericDone", false);
      }
    },
    //case1: creating empty item
    getEmptyItem() {
      return {
        k1Variable: "",
        k2Variable: "",
        th1Variable: "",
        th2Variable: "",
        gabaGmin: "",
        gabaGmax: ""
      };
    },
    getDefaultItem() {
      return {
        //todos float, pueden ser negativos
        k1Variable: 2.0,
        k2Variable: 0.8,
        th1Variable: -40.0,
        th2Variable: 0.8,
        gabaGmin: 0.000001,
        gabaGmax: 0.0008
      };
    }
  },
  watch: {
    useDefault: {
      handler() {
        if (this.useDefault) {
          this.gabaericFunction = this.getDefaultItem();

          this.$store.dispatch(
            "parameters/setGabaericFunction",
            this.gabaericFunction
          );

          this.$store.dispatch("parameters/gabaericDone", true);
        } else {
          this.gabaericFunction = this.getEmptyItem();
          this.$store.dispatch("parameters/gabaericDone", false);
        }
      }
    }
  }
};
</script>

<style></style>
