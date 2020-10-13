package com.example.simulatorMiddleware.domain.handler;

import com.example.simulatorMiddleware.domain.exception.SimulationErrorException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

@ControllerAdvice
public class ExceptionHandlingController extends ResponseEntityExceptionHandler {
    private static final Logger LOG = LoggerFactory.getLogger(ExceptionHandlingController.class);

    @Override
    protected ResponseEntity<Object> handleHttpMessageNotReadable(HttpMessageNotReadableException ex,
                                                                  HttpHeaders headers, HttpStatus status, WebRequest request) {
        String message = "Invalid request structure";
        return buildResponseEntity(HttpStatus.BAD_REQUEST, message, ex.getMessage());
    }

    @Override
    protected ResponseEntity<Object> handleExceptionInternal(Exception ex, Object body, HttpHeaders headers,
                                                             HttpStatus status, WebRequest request) {
        var responseEntity = super.handleExceptionInternal(ex, body, headers, status, request);

        if (body == null) {
            ErrorResponse errorResponse = new ErrorResponse(status.value(), status.getReasonPhrase(),
                    List.of(ex.getMessage()), LocalDateTime.now());
            return new ResponseEntity<>(errorResponse, responseEntity.getHeaders(), responseEntity.getStatusCode());
        }

        return responseEntity;
    }

    @ExceptionHandler({ SimulationErrorException.class })
    public ResponseEntity<Object> handleOperationException(SimulationErrorException ex) {
        final HttpStatus status = HttpStatus.valueOf(Integer.parseInt(ex.getCode()));
        final String message = ex.getMessage();

        LOG.info("handleOperationException|status={}, message={}, class={}", status, message,
                ex.getClass().getSimpleName());

        return buildResponseEntity(status, message,
                ex.getLocalizedMessage());
    }

    private ResponseEntity<Object> buildResponseEntity(HttpStatus status, String message, String error) {
        List<String> errors = Collections.singletonList(error);
        return buildResponseEntity(status, message, errors);
    }

    private ResponseEntity<Object> buildResponseEntity(HttpStatus status, String message, List<String> error) {
        ErrorResponse schemaError = new ErrorResponse(status.value(), message, error, LocalDateTime.now());
        return new ResponseEntity<>(schemaError, status);
    }

}
