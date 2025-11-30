# ==========================================
# BLOCO DE COMPATIBILIDADE (O REMENDO MÁGICO)
# Isso engana o Spyne para ele rodar no Python 3.13
# ==========================================
import sys
import collections
from collections import abc

# 1. Corrige o problema das Collections (MutableMapping, Sequence, etc)
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = abc.MutableMapping
if not hasattr(collections, 'MutableSet'):
    collections.MutableSet = abc.MutableSet
if not hasattr(collections, 'Sequence'):
    collections.Sequence = abc.Sequence
if not hasattr(collections, 'Iterable'):
    collections.Iterable = abc.Iterable

# 2. Corrige o problema do CGI (Removido no Python 3.13)
# Criamos um módulo 'cgi' falso na memória com as funções que o Spyne usa
if "cgi" not in sys.modules:
    import html
    from types import ModuleType
    
    fake_cgi = ModuleType("cgi")
    
    # Spyne usa cgi.escape (agora está em html.escape)
    fake_cgi.escape = html.escape
    
    # Spyne usa cgi.parse_header (agora precisamos simular)
    def parse_header(line):
        # Simulação simples para evitar o crash
        if not line: return ("", {})
        parts = line.split(";")
        return (parts[0].strip(), {})
    fake_cgi.parse_header = parse_header

    # Spyne usa cgi.FieldStorage (mock vazio para passar pelo import)
    class FieldStorage:
        def __init__(self, fp=None, headers=None, outerboundary=b'',
                     environ=None, keep_blank_values=0, strict_parsing=0,
                     limit=None, encoding='utf-8', errors='replace',
                     max_num_fields=None, separator='&'):
            pass
    fake_cgi.FieldStorage = FieldStorage

    # Injeta o módulo falso no Python
    sys.modules["cgi"] = fake_cgi

# ==========================================
# FIM DO BLOCO DE COMPATIBILIDADE
# Agora começa o seu código normal
# ==========================================

from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import database as bd

# --- MODELOS DE DADOS (XML) ---
class UsuarioModel(ComplexModel):
    id = Integer
    nome = Unicode
    idade = Integer

class MusicaModel(ComplexModel):
    id = Integer
    titulo = Unicode
    artista = Unicode

class PlaylistModel(ComplexModel):
    id = Integer
    nome = Unicode
    dono_id = Integer

