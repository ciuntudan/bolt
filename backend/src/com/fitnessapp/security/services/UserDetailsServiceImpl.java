package com.fitnessapp.security.services;

import com.fitnessapp.model.User;
import com.fitnessapp.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {
    private static final Logger logger = LoggerFactory.getLogger(UserDetailsServiceImpl.class);
    
    @Autowired
    UserRepository userRepository;

    @Override
    @Transactional
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        logger.info("Attempting to load user by email: {}", email);
        
        try {
            User user = userRepository.findByEmail(email)
                    .orElseThrow(() -> {
                        logger.error("User not found with email: {}", email);
                        return new UsernameNotFoundException("User Not Found with email: " + email);
                    });

            logger.info("User found: {}", user.getName());
            return UserDetailsImpl.build(user);
        } catch (Exception e) {
            logger.error("Error loading user by email: {}", e.getMessage());
            throw new UsernameNotFoundException("Error loading user: " + e.getMessage());
        }
    }
}