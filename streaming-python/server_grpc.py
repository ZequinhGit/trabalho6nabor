import grpc
from concurrent import futures
import streaming_pb2
import streaming_pb2_grpc
import database as bd

class StreamingService(streaming_pb2_grpc.StreamingServiceServicer):
    
    # --- USUÁRIOS ---
    def CriarUsuario(self, request, context):
        db = bd.SessionLocal()
        novo = bd.Usuario(nome=request.nome, idade=request.idade)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        db.close()
        return streaming_pb2.UsuarioResponse(id=novo.id, nome=novo.nome, idade=novo.idade)

    def ListarUsuarios(self, request, context):
        db = bd.SessionLocal()
        usuarios = db.query(bd.Usuario).all()
        lista = [streaming_pb2.UsuarioResponse(id=u.id, nome=u.nome, idade=u.idade) for u in usuarios]
        db.close()
        return streaming_pb2.ListaUsuarios(usuarios=lista)

    def AtualizarUsuario(self, request, context):
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == request.id).first()
        if u:
            u.nome = request.nome
            u.idade = request.idade
            db.commit()
            db.refresh(u)
            resp = streaming_pb2.UsuarioResponse(id=u.id, nome=u.nome, idade=u.idade)
            db.close()
            return resp
        db.close()
        context.abort(grpc.StatusCode.NOT_FOUND, "Usuario nao encontrado")

    def DeletarUsuario(self, request, context):
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == request.id).first()
        if u:
            db.delete(u)
            db.commit()
            db.close()
            return streaming_pb2.StatusResponse(mensagem="Deletado com sucesso", sucesso=True)
        db.close()
        return streaming_pb2.StatusResponse(mensagem="Erro ao deletar", sucesso=False)

    def ListarPlaylistsDoUsuario(self, request, context):
        db = bd.SessionLocal()
        playlists = db.query(bd.Playlist).filter(bd.Playlist.dono_id == request.id).all()
        lista = [streaming_pb2.PlaylistResponse(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in playlists]
        db.close()
        return streaming_pb2.ListaPlaylists(playlists=lista)

    # --- MÚSICAS ---
    def CriarMusica(self, request, context):
        db = bd.SessionLocal()
        nova = bd.Musica(titulo=request.titulo, artista=request.artista)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return streaming_pb2.MusicaResponse(id=nova.id, titulo=nova.titulo, artista=nova.artista)

    def ListarMusicas(self, request, context):
        db = bd.SessionLocal()
        musicas = db.query(bd.Musica).all()
        lista = [streaming_pb2.MusicaResponse(id=m.id, titulo=m.titulo, artista=m.artista) for m in musicas]
        db.close()
        return streaming_pb2.ListaMusicas(musicas=lista)

    def AtualizarMusica(self, request, context):
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == request.id).first()
        if m:
            m.titulo = request.titulo
            m.artista = request.artista
            db.commit()
            db.refresh(m)
            resp = streaming_pb2.MusicaResponse(id=m.id, titulo=m.titulo, artista=m.artista)
            db.close()
            return resp
        db.close()
        context.abort(grpc.StatusCode.NOT_FOUND, "Musica nao encontrada")

    def DeletarMusica(self, request, context):
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == request.id).first()
        if m:
            db.delete(m)
            db.commit()
            db.close()
            return streaming_pb2.StatusResponse(mensagem="Deletada com sucesso", sucesso=True)
        db.close()
        return streaming_pb2.StatusResponse(mensagem="Erro ao deletar", sucesso=False)
    
    # REQUISITO PAG 6: Listar playlists que contêm uma música
    def ListarPlaylistsDaMusica(self, request, context):
        db = bd.SessionLocal()
        musica = db.query(bd.Musica).filter(bd.Musica.id == request.id).first()
        lista = []
        if musica:
            lista = [streaming_pb2.PlaylistResponse(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in musica.playlists]
        db.close()
        return streaming_pb2.ListaPlaylists(playlists=lista)

    # --- PLAYLISTS ---
    def CriarPlaylist(self, request, context):
        db = bd.SessionLocal()
        nova = bd.Playlist(nome=request.nome, dono_id=request.id_usuario)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return streaming_pb2.PlaylistResponse(id=nova.id, nome=nova.nome, dono_id=nova.dono_id)

    def AtualizarPlaylist(self, request, context):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == request.id).first()
        if p:
            p.nome = request.nome
            db.commit()
            db.refresh(p)
            resp = streaming_pb2.PlaylistResponse(id=p.id, nome=p.nome, dono_id=p.dono_id)
            db.close()
            return resp
        db.close()
        context.abort(grpc.StatusCode.NOT_FOUND, "Playlist nao encontrada")

    def DeletarPlaylist(self, request, context):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == request.id).first()
        if p:
            db.delete(p)
            db.commit()
            db.close()
            return streaming_pb2.StatusResponse(mensagem="Deletada com sucesso", sucesso=True)
        db.close()
        return streaming_pb2.StatusResponse(mensagem="Erro", sucesso=False)

    def AddMusicaPlaylist(self, request, context):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == request.id_playlist).first()
        m = db.query(bd.Musica).filter(bd.Musica.id == request.id_musica).first()
        if p and m:
            p.musicas.append(m)
            db.commit()
            db.close()
            return streaming_pb2.StatusResponse(mensagem="Adicionado com sucesso", sucesso=True)
        db.close()
        return streaming_pb2.StatusResponse(mensagem="Erro: Playlist ou Musica nao achada", sucesso=False)

    def ListarMusicasDaPlaylist(self, request, context):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == request.id).first()
        lista = []
        if p:
            lista = [streaming_pb2.MusicaResponse(id=m.id, titulo=m.titulo, artista=m.artista) for m in p.musicas]
        db.close()
        return streaming_pb2.ListaMusicas(musicas=lista)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()