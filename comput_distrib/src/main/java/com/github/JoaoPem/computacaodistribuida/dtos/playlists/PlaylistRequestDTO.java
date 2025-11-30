package com.github.JoaoPem.computacaodistribuida.dtos.playlists;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.util.List;

public record PlaylistRequestDTO(

        @NotBlank
        String name,

        @NotNull
        Long userId,

        @NotEmpty
        List<Long> musicIds

) {
}
