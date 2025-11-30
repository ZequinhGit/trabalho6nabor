package com.github.JoaoPem.computacaodistribuida.controllers.rest;

import com.github.JoaoPem.computacaodistribuida.dtos.playlists.PlaylistResponseDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.useraccounts.UserAccountRequestDTO;
import com.github.JoaoPem.computacaodistribuida.dtos.useraccounts.UserAccountResponseDTO;
import com.github.JoaoPem.computacaodistribuida.mappers.PlaylistMapper;
import com.github.JoaoPem.computacaodistribuida.mappers.UserAccountMapper;
import com.github.JoaoPem.computacaodistribuida.models.Playlist;
import com.github.JoaoPem.computacaodistribuida.models.UserAccount;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import com.github.JoaoPem.computacaodistribuida.services.UserAccountService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/rest/users")
@RequiredArgsConstructor
public class UserAccountController {

    private final UserAccountService userAccountService;
    private final UserAccountMapper userAccountMapper;
    private final PlaylistService playlistService;
    private final PlaylistMapper playlistMapper;

    @PostMapping
    public ResponseEntity<UserAccountResponseDTO> createUserAccount(@RequestBody @Valid UserAccountRequestDTO userAccountRequestDTO){
        UserAccount userAccount = userAccountMapper.toEntity(userAccountRequestDTO);
        UserAccount createdUserAccount = userAccountService.createUserAccount(userAccount);
        UserAccountResponseDTO userAccountResponseDTO = userAccountMapper.toDto(createdUserAccount);
        return ResponseEntity.status(HttpStatus.CREATED).body(userAccountResponseDTO);
    }

    @GetMapping
    public ResponseEntity<List<UserAccountResponseDTO>> listAllUserAccounts(){
        List<UserAccount> userAccountList = userAccountService.listAllUserAccount();
        List<UserAccountResponseDTO> userAccountResponseDTOList = userAccountMapper.toDtoList(userAccountList);
        return ResponseEntity.status(HttpStatus.OK).body(userAccountResponseDTOList);
    }

    @GetMapping("/{userId}/playlists")
    public ResponseEntity<List<PlaylistResponseDTO>> listUserPlaylists(@PathVariable Long userId) {
        List<Playlist> playlists = playlistService.listPlaylistsByUserId(userId);
        List<PlaylistResponseDTO> playlistDtoList = playlistMapper.toDtoList(playlists);
        return ResponseEntity.ok(playlistDtoList);
    }

}
