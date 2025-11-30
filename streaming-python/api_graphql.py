import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from typing import List, Optional
import database as bd

# ==========================================
# TIPOS GRAPHQL (VIEW)
# Define como os dados são mostrados (JSON de retorno)
# ==========================================

@strawberry.type
class MusicaType:
    id: int
    titulo: str
    artista: str

@strawberry.type
class PlaylistType:
    id: int
    nome: str
    dono_id: int
    
    # Resolver aninhado: Permite buscar as músicas DENTRO da playlist
    # Atende: "Listar os dados de todas as músicas de uma determinada playlist"
    @strawberry.field
    def musicas(self) -> List[MusicaType]:
        db = bd.SessionLocal()
        playlist = db.query(bd.Playlist).filter(bd.Playlist.id == self.id).first()
        resultado = []
        if playlist:
            resultado = [
                MusicaType(id=m.id, titulo=m.titulo, artista=m.artista) 
                for m in playlist.musicas
            ]
        db.close()
        return resultado

@strawberry.type
class UsuarioType:
    id: int
    nome: str
    idade: int
    
    # Resolver aninhado: Permite buscar as playlists DENTRO do usuário
    # Atende: "Listar os dados de todas as playlists de um determinado usuário"
    @strawberry.field
    def playlists(self) -> List[PlaylistType]:
        db = bd.SessionLocal()
        playlists_db = db.query(bd.Playlist).filter(bd.Playlist.dono_id == self.id).all()
        resultado = [
            PlaylistType(id=p.id, nome=p.nome, dono_id=p.dono_id) 
            for p in playlists_db
        ]
        db.close()
        return resultado

