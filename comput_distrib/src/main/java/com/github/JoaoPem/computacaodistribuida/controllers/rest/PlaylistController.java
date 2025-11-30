package com.github.JoaoPem.computacaodistribuida.controllers.rest;

import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicResponseDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistRequestDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.mappers.MusicMapper;
import com.github.JoaoPem.computacaodistribuida.mappers.PlaylistMapper;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/rest/playlists")
@RequiredArgsConstructor
public class PlaylistController {

    private final PlaylistMapper playlistMapper;
    private final PlaylistService playlistService;
    private final MusicMapper musicMapper;

    @PostMapping
    public ResponseEntity<PlaylistResponseDTO> createPlaylist(@RequestBody @Valid PlaylistRequestDTO playlistRequestDTO){
        Playlist playlist = playlistMapper.toEntity(playlistRequestDTO);
        Playlist createdPlaylist = playlistService.createPlaylist(playlist);
        PlaylistResponseDTO playlistResponseDTO = playlistMapper.toDto(createdPlaylist);
        return ResponseEntity.status(HttpStatus.CREATED).body(playlistResponseDTO);
    }

    @GetMapping
    public ResponseEntity<List<PlaylistResponseDTO>> listAllPlaylists(){
        List<Playlist> playlistList = playlistService.listAllPlaylists();
        List<PlaylistResponseDTO> playlistResponseDTOList = playlistMapper.toDtoList(playlistList);
        return ResponseEntity.status(HttpStatus.OK).body(playlistResponseDTOList);
    }

    @GetMapping("/{playlistId}/musics")
    public ResponseEntity<List<MusicResponseDTO>> listMusicsByPlaylist(@PathVariable Long playlistId) {
        List<Music> musicList = playlistService.listMusicsByPlaylistId(playlistId);
        List<MusicResponseDTO> response = musicMapper.toDtoList(musicList);
        return ResponseEntity.ok(response);
    }

}
