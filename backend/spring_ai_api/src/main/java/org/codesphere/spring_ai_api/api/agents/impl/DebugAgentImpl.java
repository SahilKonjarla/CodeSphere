package org.codesphere.spring_ai_api.api.agents.impl;

import org.codesphere.spring_ai_api.api.agents.DebugAgent;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.InMemoryChatMemory;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.stereotype.Component;

@Component
public class DebugAgentImpl implements DebugAgent {

    // Define debug generation
    private final ChatClient DebugRes;

    // Define response critique
    private final ChatClient CritiqueAgent;

    @Override
    public String debugCode(ChatModel chatModel, String message, String user_id) {
        this.DebugRes = ChatClient.builder(chatModel)
                .defaultSystem("""
                        
                        """)
                .defaultAdvisors(new MessageChatMemoryAdvisor(new InMemoryChatMemory()))
                .build();
    }
}
