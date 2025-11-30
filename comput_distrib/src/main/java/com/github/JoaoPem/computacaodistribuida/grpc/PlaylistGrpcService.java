package com.github.JoaoPem.computacaodistribuida.grpc;

import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import com.github.JoaoPem.computacaodistribuida.services.MusicService;
import io.grpc.stub.StreamObserver;
import lombok.RequiredArgsConstructor;
import net.devh.boot.grpc.server.service.GrpcService;

import jakarta.transaction.Transactional;
import java.util.List;

@GrpcService
@RequiredArgsConstructor
public class PlaylistGrpcService extends PlaylistServiceGrpc.PlaylistServiceImplBase {

    private final PlaylistService playlistService;
    private final MusicService musicService;

    @Override
    @Transactional
    public void listAllPlaylists(
            com.github.JoaoPem.computacaodistribuida.grpc.EmptyRequest request,
            StreamObserver<com.github.JoaoPem.computacaodistribuida.grpc.PlaylistListResponse> responseObserver) {

        List<com.github.JoaoPem.computacaodistribuida.models.Playlist> playlists =
                playlistService.listAllPlaylists();

        com.github.JoaoPem.computacaodistribuida.grpc.PlaylistListResponse.Builder responseBuilder =
                com.github.JoaoPem.computacaodistribuida.grpc.PlaylistListResponse.newBuilder();

        playlists.forEach(p -> responseBuilder.addPlaylists(
                com.github.JoaoPem.computacaodistribuida.grpc.Playlist.newBuilder()
                        .setId(p.getId())
                        .setName(p.getName())
                        .setUserAccountName(
                                p.getUser() != null ? p.getUser().getName() : ""
                        )
                        .addAllMusicNameList(
                                p.getMusicList() != null
                                        ? p.getMusicList().stream().map(m -> m.getName()).toList()
                                        : List.of()
                        )
                        .build()
        ));

        responseObserver.onNext(responseBuilder.build());
        responseObserver.onCompleted();
    }

    @Override
    @Transactional
    public void listMusicsByPlaylist(
            com.github.JoaoPem.computacaodistribuida.grpc.PlaylistIdRequest request,
            StreamObserver<com.github.JoaoPem.computacaodistribuida.grpc.MusicListResponse> responseObserver) {

        List<com.github.JoaoPem.computacaodistribuida.models.Music> musics =
                playlistService.listMusicsByPlaylistId(request.getPlaylistId());

        if (musics == null) musics = List.of();

        com.github.JoaoPem.computacaodistribuida.grpc.MusicListResponse.Builder responseBuilder =
                com.github.JoaoPem.computacaodistribuida.grpc.MusicListResponse.newBuilder();

        musics.forEach(m -> responseBuilder.addMusics(
                com.github.JoaoPem.computacaodistribuida.grpc.Music.newBuilder()
                        .setId(m.getId())
                        .setName(m.getName())
                        .setArtist(m.getArtist())
                        .build()
        ));

        responseObserver.onNext(responseBuilder.build());
        responseObserver.onCompleted();
    }
}
