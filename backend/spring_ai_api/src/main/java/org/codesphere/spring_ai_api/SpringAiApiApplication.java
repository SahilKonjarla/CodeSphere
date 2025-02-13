package org.codesphere.spring_ai_api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class SpringAiApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringAiApiApplication.class, args);
	}

}