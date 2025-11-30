package com.github.JoaoPem.computacaodistribuida.controllers.graph;

import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.useraccounts.UserAccountResponseDTO;
import com.github.JoaoPem.computacaodistribuida.mappers.PlaylistMapper;
import com.github.JoaoPem.computacaodistribuida.mappers.UserAccountMapper;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.models.UserAccount;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import com.github.JoaoPem.computacaodistribuida.services.UserAccountService;
import lombok.RequiredArgsConstructor;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class UserAccountGraphQLResolver {

    private final UserAccountService userAccountService;
    private final UserAccountMapper userAccountMapper;
    private final PlaylistService playlistService;
    private final PlaylistMapper playlistMapper;

    @QueryMapping
    public List<UserAccountResponseDTO> allUsers() {
        List<UserAccount> userAccountList = userAccountService.listAllUserAccount();
        return userAccountMapper.toDtoList(userAccountList);
    }

    @QueryMapping
    public List<PlaylistResponseDTO> userPlaylists(@Argument Long userId) {
        List<Playlist> playlists = playlistService.listPlaylistsByUserId(userId);
        return playlistMapper.toDtoList(playlists);
    }

}
