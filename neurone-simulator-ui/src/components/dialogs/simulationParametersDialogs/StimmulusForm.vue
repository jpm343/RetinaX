<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="650px">
      <template v-slot:activator="{ on }">
        <v-banner :color="color" dark single-line>
          <v-avatar slot="icon" color="secondary" size="40">
            <v-icon icon="mdi-resistor" color="white"
              >mdi-resistor</v-icon
            > </v-avatar
          >Stimmulus parameters
          <v-spacer />
          <v-icon v-if="stimmulusDone" color="success"
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
          <span class="headline">Stimmulus</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-select
                  v-model="stimmulus.stimmulusType"
                  :items="types"
                  attach
                  chips
                  label="Stimulus type"
                  :error-messages="typeErrors"
                  @input="$v.stimmulus.stimmulusType.$touch()"
                  @blur="$v.stimmulus.stimmulusType.$touch()"
                ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="stimmulus.stabilizationTime"
                  label="Stabilization time (ms)"
                  type="float"
                  :error-messages="timeErrors"
                  @input="$v.stimmulus.stabilizationTime.$touch()"
                  @blur="$v.stimmulus.stabilizationTime.$touch()"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-divider v-if="currentStimmulusType"></v-divider>
            <v-layout v-if="currentStimmulusType" wrap>
              <!--this must be fixed-->
              <span class="headline"
                >Stimmulus Params: {{ currentStimmulusType }}</span
              >
              <v-flex
                v-for="(item, key, index) in stimmulusParam"
                :key="index"
                xs12
              >
                <v-text-field
                  v-model.number="stimmulusParam[key]"
                  :label="key"
                  type="number"
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
import { required, decimal } from "vuelidate/lib/validators";
import { mapState } from "vuex";
export default {
  mixins: [validationMixin],
  validations() {
    return {
      stimmulus: {
        stimmulusType: { required },
        stabilizationTime: { required, decimal }
      }
    };
  },
  props: {
    color: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      dialog: false,
      stimmulus: {},
      stimmulusParam: {},
      types: ["bar", "annulus", "grating"],
      useDefault: false
    };
  },
  computed: {
    currentStimmulusType() {
      if (this.stimmulus.stimmulusType) return this.stimmulus.stimmulusType;
      else return null;
    },
    typeErrors() {
      const errors = [];
      if (!this.$v.stimmulus.stimmulusType.$dirty) return errors;
      !this.$v.stimmulus.stimmulusType.required &&
        errors.push("Required field.");
      return errors;
    },
    timeErrors() {
      const errors = [];
      if (!this.$v.stimmulus.stabilizationTime.$dirty) return errors;
      !this.$v.stimmulus.stabilizationTime.required &&
        errors.push("Required field.");
      !this.$v.stimmulus.stabilizationTime.decimal &&
        errors.push("Must be a numeric value");
      return errors;
    },
    ...mapState("parameters", ["stimmulusDone"])
  },
  watch: {
    currentStimmulusType: {
      handler() {
        if (!this.currentStimmulusType) this.stimmulusParam = {};
        else if (this.currentStimmulusType === "bar") {
          this.stimmulusParam = {
            bar_speed: 1,
            bar_width: 400,
            bar_x_init: 0
          };
        } else if (this.currentStimmulusType === "annulus") {
          //aun no se
          this.stimmulusParam = {};
        } else if (this.currentStimmulusType === "grating") {
          //aun no se
          this.stimmulusParam = {};
        } else {
          this.stimmulusParam = {};
        }
      }
    },
    useDefault: {
      handler() {
        //console.log("change");
        if (this.useDefault) {
          this.getDefaultItem();

          let payload = {
            paramsObject: this.stimmulus,
            stimmulusParam: this.stimmulusParam
          };
          this.$store.dispatch("parameters/setStimmulus", payload);

          this.$store.dispatch("parameters/stimmulusDone", true);
        } else {
          this.getEmptyItem();
          this.$store.dispatch("parameters/stimmulusDone", false);
        }
      }
    }
  },
  mounted() {
    this.getEmptyItem();
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //this.useDefault ? this.getDefaultItem() : this.getEmptyItem();
      //console.log(this.stimmulus);
      this.dialog = true;
    },
    closeDialog() {
      this.$v.$reset();
      this.dialog = false;
    },
    confirmParams() {
      //aqui asociar el param
      //send: payload -> params Object and stimmulusParam
      this.$v.$touch();
      if (!this.$v.$invalid) {
        let payload = {
          paramsObject: this.stimmulus,
          stimmulusParam: this.stimmulusParam
        };
        this.$store.dispatch("parameters/setStimmulus", payload).then(() => {
          this.$v.$reset();
          this.dialog = false;
        });
      } else {
        this.$store.dispatch("parameters/stimmulusDone", false);
      }
    },
    //case1: creating empty item
    getEmptyItem() {
      this.stimmulus = {
        stimmulusType: "",
        stabilizationTime: ""
      };
    },
    getDefaultItem() {
      this.stimmulus = {
        stimmulusType: "bar", //opciones: bar, annulus y grating. De estos depende el siguiente parametro. el parametro debe ser obteniudo con un metodo
        stabilizationTime: 100.0 //float positivo
      };
      this.stimmulusParam = {
        bar_speed: 1,
        bar_width: 400,
        bar_x_init: 0
      };
    }
  }
};
</script>

<style></style>
