package com.example.simulatorMiddleware.domain.model;

import lombok.Getter;
import lombok.Setter;

import java.util.List;
import java.util.Map;

@Getter
@Setter
public class HeatMapDataEntry {
    private String yLabel;
    private List<Map<String, Object>> data;

    public HeatMapDataEntry(String yLabel, List<Map<String, Object>> data) {
        this.yLabel = yLabel;
        this.data = data;
    }
}
