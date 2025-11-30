package com.github.JoaoPem.computacaodistribuida.mappers;

import com.github.JoaoPem.computacaodistribuida.dtos.useraccounts.UserAccountRequestDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.useraccounts.UserAccountResponseDTO;
import com.github.JoaoPem.computacaodistribuida.models.UserAccount;
import org.mapstruct.Mapper;

import java.util.List;

@Mapper(componentModel = "spring")
public interface UserAccountMapper {

    UserAccount toEntity(UserAccountRequestDTO userAccountRequestDTO);

    UserAccountResponseDTO toDto(UserAccount userAccountList);

    List<UserAccountResponseDTO> toDtoList(List<UserAccount> userAccountList);

}