# ==========================================
# QUERIES (CONSULTAS - Equivalente ao GET)
# ==========================================
@strawberry.type
class Query:
    # 1. Listar todos os usuários (PDF Pag 6)
    @strawberry.field
    def todos_usuarios(self) -> List[UsuarioType]:
        db = bd.SessionLocal()
        usuarios = db.query(bd.Usuario).all()
        res = [UsuarioType(id=u.id, nome=u.nome, idade=u.idade) for u in usuarios]
        db.close()
        return res

    # 2. Listar todas as músicas (PDF Pag 6)
    @strawberry.field
    def todas_musicas(self) -> List[MusicaType]:
        db = bd.SessionLocal()
        musicas = db.query(bd.Musica).all()
        res = [MusicaType(id=m.id, titulo=m.titulo, artista=m.artista) for m in musicas]
        db.close()
        return res

    # Extra: Listar todas as playlists (Para facilitar seus testes)
    @strawberry.field
    def todas_playlists(self) -> List[PlaylistType]:
        db = bd.SessionLocal()
        playlists = db.query(bd.Playlist).all()
        res = [PlaylistType(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in playlists]
        db.close()
        return res
    
    # Consulta Auxiliar: Usuário por ID
    @strawberry.field
    def usuario_por_id(self, id: int) -> Optional[UsuarioType]:
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == id).first()
        db.close()
        if u:
            return UsuarioType(id=u.id, nome=u.nome, idade=u.idade)
        return None

    # Consulta Auxiliar: Playlist por ID (Para ver músicas de uma playlist específica)
    @strawberry.field
    def playlist_por_id(self, id: int) -> Optional[PlaylistType]:
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id).first()
        db.close()
        if p:
            return PlaylistType(id=p.id, nome=p.nome, dono_id=p.dono_id)
        return None

    # 3. Listar playlists de um usuário específico (Equivalente direto do REST)
    @strawberry.field
    def playlists_por_usuario(self, id_usuario: int) -> List[PlaylistType]:
        db = bd.SessionLocal()
        playlists = db.query(bd.Playlist).filter(bd.Playlist.dono_id == id_usuario).all()
        res = [PlaylistType(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in playlists]
        db.close()
        return res

    # 4. Listar playlists que contêm uma música (PDF Pag 6 - REQUISITO CRÍTICO)
    @strawberry.field
    def playlists_por_musica(self, id_musica: int) -> List[PlaylistType]:
        db = bd.SessionLocal()
        musica = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
        resultado = []
        if musica:
            resultado = [
                PlaylistType(id=p.id, nome=p.nome, dono_id=p.dono_id) 
                for p in musica.playlists
            ]
        db.close()
        return resultado

# ==========================================
# MUTATIONS (CADASTROS - Equivalente ao POST/PUT/DELETE)
# ==========================================
@strawberry.type
class Mutation:
    # --- CRIAÇÃO (CREATE) ---
    
    @strawberry.mutation
    def criar_usuario(self, nome: str, idade: int) -> UsuarioType:
        db = bd.SessionLocal()
        novo = bd.Usuario(nome=nome, idade=idade)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        db.close()
        return UsuarioType(id=novo.id, nome=novo.nome, idade=novo.idade)

    @strawberry.mutation
    def criar_musica(self, titulo: str, artista: str) -> MusicaType:
        db = bd.SessionLocal()
        nova = bd.Musica(titulo=titulo, artista=artista)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return MusicaType(id=nova.id, titulo=nova.titulo, artista=nova.artista)

    @strawberry.mutation
    def criar_playlist(self, nome: str, id_usuario: int) -> PlaylistType:
        db = bd.SessionLocal()
        nova = bd.Playlist(nome=nome, dono_id=id_usuario)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        db.close()
        return PlaylistType(id=nova.id, nome=nova.nome, dono_id=nova.dono_id)

    # --- RELACIONAMENTO (MUITOS-PARA-MUITOS) ---
    @strawberry.mutation
    def adicionar_musica_playlist(self, id_playlist: int, id_musica: int) -> str:
        db = bd.SessionLocal()
        playlist = db.query(bd.Playlist).filter(bd.Playlist.id == id_playlist).first()
        musica = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
        
        msg = "Erro: Playlist ou Musica nao encontrada"
        if playlist and musica:
            playlist.musicas.append(musica)
            db.commit()
            msg = f"Sucesso: Musica {musica.titulo} adicionada na playlist {playlist.nome}"
        
        db.close()
        return msg

    # --- ATUALIZAÇÃO (UPDATE) ---

    @strawberry.mutation
    def atualizar_usuario(self, id: int, nome: str, idade: int) -> Optional[UsuarioType]:
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == id).first()
        if u:
            u.nome = nome
            u.idade = idade
            db.commit()
            db.refresh(u)
            db.close()
            return UsuarioType(id=u.id, nome=u.nome, idade=u.idade)
        db.close()
        return None

    @strawberry.mutation
    def atualizar_musica(self, id: int, titulo: str, artista: str) -> Optional[MusicaType]:
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == id).first()
        if m:
            m.titulo = titulo
            m.artista = artista
            db.commit()
            db.refresh(m)
            db.close()
            return MusicaType(id=m.id, titulo=m.titulo, artista=m.artista)
        db.close()
        return None

    @strawberry.mutation
    def atualizar_playlist(self, id: int, nome: str) -> Optional[PlaylistType]:
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id).first()
        if p:
            p.nome = nome
            db.commit()
            db.refresh(p)
            db.close()
            return PlaylistType(id=p.id, nome=p.nome, dono_id=p.dono_id)
        db.close()
        return None

    # --- REMOÇÃO (DELETE) ---

    @strawberry.mutation
    def deletar_usuario(self, id: int) -> bool:
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == id).first()
        if u:
            db.delete(u)
            db.commit()
            db.close()
            return True
        db.close()
        return False

    @strawberry.mutation
    def deletar_musica(self, id: int) -> bool:
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == id).first()
        if m:
            db.delete(m)
            db.commit()
            db.close()
            return True
        db.close()
        return False

    @strawberry.mutation
    def deletar_playlist(self, id: int) -> bool:
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id).first()
        if p:
            db.delete(p)
            db.commit()
            db.close()
            return True
        db.close()
        return False

# --- CONFIGURAÇÃO DO APP ---
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="Streaming GraphQL")
app.include_router(graphql_app, prefix="/graphql")