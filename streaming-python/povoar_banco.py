from sqlalchemy.orm import Session
from sqlalchemy import text
import database as bd
import random
import time

def povoar_equilibrado():
    print("⚖️ INICIANDO CARGA EQUILIBRADA (SEGURO PARA APRESENTAÇÃO) ⚖️")
    start_time = time.time()

    # --- 1. LIMPEZA BLINDADA ---
    print("1. Limpando banco...")
    with bd.engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        bd.Base.metadata.drop_all(bind=conn)
        bd.Base.metadata.create_all(bind=conn)
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    
    db = bd.SessionLocal()

    try:
        # --- 2. CRIAR MÚSICAS (O Peso Pesado) ---
        # Mantemos 2000 pois é excelente para testar payload
        print("2. Gerando 2.000 Músicas...")
        lista_musicas = []
        for i in range(2000):
            m = bd.Musica(
                titulo=f"Symphony No. {i} in C Minor", 
                artista=f"Ludwig van Beethoven {i%100}"
            )
            lista_musicas.append(m)
        db.add_all(lista_musicas)
        db.commit()

        # --- 3. CRIAR USUÁRIOS (Quantidade Média) ---
        # 500 é um número muito bom para gráficos
        print("3. Gerando 500 Usuários...")
        lista_usuarios = []
        for i in range(500):
            u = bd.Usuario(nome=f"Usuario Demo {i}", idade=random.randint(18, 90))
            lista_usuarios.append(u)
        db.add_all(lista_usuarios)
        db.commit()

        # --- 4. CRIAR PLAYLISTS (Relacionamentos) ---
        print("4. Gerando 300 Playlists...")
        
        # Sorteia 300 usuários para terem playlists
        donos_sorteados = random.sample(lista_usuarios, 300)
        playlists_para_criar = []
        
        for i, dono in enumerate(donos_sorteados):
            p = bd.Playlist(nome=f"Playlist Vibe {i}", dono_id=dono.id)
            
            # Coloca entre 10 e 30 músicas em cada (gera volume de XML)
            qtd_musicas = random.randint(10, 30)
            musicas_da_playlist = random.sample(lista_musicas, qtd_musicas)
            
            p.musicas.extend(musicas_da_playlist)
            playlists_para_criar.append(p)

        db.add_all(playlists_para_criar)
        db.commit()
        
        tempo_total = time.time() - start_time
        print(f"✅ SUCESSO! Banco pronto em {tempo_total:.2f} segundos.")
        print(f"   - Músicas: 2.000 (Tabela Pesada)")
        print(f"   - Usuários: 500 (Tabela Média)")
        print(f"   - Playlists: 300 (Tabela Relacional)")

    except Exception as e:
        print(f"❌ DEU ERRO: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    povoar_equilibrado()