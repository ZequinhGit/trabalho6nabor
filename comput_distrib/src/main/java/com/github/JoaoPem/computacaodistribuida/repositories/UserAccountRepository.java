package com.github.JoaoPem.computacaodistribuida.repositories;

import com.github.JoaoPem.computacaodistribuida.models.UserAccount;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserAccountRepository extends JpaRepository<UserAccount, Long> {

}
