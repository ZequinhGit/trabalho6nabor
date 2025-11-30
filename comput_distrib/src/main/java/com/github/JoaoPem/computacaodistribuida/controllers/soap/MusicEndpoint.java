package com.github.JoaoPem.computacaodistribuida.controllers.soap;

import com.example.musics.soap.GetAllMusicsRequest;
import com.example.musics.soap.GetAllMusicsResponse;
import com.example.musics.soap.GetPlaylistsByMusicRequest;
import com.example.musics.soap.GetPlaylistsByMusicResponse;
import com.example.musics.soap.Music;
import com.example.musics.soap.Playlist;

import com.github.JoaoPem.computacaodistribuida.services.MusicService;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import java.util.List;

@Endpoint
@RequiredArgsConstructor
public class MusicEndpoint {

    private static final String NAMESPACE_URI = "http://example.com/musics/soap";

    private final MusicService musicService;
    private final PlaylistService playlistService;

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetAllMusicsRequest")
    @ResponsePayload
    public GetAllMusicsResponse getAllMusics(@RequestPayload GetAllMusicsRequest request) {
        List<com.github.JoaoPem.computacaodistribuida.models.Music> musicList = musicService.listAllMusics();

        GetAllMusicsResponse response = new GetAllMusicsResponse();
        musicList.forEach(musicEntity -> {
            Music soapMusic = new Music();
            soapMusic.setId(musicEntity.getId());
            soapMusic.setName(musicEntity.getName());
            soapMusic.setArtist(musicEntity.getArtist());
            response.getMusics().add(soapMusic);
        });

        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetPlaylistsByMusicRequest")
    @ResponsePayload
    @Transactional
    public GetPlaylistsByMusicResponse getPlaylistsByMusic(@RequestPayload GetPlaylistsByMusicRequest request) {
        GetPlaylistsByMusicResponse response = new GetPlaylistsByMusicResponse();

        List<com.github.JoaoPem.computacaodistribuida.models.Playlist> playlists =
                playlistService.listPlaylistsByMusicId(request.getMusicId());

        playlists.forEach(playlistEntity -> {
            Playlist playlistSoap = new Playlist();
            playlistSoap.setId(playlistEntity.getId());
            playlistSoap.setName(playlistEntity.getName());
            playlistSoap.setUserAccountName(playlistEntity.getUser().getName());

            playlistEntity.getMusicList().forEach(musicEntity -> {
                Music musicSoap = new Music();
                musicSoap.setId(musicEntity.getId());
                musicSoap.setName(musicEntity.getName());
                musicSoap.setArtist(musicEntity.getArtist());
                playlistSoap.getMusics().add(musicSoap);
            });

            response.getPlaylists().add(playlistSoap);
        });

        return response;
    }
}
