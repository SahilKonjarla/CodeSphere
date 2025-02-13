package org.codesphere.spring_ai_api.api.controller;

import org.codesphere.spring_ai_api.api.model.DebugModel;
import org.codesphere.spring_ai_api.service.DebugService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class DebugController {

    private final DebugService debugService;

    @Autowired
    public DebugController(DebugController debugService) {this.debugService = debugService;}

    @CrossOrigin(origins = "http://localhost:3000")
    @GetMapping("/codesphere/api/v2/debug")
    public Map<String, Object> debug(@RequestParam String message, @RequestParam String user_id) {
        List<DebugModel> res = debugService.getDebug(user_id, message);

        Map<String, Object> debug = new HashMap<>();
        debug.put("user_id", user_id);
        debug.put("message", res);

        return debug;
    }
}
