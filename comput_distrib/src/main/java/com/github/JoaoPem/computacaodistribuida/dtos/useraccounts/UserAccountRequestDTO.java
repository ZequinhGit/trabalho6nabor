package com.github.JoaoPem.computacaodistribuida.dtos.useraccounts;

import jakarta.validation.constraints.NotBlank;

public record UserAccountRequestDTO(

        @NotBlank
        String name

) {
}
