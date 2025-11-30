package com.github.JoaoPem.computacaodistribuida.grpc;

import com.github.JoaoPem.computacaodistribuida.services.MusicService;
import com.github.JoaoPem.computacaodistribuida.services.PlaylistService;
import io.grpc.stub.StreamObserver;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import net.devh.boot.grpc.server.service.GrpcService;

import java.util.List;

@GrpcService
@RequiredArgsConstructor
public class MusicGrpcService extends MusicServiceGrpc.MusicServiceImplBase {

    private final MusicService musicService;
    private final PlaylistService playlistService;

    @Override
    public void listAllMusics(
            EmptyRequest request,
            StreamObserver<MusicListResponse> responseObserver) {

        List<com.github.JoaoPem.computacaodistribuida.models.Music> musics = musicService.listAllMusics();

        MusicListResponse.Builder responseBuilder = MusicListResponse.newBuilder();

        musics.forEach(music -> responseBuilder.addMusics(
                com.github.JoaoPem.computacaodistribuida.grpc.Music.newBuilder()
                        .setId(music.getId())
                        .setName(music.getName())
                        .setArtist(music.getArtist())
                        .build()
        ));

        responseObserver.onNext(responseBuilder.build());
        responseObserver.onCompleted();
    }

    @Override
    @Transactional
    public void listPlaylistsByMusic(
            com.github.JoaoPem.computacaodistribuida.grpc.MusicIdRequest request,
            StreamObserver<com.github.JoaoPem.computacaodistribuida.grpc.PlaylistListResponse> responseObserver) {

        List<com.github.JoaoPem.computacaodistribuida.models.Playlist> playlists =
                playlistService.listPlaylistsByMusicId(request.getMusicId());

        if (playlists == null) {
            playlists = List.of();
        }

        com.github.JoaoPem.computacaodistribuida.grpc.PlaylistListResponse.Builder responseBuilder =
                com.github.JoaoPem.computacaodistribuida.grpc.PlaylistListResponse.newBuilder();

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