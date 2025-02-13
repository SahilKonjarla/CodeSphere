package org.codesphere.spring_ai_api.api.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
public class DebugModel {
    @Getter
    @Setter
    String user_id;
    String message;

    @Override
    public String toString() {
        return "DebugRequest{" +
                "user_id='" + user_id + '\'' +
                "code='" + message + '\'' +
                '}';
    }
}
