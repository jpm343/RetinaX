package com.example.simulatorMiddleware.presntation;

import com.example.simulatorMiddleware.domain.command.HeatMapDataCommand;
import com.example.simulatorMiddleware.domain.exception.SimulationErrorException;
import com.example.simulatorMiddleware.domain.model.HeatMapDataEntry;
import com.example.simulatorMiddleware.domain.model.SimulationParameters;
import com.example.simulatorMiddleware.domain.model.SimulationResult;
import com.example.simulatorMiddleware.presntation.dto.SimulationResultForHeatMap;
import com.example.simulatorMiddleware.presntation.dto.SimulationResultResponse;
import com.example.simulatorMiddleware.repository.SimulationResultRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Value;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

import static java.util.Map.entry;

@RestController
@CrossOrigin(origins = "*")
public class SimulationResultController {
    private static final Logger LOGGER = LoggerFactory.getLogger(SimulationResultController.class);
    @Value("${simulator.uri}")
    private String pythonURI;

    @Autowired
    private SimulationResultRepository repository;

    //get all simulations
    @GetMapping("/v1/simulations")
    public List<SimulationResultResponse> getAll() {
        LOGGER.info("getAllSimulations | request");
        return repository.findAll().stream().map(SimulationResult::convertToResponse).collect(Collectors.toList());
    }

    //get full details of a single simulation
    @GetMapping("/v1/simulations/{id}")
    public SimulationResult getSimulationDetails(@PathVariable("id") String simulationResultId) {
        LOGGER.info("getSimulationDetails | request. id={}", simulationResultId );
        Optional<SimulationResult> found = repository.findById(simulationResultId);
        return found.orElse(null);
    }

    //delete one simulation
    @DeleteMapping("/v1/simulations/{id}")
    public void delete(@PathVariable("id") String simulationResultId) {
        LOGGER.info("deleteSimulation | request. id={}", simulationResultId);
        Optional<SimulationResult> found = repository.findById(simulationResultId);
        found.ifPresent(simulationResult -> repository.delete(simulationResult));
    }

    //dispatch python service and save result. It seems that I have to create parameters entity
    @PostMapping("/v1/simulations/runAndSave")
    public SimulationResult create(@RequestBody final SimulationParameters params) {
        LOGGER.info("createSimulation | request. params={}", params);
        //params should be converted to json string
        ObjectMapper mapper = new ObjectMapper();
        String paramsJson = "";
        try {
            paramsJson = mapper.writeValueAsString(params);
        } catch(IOException e) {
            LOGGER.error(e.getMessage());
        }

        //send json to python flask API
        LOGGER.info("createSimulation | sending to python API. URI={}", pythonURI);
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");

        HttpEntity<String> entity =  new HttpEntity<>(paramsJson, headers);

        Map results;
        try {
            results = restTemplate.postForObject(pythonURI, entity, Map.class);
        } catch (HttpClientErrorException | HttpServerErrorException httpClientOrServerExc) {
            throw new SimulationErrorException(HttpStatus.BAD_REQUEST, "Simulation error occurred. Check your parameters and try again");
        } catch (ResourceAccessException exc) {
            throw new SimulationErrorException(HttpStatus.SERVICE_UNAVAILABLE, "Connection to simulator service on URI=" + pythonURI + " failed. Is it running?");
        }


        //with results -> build SimulationResult and return
        LOGGER.info("createSimulation | receiving from python API. URI={}", pythonURI);
        List parsedResults = parseResults(results);
        Map<String, List> plotData = extractPlotData(results);
        SimulationResult simulationResult = new SimulationResult(results, parsedResults, plotData, params);
        LOGGER.info("createSimulation | saved result");
        return repository.save(simulationResult);
    }

    //get heatmap data

