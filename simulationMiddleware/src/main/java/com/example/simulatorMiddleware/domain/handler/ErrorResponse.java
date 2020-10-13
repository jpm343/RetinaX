package com.example.simulatorMiddleware.domain.handler;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.time.LocalDateTime;
import java.util.List;

public class ErrorResponse {
    private final int code;
    private final String message;
    private final List<String> errors;
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd-MM-yyyy hh:mm:ss")
    private final LocalDateTime timestamp;

    ErrorResponse(final int code, final String message, final List<String> errors,
                  final LocalDateTime timestamp) {
        super();
        this.code = code;
        this.message = message;
        this.errors = errors;
        this.timestamp = timestamp;
    }

    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public List<String> getErrors() {
        return errors;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

}
