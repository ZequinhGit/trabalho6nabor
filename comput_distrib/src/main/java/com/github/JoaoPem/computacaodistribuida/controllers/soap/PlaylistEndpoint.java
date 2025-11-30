package com.github.JoaoPem.computacaodistribuida.controllers.soap;

import com.example.playlists.soap.*;
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
public class PlaylistEndpoint {

    private static final String NAMESPACE_URI = "http://example.com/playlists/soap";

    private final PlaylistService playlistService;

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetAllPlaylistsRequest")
    @ResponsePayload
    @Transactional
    public GetAllPlaylistsResponse getAllPlaylists(@RequestPayload GetAllPlaylistsRequest request) {
        List<com.github.JoaoPem.computacaodistribuida.models.Playlist> playlists =
                playlistService.listAllPlaylists();

        GetAllPlaylistsResponse response = new GetAllPlaylistsResponse();

        playlists.forEach(entity -> {
            Playlist soapPlaylist = new Playlist();
            soapPlaylist.setId(entity.getId());
            soapPlaylist.setName(entity.getName());
            soapPlaylist.setUserAccountName(entity.getUser().getName());

            // Inclui músicas
            entity.getMusicList().forEach(music -> {
                Music soapMusic = new Music();
                soapMusic.setId(music.getId());
                soapMusic.setName(music.getName());
                soapMusic.setArtist(music.getArtist());
                soapPlaylist.getMusics().add(soapMusic);
            });

            response.getPlaylists().add(soapPlaylist);
        });

        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetMusicsByPlaylistRequest")
    @ResponsePayload
    @Transactional
    public GetMusicsByPlaylistResponse getMusicsByPlaylist(@RequestPayload GetMusicsByPlaylistRequest request) {
        List<com.github.JoaoPem.computacaodistribuida.models.Music> musicList =
                playlistService.listMusicsByPlaylistId(request.getPlaylistId());

        GetMusicsByPlaylistResponse response = new GetMusicsByPlaylistResponse();

        musicList.forEach(entity -> {
            Music soapMusic = new Music();
            soapMusic.setId(entity.getId());
            soapMusic.setName(entity.getName());
            soapMusic.setArtist(entity.getArtist());
            response.getMusics().add(soapMusic);
        });

        return response;
    }
}

