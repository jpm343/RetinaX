package com.example.simulatorMiddleware.mapper;

import com.example.simulatorMiddleware.domain.model.HeatMapDataResponse;
import com.example.simulatorMiddleware.domain.model.SimulationResult;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface HeatMapDataMapper {

    HeatMapDataResponse mapToHeatMapDataResponse(SimulationResult result);
}
