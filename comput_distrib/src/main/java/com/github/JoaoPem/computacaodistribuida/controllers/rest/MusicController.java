package com.github.JoaoPem.computacaodistribuida.controllers.rest;

import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicRequestDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicResponseDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.mappers.MusicMapper;
import com.github.JoaoPem.computacaodistribuida.mappers.PlaylistMapper;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.services.MusicService;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/rest/musics")
@RequiredArgsConstructor
public class MusicController {

    private final MusicMapper musicMapper;
    private final MusicService musicService;
    private final PlaylistService playlistService;
    private final PlaylistMapper playlistMapper;

    @PostMapping
    public ResponseEntity<MusicResponseDTO> createMusic(@RequestBody @Valid MusicRequestDTO musicRequestDTO){
        Music music = musicMapper.toEntity(musicRequestDTO);
        Music createdMusic = musicService.createMusic(music);
        MusicResponseDTO musicResponseDTO = musicMapper.toDto(createdMusic);
        return ResponseEntity.status(HttpStatus.CREATED).body(musicResponseDTO);
    }

    @GetMapping
    public ResponseEntity<List<MusicResponseDTO>> listAllMusics(){
        List<Music> musicList = musicService.listAllMusics();
        List<MusicResponseDTO> musicMapperDtoList = musicMapper.toDtoList(musicList);
        return ResponseEntity.status(HttpStatus.OK).body(musicMapperDtoList);
    }

    @GetMapping("/{musicId}/playlists")
    public ResponseEntity<List<PlaylistResponseDTO>> listPlaylistsByMusic(@PathVariable Long musicId) {
        List<Playlist> playlists = playlistService.listPlaylistsByMusicId(musicId);
        List<PlaylistResponseDTO> playlistDtoList = playlistMapper.toDtoList(playlists);
        return ResponseEntity.ok(playlistDtoList);
    }

}
