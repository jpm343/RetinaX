<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="650px">
      <template v-slot:activator="{ on }">
        <v-banner :color="color" dark single-line>
          <v-avatar slot="icon" color="secondary" size="40">
            <v-icon icon="mdi-vector-line" color="white"
              >mdi-vector-line</v-icon
            > </v-avatar
          >Recoriding vector parameters
          <v-spacer />
          <v-icon v-if="recordingDone" color="success"
            >mdi-check-outline</v-icon
          >
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
          <span class="headline">Recording vectors</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-combobox
                  v-model="recordingVector.amacrineRecord"
                  label="Amacrine number to record"
                  multiple
                  chips
                  :error-messages="amacrineErrors"
                  @input="$v.recordingVector.amacrineRecord.$touch()"
                  @blur="$v.recordingVector.amacrineRecord.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-select
                  v-model="recordingVector.secRecord"
                  :items="types"
                  attach
                  chips
                  label="Section to record in cell"
                  :error-messages="secErrors"
                  @input="$v.recordingVector.secRecord.$touch()"
                  @blur="$v.recordingVector.secRecord.$touch()"
                ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="recordingVector.amacrineVariableRecord"
                  label="Amacrine variable to record (e.g., ‘v’)"
                  multiple
                  chips
                  :error-messages="amacrineVariableErrors"
                  @input="$v.recordingVector.amacrineVariableRecord.$touch()"
                  @blur="$v.recordingVector.amacrineVariableRecord.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="recordingVector.xRecord"
                  label="Position where to record within NEURON section [0, 1]"
                  multiple
                  chips
                  :error-messages="xErrors"
                  @input="$v.recordingVector.xRecord.$touch()"
                  @blur="$v.recordingVector.xRecord.$touch()"
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="recordingVector.synapsisVariableRecord"
                  label="Synaptic variable to record (e.g. ’sc2’)"
                  multiple
                  chips
                  :error-messages="synapsisErrors"
                  @input="$v.recordingVector.synapsisVariableRecord.$touch()"
                  @blur="$v.recordingVector.synapsisVariableRecord.$touch()"
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
  minValue,
  decimal,
  between,
  alphaNum
} from "vuelidate/lib/validators";
import { mapState } from "vuex";
export default {
  mixins: [validationMixin],
  validations() {
    return {
      recordingVector: {
        amacrineRecord: {
          required,
          $each: {
            integer,
            minValue: minValue(0)
          }
        },
        secRecord: { required },
        xRecord: {
          required,
          $each: {
            decimal,
            between: between(0, 1)
          }
        },
        amacrineVariableRecord: {
          required,
          $each: { alphaNum }
        },
        synapsisVariableRecord: {
          required,
          $each: { alphaNum }
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
    amacrineErrors() {
      const errors = [];
      if (!this.$v.recordingVector.amacrineRecord.$dirty) return errors;
      !this.$v.recordingVector.amacrineRecord.required &&
        errors.push("Required field.");
      this.$v.recordingVector.amacrineRecord.$each.$anyError &&
        errors.push("Must be a numeric value greater or equal to 0");
      return errors;
    },
    secErrors() {
      const errors = [];
      if (!this.$v.recordingVector.secRecord.$dirty) return errors;
      !this.$v.recordingVector.secRecord.required &&
        errors.push("Required field.");
      return errors;
    },
    xErrors() {
      const errors = [];
      if (!this.$v.recordingVector.xRecord.$dirty) return errors;
      !this.$v.recordingVector.xRecord.required &&
        errors.push("Required field.");
      this.$v.recordingVector.xRecord.$each.$anyError &&
        errors.push("Must be a numeric value between 0 and 1");
      return errors;
    },
    amacrineVariableErrors() {
      const errors = [];
      if (!this.$v.recordingVector.amacrineVariableRecord.$dirty) return errors;
      !this.$v.recordingVector.amacrineVariableRecord.required &&
        errors.push("Required field.");
      this.$v.recordingVector.amacrineVariableRecord.$each.$anyError &&
        errors.push("Must be an alphanumeric value");
      return errors;
    },
    synapsisErrors() {
      const errors = [];
      if (!this.$v.recordingVector.synapsisVariableRecord.$dirty) return errors;
      !this.$v.recordingVector.synapsisVariableRecord.required &&
        errors.push("Required field.");
      this.$v.recordingVector.synapsisVariableRecord.$each.$anyError &&
        errors.push("Must be an alphanumeric value");
      return errors;
    },
    ...mapState("parameters", ["recordingDone"])
  },
  data() {
    return {
      dialog: false,
      recordingVector: {},
      useDefault: false,
      types: ["dend", "soma", "action"]
    };
  },
  mounted() {
    this.recordingVector = this.getEmptyItem();
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //this.recordingVector = this.useDefault
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
        //parse integer strings inside arrays
        for (let i = 0; i < this.recordingVector.amacrineRecord.length; i++) {
          this.recordingVector.amacrineRecord[i] = Number(
            this.recordingVector.amacrineRecord[i]
          );
        }
        for (let i = 0; i < this.recordingVector.xRecord.length; i++) {
          this.recordingVector.xRecord[i] = Number(
            this.recordingVector.xRecord[i]
          );
        }
        this.$store
          .dispatch("parameters/setRecordingVector", this.recordingVector)
          .then(() => {
            this.$v.$reset();
            this.dialog = false;
          });
      } else {
        this.$store.dispatch("parameters/recordingDone", false);
      }
    },
    //case1: creating empty item
    getEmptyItem() {
      return {
        amacrineRecord: [],
        secRecord: "",
        xRecord: [],
        amacrineVariableRecord: [],
        synapsisVariableRecord: []
      };
    },
    getDefaultItem() {
      return {
        amacrineRecord: [44, 54, 65], //arreglo de enteros positivos. puede ir el 0
        secRecord: "dend", //puede ser: dend, soma o axon
        xRecord: [0.8], //arreglo de floats entre 0 y 1
        amacrineVariableRecord: ["v"], //arreglo de strings
        synapsisVariableRecord: ["sc2"] //arreglo de strings
      };
    }
  },
  watch: {
    useDefault() {
      if (this.useDefault) {
        this.recordingVector = this.getDefaultItem();

        this.$store.dispatch(
          "parameters/setRecordingVector",
          this.recordingVector
        );

        this.$store.dispatch("parameters/recordingDone", true);
      } else {
        this.recordingVector = this.getEmptyItem();
        this.$store.dispatch("parameters/recordingDone", false);
      }
    }
  }
};
</script>

<style></style>
