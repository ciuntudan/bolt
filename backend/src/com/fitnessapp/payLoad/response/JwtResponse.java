package com.fitnessapp.payload.response;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class JwtResponse {
    private String token;
    private String type = "Bearer";
    private Long id;
    private String name;
    private String email;
    private String avatar;
    private List<String> roles;

    public JwtResponse(String token, Long id, String name, String email, String avatar, List<String> roles) {
        this.token = token;
        this.id = id;
        this.name = name;
        this.email = email;
        this.avatar = avatar;
        this.roles = roles;
    }
}
