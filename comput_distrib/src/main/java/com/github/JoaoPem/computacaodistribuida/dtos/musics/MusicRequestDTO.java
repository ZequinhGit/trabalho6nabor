package com.github.JoaoPem.computacaodistribuida.dtos.musics;

import jakarta.validation.constraints.NotBlank;

public record MusicRequestDTO(

        @NotBlank
        String name,

        @NotBlank
        String artist

) {
}
