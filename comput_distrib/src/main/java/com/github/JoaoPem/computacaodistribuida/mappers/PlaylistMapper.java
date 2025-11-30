package com.github.JoaoPem.computacaodistribuida.mappers;

import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistRequestDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.models.UserAccount;
import com.github.JoaoPem.computacaodistribuida.repositories.MusicRepository;
import com.github.JoaoPem.computacaodistribuida.repositories.UserAccountRepository;
import lombok.RequiredArgsConstructor;
import org.mapstruct.Mapper;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@Mapper(componentModel = "spring")
public abstract class PlaylistMapper {

    @Autowired
    protected UserAccountRepository userAccountRepository;

    @Autowired
    protected MusicRepository musicRepository;

    public Playlist toEntity(PlaylistRequestDTO playlistRequestDTO) {
        Playlist playlist = new Playlist();
        playlist.setName(playlistRequestDTO.name());

        UserAccount user = userAccountRepository.findById(playlistRequestDTO.userId())
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado com ID " + playlistRequestDTO.userId()));
        playlist.setUser(user);

        List<Music> musics = musicRepository.findAllById(playlistRequestDTO.musicIds());
        if (musics.size() != playlistRequestDTO.musicIds().size()) {
            throw new RuntimeException("Alguma música não foi encontrada");
        }
        playlist.setMusicList(musics);

        return playlist;
    }

    public PlaylistResponseDTO toDto(Playlist playlist) {
        return new PlaylistResponseDTO(
                playlist.getId(),
                playlist.getName(),
                playlist.getUser().getName(),
                playlist.getMusicList().stream().map(Music::getName).toList()
        );
    }

    public List<PlaylistResponseDTO> toDtoList(List<Playlist> playlistList){
        return playlistList.stream()
                .map(this::toDto)
                .toList();
    }
}
