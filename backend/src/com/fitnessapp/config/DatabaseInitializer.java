package com.fitnessapp.config;

import com.fitnessapp.model.ERole;
import com.fitnessapp.model.Role;
import com.fitnessapp.repository.RoleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.Arrays;

@Component
public class DatabaseInitializer implements CommandLineRunner {

    @Autowired
    private RoleRepository roleRepository;

    @Override
    public void run(String... args) {
        // Check if roles exist, if not create them
        if (roleRepository.count() == 0) {
            Arrays.stream(ERole.values()).forEach(role -> {
                Role newRole = new Role();
                newRole.setName(role);
                roleRepository.save(newRole);
            });
            
            System.out.println("Initialized roles in database");
        }
    }
}