package org.codesphere.spring_ai_api.api.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@NoArgsConstructor
public class TestingRequest {
    @Getter
    @Setter
    String user_id;
    String code;

    @Override
    public String toString() {
        return "TestingRequest{" +
                "user_id='" + user_id + '\'' +
                "code='" + code + '\'' +
                "}";
    }
}
