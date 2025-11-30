package com.github.JoaoPem.computacaodistribuida.models;

import jakarta.persistence.*;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "musics")
@Data
public class Music {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String artist;

    @ManyToMany(mappedBy = "musicList")
    private List<Playlist> playlists = new ArrayList<>();

}
