package com.example.simulatorMiddleware.domain.command;

import lombok.Value;

import java.util.List;

@Value
public class HeatMapDataCommand {
    static final List<String> validVariables = List.of("DSsc", "DSsca", "DSvd", "scp", "scpa", "vp");
    static final List<String> validParameters = List.of(
            "ndend", "dendseg", "diam_min","diam_max","area_thresh",
            "k1","k2","th1","th2","gabaGmin","gabaGmax",
            "d_is", "excGmax", "excGmin",
            "bar_speed", "bar_width", "bar_x_init",
            "tstop", "cvode_tolerance", "v_init"
    );
    static final List<String> validLocations = List.of(
            "amacrine", "gabaeric", "bipolar", "stimmulus.stim_param", "neuron"
    );
    String variable;
    String xParameter;
    String xParameterLocation;
    String yParameter;
    String yParameterLocation;

    public Boolean isValid() {
        return validVariables.contains(variable) &&
                validParameters.contains(xParameter) &&
                validParameters.contains(yParameter) &&
                validLocations.contains(xParameterLocation) &&
                validLocations.contains(yParameterLocation) &&
                !yParameter.equals(xParameter);
    }
}
