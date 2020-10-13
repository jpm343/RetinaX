package com.example.simulatorMiddleware.presntation.dto;

import com.example.simulatorMiddleware.domain.model.SimulationParameters;
import lombok.Value;

@Value
public class SimulationResultResponse {
    String id;
    String createdDate;
    String elapsedTime;
    SimulationParameters parameters;


}