# --- SERVIÇO SOAP ---
class StreamingService(ServiceBase):
    
    # ==========================================
    # USUÁRIOS
    # ==========================================
    @rpc(Unicode, Integer, _returns=UsuarioModel)
    def criar_usuario(ctx, nome, idade):
        db = bd.SessionLocal()
        novo = bd.Usuario(nome=nome, idade=idade)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return UsuarioModel(id=novo.id, nome=novo.nome, idade=novo.idade)

    @rpc(_returns=Array(UsuarioModel))
    def listar_usuarios(ctx):
        db = bd.SessionLocal()
        users = db.query(bd.Usuario).all()
        return [UsuarioModel(id=u.id, nome=u.nome, idade=u.idade) for u in users]

    @rpc(Integer, Unicode, Integer, _returns=UsuarioModel)
    def atualizar_usuario(ctx, id, nome, idade):
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == id).first()
        if u:
            u.nome = nome
            u.idade = idade
            db.commit()
            db.refresh(u)
            return UsuarioModel(id=u.id, nome=u.nome, idade=u.idade)
        return None

    @rpc(Integer, _returns=Boolean)
    def deletar_usuario(ctx, id):
        db = bd.SessionLocal()
        u = db.query(bd.Usuario).filter(bd.Usuario.id == id).first()
        if u:
            db.delete(u)
            db.commit()
            return True
        return False

    @rpc(Integer, _returns=Array(PlaylistModel))
    def listar_playlists_do_usuario(ctx, id_usuario):
        db = bd.SessionLocal()
        playlists = db.query(bd.Playlist).filter(bd.Playlist.dono_id == id_usuario).all()
        return [PlaylistModel(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in playlists]

    # ==========================================
    # MÚSICAS
    # ==========================================
    @rpc(Unicode, Unicode, _returns=MusicaModel)
    def criar_musica(ctx, titulo, artista):
        db = bd.SessionLocal()
        nova = bd.Musica(titulo=titulo, artista=artista)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        return MusicaModel(id=nova.id, titulo=nova.titulo, artista=nova.artista)

    @rpc(_returns=Array(MusicaModel))
    def listar_musicas(ctx):
        db = bd.SessionLocal()
        musicas = db.query(bd.Musica).all()
        return [MusicaModel(id=m.id, titulo=m.titulo, artista=m.artista) for m in musicas]

    @rpc(Integer, Unicode, Unicode, _returns=MusicaModel)
    def atualizar_musica(ctx, id, titulo, artista):
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == id).first()
        if m:
            m.titulo = titulo
            m.artista = artista
            db.commit()
            db.refresh(m)
            return MusicaModel(id=m.id, titulo=m.titulo, artista=m.artista)
        return None

    @rpc(Integer, _returns=Boolean)
    def deletar_musica(ctx, id):
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == id).first()
        if m:
            db.delete(m)
            db.commit()
            return True
        return False

    @rpc(Integer, _returns=Array(PlaylistModel))
    def listar_playlists_da_musica(ctx, id_musica):
        db = bd.SessionLocal()
        m = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
        if m:
            return [PlaylistModel(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in m.playlists]
        return []

    # ==========================================
    # PLAYLISTS
    # ==========================================
    @rpc(Unicode, Integer, _returns=PlaylistModel)
    def criar_playlist(ctx, nome, id_usuario):
        db = bd.SessionLocal()
        nova = bd.Playlist(nome=nome, dono_id=id_usuario)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        return PlaylistModel(id=nova.id, nome=nova.nome, dono_id=nova.dono_id)

    @rpc(Integer, Unicode, _returns=PlaylistModel)
    def atualizar_playlist(ctx, id, nome):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id).first()
        if p:
            p.nome = nome
            db.commit()
            db.refresh(p)
            return PlaylistModel(id=p.id, nome=p.nome, dono_id=p.dono_id)
        return None

    @rpc(Integer, _returns=Boolean)
    def deletar_playlist(ctx, id):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id).first()
        if p:
            db.delete(p)
            db.commit()
            return True
        return False

    @rpc(Integer, Integer, _returns=Boolean)
    def adicionar_musica_playlist(ctx, id_playlist, id_musica):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id_playlist).first()
        m = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
        if p and m:
            p.musicas.append(m)
            db.commit()
            return True
        return False

    @rpc(Integer, _returns=Array(MusicaModel))
    def listar_musicas_da_playlist(ctx, id_playlist):
        db = bd.SessionLocal()
        p = db.query(bd.Playlist).filter(bd.Playlist.id == id_playlist).first()
        if p:
            return [MusicaModel(id=m.id, titulo=m.titulo, artista=m.artista) for m in p.musicas]
        return []
    @rpc(_returns=Array(PlaylistModel))
    def listar_playlists(ctx):
        db = bd.SessionLocal()
        playlists = db.query(bd.Playlist).all()
        # Mapeando do objeto do banco para o modelo XML
        lista = [PlaylistModel(id=p.id, nome=p.nome, dono_id=p.dono_id) for p in playlists]
        db.close()
        return lista

# --- APP SETUP ---
application = Application([StreamingService], 'spyne.streaming.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("Servidor SOAP rodando na porta 8002 (Waitress Turbinado)...")
    
    from waitress import serve
    
    serve(
        wsgi_app, 
        host='0.0.0.0', 
        port=8002, 
        # Aumentamos o número de threads (trabalhadores) para processar mais coisas ao mesmo tempo
        threads=100,
        # Aumentamos o limite de conexões (tem que ser maior que seus usuários no Locust)
        connection_limit=1000,
        # Aumentamos a fila de espera do socket
        backlog=1000,
        # Aumentamos a fila interna de tarefas pendentes
        channel_request_lookahead=1000
    )