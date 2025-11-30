from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import database as bd

# Cria as tabelas no MySQL se não existirem
bd.Base.metadata.create_all(bind=bd.engine)

app = FastAPI(title="Streaming Distribuído - REST")

# --- Dependência do Banco ---
def get_db():
    db = bd.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# Pydantic Models (Validação e Resposta)
# ==========================================

# --- USUÁRIOS ---
class UsuarioCreate(BaseModel):
    nome: str
    idade: int

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    idade: int
    class Config:
        from_attributes = True

# --- MÚSICAS ---
class MusicaCreate(BaseModel):
    titulo: str
    artista: str

class MusicaResponse(BaseModel):
    id: int
    titulo: str
    artista: str
    class Config:
        from_attributes = True

# --- PLAYLISTS ---
class PlaylistCreate(BaseModel):
    nome: str
    id_usuario: int  # Link obrigatório com Usuário (1..1 no diagrama)

class PlaylistResponse(BaseModel):
    id: int
    nome: str
    dono_id: int
    musicas: List[MusicaResponse] = [] # Mostra as músicas dentro da playlist
    class Config:
        from_attributes = True

# ==========================================
# ENDPOINTS (Rotas)
# ==========================================

# --- 1. USUÁRIOS ---
@app.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = bd.Usuario(nome=usuario.nome, idade=usuario.idade)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(bd.Usuario).all()

# --- 2. MÚSICAS ---
@app.post("/musicas", response_model=MusicaResponse)
def criar_musica(musica: MusicaCreate, db: Session = Depends(get_db)):
    nova_musica = bd.Musica(titulo=musica.titulo, artista=musica.artista)
    db.add(nova_musica)
    db.commit()
    db.refresh(nova_musica)
    return nova_musica

@app.get("/musicas", response_model=List[MusicaResponse])
def listar_musicas(db: Session = Depends(get_db)):
    return db.query(bd.Musica).all()

# --- 3. PLAYLISTS ---
@app.post("/playlists", response_model=PlaylistResponse)
def criar_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    # Verifica se usuário existe antes de criar
    dono = db.query(bd.Usuario).filter(bd.Usuario.id == playlist.id_usuario).first()
    if not dono:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    nova_playlist = bd.Playlist(nome=playlist.nome, dono_id=playlist.id_usuario)
    db.add(nova_playlist)
    db.commit()
    db.refresh(nova_playlist)
    return nova_playlist

@app.get("/usuarios/{id_usuario}/playlists", response_model=List[PlaylistResponse])
def listar_playlists_usuario(id_usuario: int, db: Session = Depends(get_db)):
    # Retorna playlists de um usuário específico
    return db.query(bd.Playlist).filter(bd.Playlist.dono_id == id_usuario).all()

# --- 4. RELACIONAMENTO: ADICIONAR MÚSICA NA PLAYLIST ---
@app.post("/playlists/{id_playlist}/musicas/{id_musica}")
def adicionar_musica_na_playlist(id_playlist: int, id_musica: int, db: Session = Depends(get_db)):
    # Busca a Playlist
    playlist = db.query(bd.Playlist).filter(bd.Playlist.id == id_playlist).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    # Busca a Música
    musica = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    # Faz a ligação (Many-to-Many)
    playlist.musicas.append(musica)
    db.commit()
    
    return {"mensagem": f"Música '{musica.titulo}' adicionada à playlist '{playlist.nome}'"}

# --- 5. CONSULTA ESPECÍFICA (PDF Pag 6) ---
@app.get("/musicas/{id_musica}/playlists", response_model=List[PlaylistResponse])
def listar_playlists_com_musica(id_musica: int, db: Session = Depends(get_db)):
    # Busca a música primeiro
    musica = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
    
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    # Graças ao relacionamento no SQLAlchemy, a lista já está pronta
    return musica.playlists

# ==========================================
# OPERAÇÕES DE ALTERAÇÃO (PUT) E REMOÇÃO (DELETE)
# Cole isso no final do seu arquivo api_rest.py
# ==========================================

# --- GERENCIAMENTO DE USUÁRIOS ---
@app.put("/usuarios/{id_usuario}", response_model=UsuarioResponse)
def atualizar_usuario(id_usuario: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(bd.Usuario).filter(bd.Usuario.id == id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db_usuario.nome = usuario.nome
    db_usuario.idade = usuario.idade
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuarios/{id_usuario}")
def deletar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    db_usuario = db.query(bd.Usuario).filter(bd.Usuario.id == id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(db_usuario)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}

# --- GERENCIAMENTO DE MÚSICAS ---
@app.put("/musicas/{id_musica}", response_model=MusicaResponse)
def atualizar_musica(id_musica: int, musica: MusicaCreate, db: Session = Depends(get_db)):
    db_musica = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
    if not db_musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    db_musica.titulo = musica.titulo
    db_musica.artista = musica.artista
    db.commit()
    db.refresh(db_musica)
    return db_musica

@app.delete("/musicas/{id_musica}")
def deletar_musica(id_musica: int, db: Session = Depends(get_db)):
    db_musica = db.query(bd.Musica).filter(bd.Musica.id == id_musica).first()
    if not db_musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    
    db.delete(db_musica)
    db.commit()
    return {"mensagem": "Música deletada com sucesso"}

# --- GERENCIAMENTO DE PLAYLISTS ---
@app.put("/playlists/{id_playlist}", response_model=PlaylistResponse)
def atualizar_playlist(id_playlist: int, playlist_update: PlaylistCreate, db: Session = Depends(get_db)):
    db_playlist = db.query(bd.Playlist).filter(bd.Playlist.id == id_playlist).first()
    if not db_playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    db_playlist.nome = playlist_update.nome
    # Nota: Geralmente não mudamos o dono da playlist, mas se quiser, pode atualizar:
    # db_playlist.dono_id = playlist_update.id_usuario
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@app.get("/playlists", response_model=List[PlaylistResponse])
def listar_todas_playlists(db: Session = Depends(get_db)):
    return db.query(bd.Playlist).all()

@app.delete("/playlists/{id_playlist}")
def deletar_playlist(id_playlist: int, db: Session = Depends(get_db)):
    db_playlist = db.query(bd.Playlist).filter(bd.Playlist.id == id_playlist).first()
    if not db_playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    
    db.delete(db_playlist)
    db.commit()
    return {"mensagem": f"Playlist de id '{id_playlist}' deletada com sucesso"}