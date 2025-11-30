CREATE TABLE user_accounts (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE musics (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL
);

CREATE TABLE playlists (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    user_id BIGINT NOT NULL,
    CONSTRAINT fk_playlists_user
        FOREIGN KEY (user_id)
        REFERENCES user_accounts(id)
        ON DELETE CASCADE
);


CREATE TABLE playlist_musics (
    playlist_id BIGINT NOT NULL,
    music_id BIGINT NOT NULL,

    PRIMARY KEY (playlist_id, music_id),

    CONSTRAINT fk_playlistmusics_playlist
        FOREIGN KEY (playlist_id)
        REFERENCES playlists(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_playlistmusics_music
        FOREIGN KEY (music_id)
        REFERENCES musics(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_playlist_user ON playlists(user_id);
CREATE INDEX idx_playlistmusics_playlist ON playlist_musics(playlist_id);
CREATE INDEX idx_playlistmusics_music ON playlist_musics(music_id);
