from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Conexão (Mantida igual)
DATABASE_URL = "mysql+pymysql://user_streaming:userpassword@localhost:3307/streaming_db"

engine = create_engine(
    DATABASE_URL,
    # Mantém 200 conexões sempre abertas
    pool_size=200,
    # Permite abrir mais 300 se precisar (Total 500)
    max_overflow=300,
    # Timeout baixo: se não conectar em 10s, falha logo (melhor que travar o teste)
    pool_timeout=15,
    pool_recycle=1800
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- TABELA DE ASSOCIAÇÃO ---
# Java espera: 'playlist_musics' com colunas 'playlist_id' e 'music_id'
playlist_musicas = Table(
    'playlist_musics', Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('music_id', Integer, ForeignKey('musics.id'))
)

# --- MODELOS ---

class Usuario(Base):
    __tablename__ = 'user_accounts'  # Java usa 'user_accounts'
    
    id = Column(Integer, primary_key=True, index=True)
    # Python usa .nome, mas no banco grava na coluna 'name'
    nome = Column('name', String(255)) 
    idade = Column(Integer) # Java não tem idade, mas o banco vai guardar

    playlists = relationship("Playlist", back_populates="dono")

class Musica(Base):
    __tablename__ = 'musics' # Java usa 'musics'
    
    id = Column(Integer, primary_key=True, index=True)
    # Python usa .titulo, mas no banco grava na coluna 'name'
    titulo = Column('name', String(255)) 
    # Python usa .artista, mas no banco grava na coluna 'artist'
    artista = Column('artist', String(255))

    playlists = relationship("Playlist", secondary=playlist_musicas, back_populates="musicas")

class Playlist(Base):
    __tablename__ = 'playlists' # Igual
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column('name', String(255))
    # Java espera a coluna 'user_id' como chave estrangeira
    dono_id = Column('user_id', Integer, ForeignKey('user_accounts.id'))

    dono = relationship("Usuario", back_populates="playlists")
    musicas = relationship("Musica", secondary=playlist_musicas, back_populates="playlists")