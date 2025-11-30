package com.github.JoaoPem.computacaodistribuida.services;

import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.repositories.PlaylistRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PlaylistService {

    private final PlaylistRepository playlistRepository;

    public Playlist createPlaylist(Playlist playlist) {
        return playlistRepository.save(playlist);
    }

    public List<Playlist> listAllPlaylists() {
        return playlistRepository.findAll();
    }

    public List<Playlist> listPlaylistsByUserId(Long userId) {
        return playlistRepository.findByUserId(userId);
    }

    public List<Music> listMusicsByPlaylistId(Long playlistId) {
        Playlist playlist = playlistRepository.findById(playlistId)
                .orElseThrow(() -> new RuntimeException("Playlist não encontrada com ID " + playlistId));

        return playlist.getMusicList();
    }

    public List<Playlist> listPlaylistsByMusicId(Long musicId) {
        return playlistRepository.findByMusicListId(musicId);
    }

}
