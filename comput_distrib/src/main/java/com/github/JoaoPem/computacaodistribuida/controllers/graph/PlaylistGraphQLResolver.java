package com.github.JoaoPem.computacaodistribuida.controllers.graph;

import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicResponseDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.mappers.MusicMapper;
import com.github.JoaoPem.computacaodistribuida.mappers.PlaylistMapper;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import lombok.RequiredArgsConstructor;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class PlaylistGraphQLResolver {

    private final PlaylistService playlistService;
    private final PlaylistMapper playlistMapper;
    private final MusicMapper musicMapper;

    @QueryMapping
    public List<PlaylistResponseDTO> allPlaylists() {
        List<Playlist> playlistList = playlistService.listAllPlaylists();
        return playlistMapper.toDtoList(playlistList);
    }

    @QueryMapping
    public List<MusicResponseDTO> musicsByPlaylist(@Argument Long playlistId) {
        List<Music> musicList = playlistService.listMusicsByPlaylistId(playlistId);
        return musicMapper.toDtoList(musicList);
    }

}
