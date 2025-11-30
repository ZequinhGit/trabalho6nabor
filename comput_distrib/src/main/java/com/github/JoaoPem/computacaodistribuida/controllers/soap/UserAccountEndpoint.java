package com.github.JoaoPem.computacaodistribuida.controllers.soap;

import com.example.users.soap.*;

import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import com.github.JoaoPem.computacaodistribuida.services.UserAccountService;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;

import java.util.List;

@Endpoint
@RequiredArgsConstructor
public class UserAccountEndpoint {

    private static final String NAMESPACE_URI = "http://example.com/users/soap";

    private final UserAccountService userAccountService;
    private final PlaylistService playlistService;


    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetAllUsersRequest")
    @ResponsePayload
    public GetAllUsersResponse getAllUsers(@RequestPayload GetAllUsersRequest request) {
        List<com.github.JoaoPem.computacaodistribuida.models.UserAccount> users = userAccountService.listAllUserAccount();

        GetAllUsersResponse response = new GetAllUsersResponse();

        users.forEach(userEntity -> {
            UserAccount soapUser = new UserAccount();
            soapUser.setId(userEntity.getId());
            soapUser.setName(userEntity.getName());
            response.getUsers().add(soapUser);
        });

        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetUserPlaylistsRequest")
    @ResponsePayload
    @Transactional
    public GetUserPlaylistsResponse getUserPlaylists(@RequestPayload GetUserPlaylistsRequest request) {
        Long userId = request.getUserId();

        List<com.github.JoaoPem.computacaodistribuida.models.Playlist> playlists =
                playlistService.listPlaylistsByUserId(userId);

        GetUserPlaylistsResponse response = new GetUserPlaylistsResponse();

        playlists.forEach(playlistEntity -> {
            Playlist soapPlaylist = new Playlist();
            soapPlaylist.setId(playlistEntity.getId());
            soapPlaylist.setName(playlistEntity.getName());
            soapPlaylist.setUserAccountName(playlistEntity.getUser().getName());

            playlistEntity.getMusicList().forEach(music ->
                    soapPlaylist.getMusicNameList().add(music.getName())
            );

            response.getPlaylists().add(soapPlaylist);
        });

        return response;
    }

}
