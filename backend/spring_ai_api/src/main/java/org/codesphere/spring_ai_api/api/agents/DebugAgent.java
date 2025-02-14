package org.codesphere.spring_ai_api.api.agents;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Component;

@Component
public interface DebugAgent {

    // Stating the Debugging Agent
    String debugCode(String message, String user_id);

}
