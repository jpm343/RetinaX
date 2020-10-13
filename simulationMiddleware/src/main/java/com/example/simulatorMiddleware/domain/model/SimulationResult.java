package com.example.simulatorMiddleware.domain.model;

import com.example.simulatorMiddleware.presntation.dto.SimulationResultForHeatMap;
import com.example.simulatorMiddleware.presntation.dto.SimulationResultResponse;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.TimeZone;

@Document(collection = "simulationResults")
@Getter
@Setter
public class SimulationResult {
    @Id
    private String id;

    private String createdDate;

    private String elapsedTime;

    //json object not specified
    private Map<String, Object> results;
    private List<Map<String, String>> parsedResults;

    @Transient
    private Map<String, List> plotData;

    private SimulationParameters parameters;

    public SimulationResult() {

    }

    public SimulationResult(Map<String, Object> results, List<Map<String, String>> parsedResults, Map<String, List> plotData, SimulationParameters parameters) {
        this.results = results;
        this.parameters = parameters;
        this.parsedResults = parsedResults;
        this.plotData = plotData;
        this.elapsedTime = ((String) results.get("simulationTime"));
        this.createdDate = this.getTimeStamp();
    }

    @Override
    public String toString() {
        return "SimulationResult{" +
                "id='" + id + '\'' +
                ", createdDate='" + createdDate + '\'' +
                ", elapsedTime='" + elapsedTime + '\'' +
                ", results=" + results +
                ", parsedResults=" + parsedResults +
                ", plotData=" + plotData +
                ", parameters=" + parameters +
                '}';
    }

    private String getTimeStamp() {
        TimeZone tz = TimeZone.getTimeZone("UTC");
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm'Z'");
        df.setTimeZone(tz);
        return df.format(new Date());
    }

    public SimulationResultResponse convertToResponse() {
        return new SimulationResultResponse(
                this.id,
                this.createdDate,
                this.elapsedTime,
                this.parameters
        );
    }

    public SimulationResultForHeatMap convertToHeatMapResponse() {
        return new SimulationResultForHeatMap(
                this.id,
                this.parameters,
                this.results
        );
    }
}


