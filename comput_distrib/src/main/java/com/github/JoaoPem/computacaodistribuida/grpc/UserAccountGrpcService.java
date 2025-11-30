package com.github.JoaoPem.computacaodistribuida.grpc;

import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import com.github.JoaoPem.computacaodistribuida.services.UserAccountService;
import io.grpc.stub.StreamObserver;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import net.devh.boot.grpc.server.service.GrpcService;

import java.util.List;

@GrpcService
@RequiredArgsConstructor
public class UserAccountGrpcService extends UserAccountServiceGrpc.UserAccountServiceImplBase {

    private final UserAccountService userAccountService;
    private final PlaylistService playlistService;

    @Override
    public void listAllUserAccounts(
            EmptyRequest request,
            StreamObserver<UserAccountListResponse> responseObserver) {

        List<com.github.JoaoPem.computacaodistribuida.models.UserAccount> users =
                userAccountService.listAllUserAccount();

        UserAccountListResponse.Builder responseBuilder = UserAccountListResponse.newBuilder();

        users.forEach(user -> responseBuilder.addUsers(
                UserAccount.newBuilder()
                        .setId(user.getId())
                        .setName(user.getName())
                        .build()
        ));

        responseObserver.onNext(responseBuilder.build());
        responseObserver.onCompleted();
    }

    @Override
    @Transactional
    public void listUserPlaylists(
            UserIdRequest request,
            StreamObserver<PlaylistListResponse> responseObserver) {

        List<com.github.JoaoPem.computacaodistribuida.models.Playlist> playlists =
                playlistService.listPlaylistsByUserId(request.getUserId());

        if (playlists == null) playlists = List.of();

        PlaylistListResponse.Builder responseBuilder = PlaylistListResponse.newBuilder();

        playlists.forEach(playlist -> {
            List<String> musicNames = playlist.getMusicList() != null
                    ? playlist.getMusicList().stream().map(m -> m.getName()).toList()
                    : List.of();

            responseBuilder.addPlaylists(
                    com.github.JoaoPem.computacaodistribuida.grpc.Playlist.newBuilder()
                            .setId(playlist.getId())
                            .setName(playlist.getName())
                            .setUserAccountName(
                                    playlist.getUser() != null ? playlist.getUser().getName() : ""
                            )
                            .addAllMusicNameList(musicNames)
                            .build()
            );
        });

        responseObserver.onNext(responseBuilder.build());
        responseObserver.onCompleted();
    }
}
