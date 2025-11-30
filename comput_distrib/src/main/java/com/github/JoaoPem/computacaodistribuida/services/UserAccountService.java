package com.github.JoaoPem.computacaodistribuida.services;

import com.github.JoaoPem.computacaodistribuida.models.UserAccount;
import com.github.JoaoPem.computacaodistribuida.repositories.UserAccountRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserAccountService {

    private final UserAccountRepository userAccountRepository;

    public UserAccount createUserAccount(UserAccount userAccount) {
        return userAccountRepository.save(userAccount);
    }

    public List<UserAccount> listAllUserAccount() {
        return userAccountRepository.findAll();
    }
}
