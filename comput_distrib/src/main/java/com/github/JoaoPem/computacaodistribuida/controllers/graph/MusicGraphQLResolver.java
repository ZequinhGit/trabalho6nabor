package com.github.JoaoPem.computacaodistribuida.controllers.graph;

import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicResponseDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.mappers.MusicMapper;
import com.github.JoaoPem.computacaodistribuida.mappers.PlaylistMapper;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.services.MusicService;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import lombok.RequiredArgsConstructor;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class MusicGraphQLResolver {

    private final MusicService musicService;
    private final MusicMapper musicMapper;
    private final PlaylistService playlistService;
    private final PlaylistMapper playlistMapper;

    @QueryMapping
    public List<MusicResponseDTO> allMusics() {
        List<Music> musicList = musicService.listAllMusics();
        return musicMapper.toDtoList(musicList);
    }

    @QueryMapping
    public List<PlaylistResponseDTO> playlistsByMusic(@Argument Long musicId) {
        List<Playlist> playlistList = playlistService.listPlaylistsByMusicId(musicId);
        return playlistMapper.toDtoList(playlistList);
    }

}
