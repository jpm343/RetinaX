package com.example.simulatorMiddleware.domain.exception;

import com.fasterxml.jackson.annotation.JsonFormat;
import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;

public class SimulationErrorException extends RuntimeException {

    private final String code;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd-MM-yyyy hh:mm:ss")
    private final LocalDateTime timestamp = LocalDateTime.now();


    public SimulationErrorException(final HttpStatus status, final String message) {
        super(message);
        this.code = String.valueOf(status.value());
    }

    public String getCode() {
        return code;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }


}
