package com.github.JoaoPem.computacaodistribuida.mappers;

import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicRequestDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicResponseDTO;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import org.mapstruct.Mapper;

import java.util.List;

@Mapper(componentModel = "spring")
public interface MusicMapper {

    Music toEntity(MusicRequestDTO musicRequestDTO);

    MusicResponseDTO toDto(Music music);

    List<MusicResponseDTO> toDtoList(List<Music> musicList);
}
