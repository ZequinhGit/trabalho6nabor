package com.github.JoaoPem.computacaodistribuida.repositories;

import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PlaylistRepository extends JpaRepository<Playlist, Long> {

    List<Playlist> findByUserId(Long userId);

    List<Playlist> findByMusicListId(Long musicId);

}
