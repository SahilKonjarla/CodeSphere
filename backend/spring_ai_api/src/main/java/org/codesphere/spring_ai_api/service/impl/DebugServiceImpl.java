package org.codesphere.spring_ai_api.service.impl;

import org.codesphere.spring_ai_api.service.DebugService;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
public class DebugServiceImpl implements DebugService {

    @Async
    public CompletableFuture<List<DebugModel>> getDebug(String message, String user_id) {

    }
}
