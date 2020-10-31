<template>
  <div>
    <v-dialog v-model="dialog" max-width="650px">
      <v-card>
        <v-card-title>
          <span class="headline">Amacrine cells</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.amacrine.ndend"
                  label="Dendrites number"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.amacrine.dendseg"
                  label="Dendrites segments"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.amacrine.diam_min"
                  label="Minimum dendrite diameter"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.amacrine.diam_max"
                  label="Maximum dendrite diameter"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.amacrine.pref_dend"
                  label="Preferred dendrite"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="results.amacrine.null_dend"
                  label="Null dendrite (opposite to preferred)"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.amacrine.dend_input_segments"
                  label="Segments with bipolar input"
                  type="number"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.amacrine.sac_sac_segments"
                  label="Segments with SAC input"
                  type="number"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="results.amacrine.area_thresh"
                  label="Threshold of area overlap for SAC-SAC synapse"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          <span class="headline">Bipolar cells</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.bipolar.d_is"
                  label="Distance between synaptic input"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.bipolar.excGmax"
                  label="Maximum excitatory conductance"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.bipolar.excGmin"
                  label="Minimum excitatory conductance"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="results.bipolar.synapse_type"
                  label="Synapse type"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.bipolar.BPsyn_tau"
                  label="Time constants of synapse"
                  type="number"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.bipolar.BPtau1"
                  label="Time constants of BPexc"
                  type="number"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.bipolar.BPtau2"
                  label="Time constants of BPexc 2"
                  type="number"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          <span class="headline">Gabaergic function</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.gabaeric.k1"
                  label="K1 variable"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.gabaeric.k2"
                  label="K2 variable"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.gabaeric.th1"
                  label="TH1 variable"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.gabaeric.th2"
                  label="TH2 variable"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.gabaeric.gabaGmin"
                  label="Minimum GABA conductance"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.gabaeric.gabaGmax"
                  label="Maximum GABA conductance"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          <span class="headline">Neuron</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.neuron.tstop"
                  label="Simulation time (ms)"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex>
                <v-switch
                  readonly
                  v-model="results.neuron.cvode_active"
                  :label="
                    `Is CVODE active?: ${
                      results.neuron.cvode_active ? 'yes' : 'no'
                    }`
                  "
                ></v-switch>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.neuron.cvode_tolerance"
                  label="CVODE Tolerance"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.neuron.v_init"
                  label="Initial membrane voltage"
                  type="number"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          <span class="headline">Recording vectors</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-combobox
                  v-model="results.recording.amac_rec"
                  label="Amacrine number to record"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="results.recording.sec_rec"
                  attach
                  chips
                  label="Section to record in cell"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.recording.var_amac_rec"
                  label="Amacrine variable to record (e.g., ‘v’)"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.recording.x_rec"
                  label="Position where to record within NEURON section [0, 1]"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
              <v-flex xs12>
                <v-combobox
                  v-model="results.recording.var_syn_rec"
                  label="Synaptic variable to record (e.g. ’sc2’)"
                  multiple
                  chips
                  readonly
                ></v-combobox>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          <span class="headline">Stimulus</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field
                  v-model="results.stimmulus.stimulus_type"
                  chips
                  label="Stimulus type"
                  readonly
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model.number="results.stimmulus.t_es"
                  label="Stabilization time (ms)"
                  type="float"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-divider></v-divider>
            <v-layout wrap>
              <!--this must be fixed-->
              <span class="headline">Stimulus params</span>
              <v-flex
                v-for="(item, key, index) in results.stimmulus.stim_param"
                :key="index"
                xs12
              >
                <v-text-field
                  readonly
                  v-model.number="results.stimmulus.stim_param[key]"
                  :label="key"
                  type="number"
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
      <v-btn color="error" @click="closeDialog">Close</v-btn>
    </v-dialog>
    <v-tooltip top>
      <template v-slot:activator="{ on }">
        <v-btn
          small
          depressed
          outlined
          icon
          fab
          dark
          color="info"
          @click="dialog = true"
          v-on="on"
        >
          <v-icon>mdi-code-json</v-icon>
        </v-btn>
      </template>
      <span>Simulation parameters</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  props: {
    results: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dialog: false
    };
  },
  methods: {
    openDialog() {
      //this is where I should get the item copy
      //by now:
      //console.log(this.results);
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    }
  }
};
</script>

<style></style>
