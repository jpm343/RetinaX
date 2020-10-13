package com.example.simulatorMiddleware.presntation.dto;

import com.example.simulatorMiddleware.domain.model.SimulationParameters;
import lombok.Value;

import java.util.Map;

@Value
public class SimulationResultForHeatMap {
    String id;
    SimulationParameters parameters;
    Map<String, Object> results;
}
