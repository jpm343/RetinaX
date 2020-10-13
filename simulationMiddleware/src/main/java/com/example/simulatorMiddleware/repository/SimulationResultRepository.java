package com.example.simulatorMiddleware.repository;

import com.example.simulatorMiddleware.domain.model.SimulationResult;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface SimulationResultRepository extends MongoRepository<SimulationResult, String> {
}
