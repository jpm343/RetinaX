export const namespaced = true;

export const state = {
  //object with parameteres from form components
  params: {
    amacrine: {},
    gabaeric: {},
    bipolar: {},
    stimmulus: {},
    recording: {},
    neuron: {},
    dataidx: 13, //wich file
    sampinvl: 0.1 //float positivo
  },

  amacrineDone: false,
  bipolarDone: false,
  gabaericDone: false,
  neuronDone: false,
  recordingDone: false,
  stimmulusDone: false
  //allDone: false //this should be a computed property based on previous state fields
};

export const mutations = {
  SET_AMACRINE_FIELDS(state, paramsObject) {
    state.params.amacrine = paramsObject;
    state.amacrineDone = true;
  },
  SET_GABAERIC_FIELDS(state, paramsObject) {
    state.params.gabaeric = paramsObject;
    state.gabaericDone = true;
  },
  SET_BIPOLAR_FIELDS(state, paramsObject) {
    state.params.bipolar = paramsObject;
    state.bipolarDone = true;
  },
  SET_STIMMULUS_FIELDS(state, paramsObject) {
    state.params.stimmulus = paramsObject;
    state.stimmulusDone = true;
  },
  SET_RECORDING_FIELDS(state, paramsObject) {
    state.params.recording = paramsObject;
    state.recordingDone = true;
  },
  SET_NEURON_FIELDS(state, paramsObject) {
    state.params.neuron = paramsObject;
    state.neuronDone = true;
  },
  FLUSH_PARAMETERS_STATE(state) {
    state.amacrineDone = false;
    state.bipolarDone = false;
    state.gabaericDone = false;
    state.neuronDone = false;
    state.recordingDone = false;
    state.stimmulusDone = false;
  },
  AMACRINE_IS_READY(state, bool) {
    state.amacrineDone = bool;
  },
  BIPOLAR_IS_READY(state, bool) {
    state.bipolarDone = bool;
  },
  GABAERIC_IS_READY(state, bool) {
    state.gabaericDone = bool;
  },
  NEURON_IS_READY(state, bool) {
    state.neuronDone = bool;
  },
  RECORDING_IS_READY(state, bool) {
    state.recordingDone = bool;
  },
  STIMMULUS_IS_READY(state, bool) {
    state.stimmulusDone = bool;
  }
};

const snackbar = {
  message: "Parameters setted up succesfully",
  color: "success"
};

export const actions = {
  setAmacrineCells({ commit, dispatch }, paramsObject) {
    let amacrine = {
      ndend: paramsObject.dendritesNumber,
      dendseg: paramsObject.dendritesSegments,
      diam_min: paramsObject.minDiameter,
      diam_max: paramsObject.maxDiameter,
      dend_input_segments: paramsObject.segmentsWithBipolarInput,
      sac_sac_segments: paramsObject.segmentsWithSacInput,
      pref_dend: paramsObject.preferedDendrite,
      null_dend: paramsObject.nullDendrite,
      area_thresh: paramsObject.threshold
    };
    commit("SET_AMACRINE_FIELDS", amacrine);
    //dispatch("displaySnackbar", snackbar, { root: true });
  },
  setGabaericFunction({ commit, dispatch }, paramsObject) {
    let gabaeric = {
      k1: paramsObject.k1Variable,
      k2: paramsObject.k2Variable,
      th1: paramsObject.th1Variable,
      th2: paramsObject.th2Variable,
      gabaGmin: paramsObject.gabaGmin,
      gabaGmax: paramsObject.gabaGmax
    };
    commit("SET_GABAERIC_FIELDS", gabaeric);
    //dispatch("displaySnackbar", snackbar, { root: true });
  },
  setBipolarCells({ commit, dispatch }, paramsObject) {
    let bipolar = {
      d_is: paramsObject.synapticDistance,
      excGmax: Number(paramsObject.excitatoryMax),
      excGmin: paramsObject.excitatoryMin,
      synapse_type: paramsObject.synapsisType,
      BPsyn_tau: paramsObject.synapseTimeConstant,
      BPtau1: paramsObject.BPTimeConstant,
      BPtau2: paramsObject.BPTimeConstant2,
      is_spatiotemporal: true //todo: correct this field
    };
    commit("SET_BIPOLAR_FIELDS", bipolar);
    //dispatch("displaySnackbar", snackbar, { root: true });
  },
  setStimmulus({ commit, dispatch }, payload) {
    let paramsObject = payload.paramsObject;
    let stimmulusParam = payload.stimmulusParam;
    let stimmulus = {
      stimulus_type: paramsObject.stimmulusType,
      stim_param: stimmulusParam, //depends on stimulus type
      t_es: paramsObject.stabilizationTime
    };
    commit("SET_STIMMULUS_FIELDS", stimmulus);
    //dispatch("displaySnackbar", snackbar, { root: true });
  },
  setRecordingVector({ commit, dispatch }, paramsObject) {
    let recording = {
      amac_rec: paramsObject.amacrineRecord,
      sec_rec: paramsObject.secRecord,
      x_rec: paramsObject.xRecord,
      var_amac_rec: paramsObject.amacrineVariableRecord,
      var_syn_rec: paramsObject.synapsisVariableRecord
    };
    commit("SET_RECORDING_FIELDS", recording);
    //dispatch("displaySnackbar", snackbar, { root: true });
  },
  setNeuron({ commit, dispatch }, paramsObject) {
    let neuron = {
      tstop: paramsObject.simulationTime,
      cvode_active: paramsObject.cvodeActive,
      cvode_tolerance: paramsObject.cvodeTolerance,
      v_init: paramsObject.initialVoltage
    };
    commit("SET_NEURON_FIELDS", neuron);
    //dispatch("displaySnackbar", snackbar, { root: true });
  },
  flushParameters({ commit }) {
    commit("FLUSH_PARAMETERS_STATE");
  },
  amacrineDone({ commit }, bool) {
    commit("AMACRINE_IS_READY", bool);
  },
  bipolarDone({ commit }, bool) {
    commit("BIPOLAR_IS_READY", bool);
  },
  gabaericDone({ commit }, bool) {
    commit("GABAERIC_IS_READY", bool);
  },
  neuronDone({ commit }, bool) {
    commit("NEURON_IS_READY", bool);
  },
  recordingDone({ commit }, bool) {
    commit("RECORDING_IS_READY", bool);
  },
  stimmulusDone({ commit }, bool) {
    commit("STIMMULUS_IS_READY", bool);
  }
};
