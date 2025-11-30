package com.github.JoaoPem.computacaodistribuida.services;

import com.github.JoaoPem.computacaodistribuida.dtos.musics.MusicRequestDTO;
import com.github.JoaoPem.computacaodistribuida.models.Music;
import com.github.JoaoPem.computacaodistribuida.repositories.MusicRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class MusicService {

    private final MusicRepository musicRepository;

    public Music createMusic(Music music) {
        return musicRepository.save(music);
    }

    public List<Music> listAllMusics() {
        return musicRepository.findAll();
    }
}