    @PostMapping("/v1/simulations/getHeatMapData")
    public List<HeatMapDataEntry> getHeatMapData(@RequestBody final HeatMapDataCommand heatMapDataCommand) {
        LOGGER.info("getHeatMapData | request. heatMapDataCommand={}", heatMapDataCommand);
        if (heatMapDataCommand.isValid()) {
            String yParamLocation = heatMapDataCommand.getYParameterLocation();
            String yParamKey = heatMapDataCommand.getYParameter();
            String xParamLocation = heatMapDataCommand.getXParameterLocation();
            String xParamKey = heatMapDataCommand.getXParameter();

            List<SimulationResultForHeatMap> results = repository.findAll().stream().map(SimulationResult::convertToHeatMapResponse).collect(Collectors.toList());
            //make unique yParameterValues
            LOGGER.info("getHeatMapData | MAKING UNIQUE SIM VECTORS. ");
            Set<SimulationResultForHeatMap> uniquesY = new HashSet<>();
            Set<SimulationResultForHeatMap> uniquesX = new HashSet<>();



            HashSet<String> seenYValues = new HashSet<>();
            HashSet<String> seenXValues = new HashSet<>();
            for (SimulationResultForHeatMap result : results) {
                String yValue = result.getParameters().getMapByLocationString(yParamLocation).get(yParamKey).toString();
                String xValue = result.getParameters().getMapByLocationString(xParamLocation).get(xParamKey).toString();
                if (!seenYValues.contains(yValue)) {
                    uniquesY.add(result);
                    seenYValues.add(yValue);
                }
                if (!seenXValues.contains(xValue)) {
                    uniquesX.add(result);
                    seenXValues.add(xValue);
                }
            }

            LOGGER.info("getHeatMapData | PREPARING ENTRIES. ");
            //prepare entries list
            List<HeatMapDataEntry> entries = new ArrayList<>();

            //iterate over Y simulations
            for (SimulationResultForHeatMap yResult : uniquesY) {
                //build X entries for Y entry
                List<Map<String, Object>> xEntries = new ArrayList<>();
                String yParamValue = yResult.getParameters().getMapByLocationString(yParamLocation).get(yParamKey).toString();
                for (SimulationResultForHeatMap xResult : uniquesX) {
                    //check if simulation exists for given combination (X,Y)
                    String xParamValue = xResult.getParameters().getMapByLocationString(xParamLocation).get(xParamKey).toString();

                    Map<String, Object> possibleResults = Map.of();

                    for (SimulationResultForHeatMap sim : results ) {
                        boolean containsX = sim.getParameters().getMapByLocationString(xParamLocation).get(xParamKey).toString().equals(xParamValue);
                        boolean containsY = sim.getParameters().getMapByLocationString(yParamLocation).get(yParamKey).toString().equals(yParamValue);
                        if (containsX && containsY) {
                            possibleResults = sim.getResults();
                            break;
                        }
                    }

                    Map<String, Object> xEntry = Map.ofEntries(
                            entry("x", xParamValue),
                            entry("y", possibleResults)
                    );
                    xEntries.add(xEntry);
                }
                //build Y entry
                HeatMapDataEntry entry = new HeatMapDataEntry(yParamValue, xEntries);

                //append to entries
                entries.add(entry);
            }
            LOGGER.info("getHeatMapData | RETURNING ENTRIES. ");
            return entries;
        } else {
            LOGGER.info("getHeatMapData | COMMAND NOT VALID. ");
            return Collections.emptyList();
        }
    }




    private Map<String, List> extractPlotData(@NonNull Map<String, Object> results) {
        // names of object fields on python service
        LOGGER.info("PRIVATE: extractPlotData | init. ");
        final String timeRecName = "timeRec";
        final String amacVecName = "amacVecs";
        final String synapseVecName = "synapseVecs";
        final String cellLabelsName = "cells";

        Object timeRec = results.get(timeRecName);
        Object amacVec = results.get(amacVecName);
        Object synapseVec = results.get(synapseVecName);
        Object cellLabels = results.get(cellLabelsName);

        Map<String, List> returnValue;

        if (timeRec == null || amacVec == null || synapseVec == null || cellLabels == null) {
            LOGGER.info("PRIVATE: extractPlotData | not valid entry. returning... ");
            returnValue = null;
        }
        else {
            returnValue = Map.ofEntries(
                    entry("amacVecs", (List<List<Long>>) amacVec),
                    entry("synapseVecs", (List<List<Long>>) synapseVec),
                    entry("timeRec", (List<Long>) timeRec),
                    entry("cellLabels", (List<String>) cellLabels)
            );
        }

        //remove fields from results
        LOGGER.info("PRIVATE: extractPlotData | removing plot data from original results... ");
        results.remove(timeRecName);
        results.remove(amacVecName);
        results.remove(synapseVecName);
        LOGGER.info("PRIVATE: extractPlotData | returning plot data ");
        return returnValue;
    }

    private List<Map<String, String>> parseResults(@NonNull Map<String, Object> results) {
        List<String> cellsFromParams = (List<String>) results.get("cells");
        if(cellsFromParams == null) return null;
        List<Map<String, String>> parsedResults = new ArrayList<>();

        //high dependency to python format
        int cellsCount = cellsFromParams.size();
        List<String> DSsc = (List<String>) results.get("DSsc");
        List<String> DSsca = (List<String>) results.get("DSsca");
        List<String> DSvd = (List<String>) results.get("DSvd");
        List<String> scp = (List<String>) results.get("scp");
        List<String> scpa = (List<String>) results.get("scpa");
        List<String> vp = (List<String>) results.get("vp");



        for (int i = 0; i < cellsCount; i ++) {
            //String name =  (cellsFromParams.get(i));
            Map<String, String> entry = Map.ofEntries(
                    entry("name", cellsFromParams.get(i)),
                    entry("DSsc", String.valueOf(DSsc.get(i))),
                    entry("DSsca", String.valueOf(DSsca.get(i))),
                    entry("DSvd", String.valueOf(DSvd.get(i))),
                    entry("scp", String.valueOf(scp.get(i))),
                    entry("scpa", String.valueOf(scpa.get(i))),
                    entry("vp", String.valueOf(vp.get(i)))
            );
            parsedResults.add(entry);
        }

        return parsedResults;
    }
}
