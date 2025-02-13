package org.codesphere.spring_ai_api.service;

import org.codesphere.spring_ai_api.api.model.DebugModel;
import org.springframework.scheduling.annotation.Async;

import java.util.List;
import java.util.concurrent.CompletableFuture;

public interface DebugService {
    @Async
    CompletableFuture<List<DebugModel>> getDebug(String message, String user_id);
}
