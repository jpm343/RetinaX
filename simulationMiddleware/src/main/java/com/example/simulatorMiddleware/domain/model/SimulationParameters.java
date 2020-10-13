package com.example.simulatorMiddleware.domain.model;

import lombok.Getter;
import lombok.Setter;

import java.util.Map;

@Getter
@Setter
public class SimulationParameters {
    private Map<String, Object> amacrine;
    private Map<String, Object> gabaeric;
    private Map<String, Object> bipolar;
    private Map<String, Object> stimmulus;
    private Map<String, Object> recording;
    private Map<String, Object> neuron;
    private Integer dataidx;
    private Float sampinvl;

    public SimulationParameters(Map<String, Object> amacrine, Map<String, Object> gabaeric, Map<String, Object> bipolar, Map<String, Object> stimmulus, Map<String, Object> recording, Map<String, Object> neuron, Integer dataidx, Float sampinvl) {
        this.amacrine = amacrine;
        this.gabaeric = gabaeric;
        this.bipolar = bipolar;
        this.stimmulus = stimmulus;
        this.recording = recording;
        this.neuron = neuron;
        this.dataidx = dataidx;
        this.sampinvl = sampinvl;
    }

    public Map<String, Object> getMapByLocationString(String location) {
        switch (location) {
            case "amacrine":
                return this.amacrine;
            case "gabaeric":
                return this.gabaeric;
            case "bipolar":
                return this.bipolar;
            case "stimmulus.stim_param":
                return (Map<String, Object>)this.stimmulus.get("stim_param");
            case "neuron":
                return this.neuron;
            default:
                return null;
        }
    }
}
