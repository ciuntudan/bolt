package com.fitnessapp.controller;

import com.fitnessapp.model.ERole;
import com.fitnessapp.model.Role;
import com.fitnessapp.model.User;
import com.fitnessapp.payload.request.LoginRequest;
import com.fitnessapp.payload.request.SignupRequest;
import com.fitnessapp.payload.response.JwtResponse;
import com.fitnessapp.payload.response.MessageResponse;
import com.fitnessapp.repository.RoleRepository;
import com.fitnessapp.repository.UserRepository;
import com.fitnessapp.security.jwt.JwtUtils;
import com.fitnessapp.security.services.UserDetailsImpl;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@CrossOrigin(origins = "http://localhost:3000", maxAge = 3600, allowCredentials = "true")
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);

    @Autowired
    AuthenticationManager authenticationManager;

    @Autowired
    UserRepository userRepository;

    @Autowired
    RoleRepository roleRepository;

    @Autowired
    PasswordEncoder encoder;

    @Autowired
    JwtUtils jwtUtils;

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {
        logger.info("Login attempt for email: {}", loginRequest.getEmail());

        try {
            // Check if user exists in the database
            if (!userRepository.existsByEmail(loginRequest.getEmail())) {
                logger.warn("Login failed: User with email {} does not exist", loginRequest.getEmail());
                return ResponseEntity.badRequest().body(new MessageResponse("Error: Invalid email or password"));
            }

            // Try to authenticate
            Authentication authentication = authenticationManager
                    .authenticate(new UsernamePasswordAuthenticationToken(loginRequest.getEmail(), loginRequest.getPassword()));

            // Update security context if authentication was successful
            SecurityContextHolder.getContext().setAuthentication(authentication);

            // Generate JWT cookie
            UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getPrincipal();
            ResponseCookie jwtCookie = jwtUtils.generateJwtCookie(userDetails);

            // Get user roles
            List<String> roles = userDetails.getAuthorities().stream()
                    .map(item -> item.getAuthority())
                    .collect(Collectors.toList());

            logger.info("User {} logged in successfully", loginRequest.getEmail());

            // Return user details with JWT
            return ResponseEntity.ok().header(HttpHeaders.SET_COOKIE, jwtCookie.toString())
                    .body(new JwtResponse(jwtCookie.getValue(),
                            userDetails.getId(),
                            userDetails.getName(),
                            userDetails.getUsername(),
                            userDetails.getAvatar(),
                            roles));
        } catch (Exception e) {
            logger.error("Authentication error: {}", e.getMessage());
            return ResponseEntity.badRequest().body(new MessageResponse("Error: Invalid email or password"));
        }
    }

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@Valid @RequestBody SignupRequest signUpRequest) {
        logger.info("Registration attempt for email: {}", signUpRequest.getEmail());

        if (userRepository.existsByEmail(signUpRequest.getEmail())) {
            logger.warn("Registration failed: Email {} is already in use", signUpRequest.getEmail());
            return ResponseEntity.badRequest().body(new MessageResponse("Error: Email is already in use!"));
        }

        try {
            // Create new user's account
            User user = new User(
                    signUpRequest.getName(),
                    signUpRequest.getEmail(),
                    encoder.encode(signUpRequest.getPassword()));

            // Generate random avatar
            user.setAvatar("https://i.pravatar.cc/150?u=" + signUpRequest.getEmail());

            // Check if roles exist in the database
            Role userRole = roleRepository.findByName(ERole.ROLE_USER)
                    .orElseThrow(() -> new RuntimeException("Error: Role not found."));
            
            Set<Role> roles = new HashSet<>();
            roles.add(userRole);
            user.setRoles(roles);

            // Save user to database
            userRepository.save(user);
            logger.info("User registered successfully: {}", signUpRequest.getEmail());

            // Login after registration
            Authentication authentication = authenticationManager
                    .authenticate(new UsernamePasswordAuthenticationToken(signUpRequest.getEmail(), signUpRequest.getPassword()));

            SecurityContextHolder.getContext().setAuthentication(authentication);

            UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getPrincipal();

            ResponseCookie jwtCookie = jwtUtils.generateJwtCookie(userDetails);

            List<String> userRoles = userDetails.getAuthorities().stream()
                    .map(item -> item.getAuthority())
                    .collect(Collectors.toList());

            return ResponseEntity.ok().header(HttpHeaders.SET_COOKIE, jwtCookie.toString())
                    .body(new JwtResponse(jwtCookie.getValue(),
                            userDetails.getId(),
                            userDetails.getName(),
                            userDetails.getUsername(),
                            userDetails.getAvatar(),
                            userRoles));
        } catch (Exception e) {
            logger.error("Registration error: {}", e.getMessage());
            return ResponseEntity.badRequest().body(new MessageResponse("Error during registration: " + e.getMessage()));
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logoutUser() {
        ResponseCookie cookie = jwtUtils.getCleanJwtCookie();
        logger.info("User logged out");
        return ResponseEntity.ok().header(HttpHeaders.SET_COOKIE, cookie.toString())
                .body(new MessageResponse("You've been signed out!"));
    }
}