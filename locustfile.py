from locust import HttpUser, task, constant

# ==============================================================================
# 1. CONFIGURAÇÃO DOS PAYLOADS (O QUE VAMOS PEDIR)
# ==============================================================================

# --- GRAPHQL ---
# Python (Campos em Português)
gql_py_full = {
    "query": """
    {
      todosUsuarios { id nome }
      todasMusicas { id titulo artista }
      todasPlaylists { id nome }
    }
    """
}

# Java (Campos em Inglês)
gql_jv_full = {
    "query": """
    {
      allUsers { id name }
      allMusics { id name}
      allPlaylists { id name }
    }
    """
}

# --- SOAP PYTHON (Spyne) ---
soap_py_users = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.streaming.soap"><soapenv:Header/><soapenv:Body><spy:listar_usuarios/></soapenv:Body></soapenv:Envelope>"""
soap_py_music = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.streaming.soap"><soapenv:Header/><soapenv:Body><spy:listar_musicas/></soapenv:Body></soapenv:Envelope>"""
soap_py_play  = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.streaming.soap"><soapenv:Header/><soapenv:Body><spy:listar_playlists/></soapenv:Body></soapenv:Envelope>"""

# --- SOAP JAVA (Spring WS) ---
soap_jv_users = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="http://example.com/users/soap"><soapenv:Header/><soapenv:Body><sch:GetAllUsersRequest/></soapenv:Body></soapenv:Envelope>"""
soap_jv_music = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="http://example.com/musics/soap"><soapenv:Header/><soapenv:Body><sch:GetAllMusicsRequest/></soapenv:Body></soapenv:Envelope>"""
soap_jv_play  = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="http://example.com/playlists/soap"><soapenv:Header/><soapenv:Body><sch:GetAllPlaylistsRequest/></soapenv:Body></soapenv:Envelope>"""

# Header Obrigatório
soap_headers = {"Content-Type": "text/xml"}

# ==============================================================================
# 2. OS TESTES (CADA CLASSE É UMA TECNOLOGIA)
# ==============================================================================

# ----------------- TIME PYTHON (Portas 8000-8002) -----------------
class PythonREST(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:8000"
    
    @task
    def baixar_tudo(self):
        # Agora baixa TUDO igual ao Java
        self.client.get("/usuarios",  name="1_PY_REST_Users")
        self.client.get("/musicas",   name="1_PY_REST_Music")
        self.client.get("/playlists", name="1_PY_REST_Play")

class PythonGraphQL(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:8001"
    
    @task
    def baixar_tudo(self):
        self.client.post("/graphql", json=gql_py_full, name="2_PY_GRAPH_FullDB")

class PythonSOAP(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:8002"
    
    @task
    def baixar_tudo(self):
        # Adicionado o POST de Playlists que faltava
        self.client.post("/", data=soap_py_users, headers=soap_headers, name="3_PY_SOAP_Users")
        self.client.post("/", data=soap_py_music, headers=soap_headers, name="3_PY_SOAP_Music")
        self.client.post("/", data=soap_py_play,  headers=soap_headers, name="3_PY_SOAP_Play")

# ----------------- TIME JAVA (Porta 8080) -----------------
class JavaREST(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:8080"
    
    @task
    def baixar_tudo(self):
        self.client.get("/rest/users",     name="4_JV_REST_Users")
        self.client.get("/rest/musics",    name="4_JV_REST_Music")
        self.client.get("/rest/playlists", name="4_JV_REST_Play")

class JavaGraphQL(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:8080"
    
    @task
    def baixar_tudo(self):
        self.client.post("/graphql", json=gql_jv_full, name="5_JV_GRAPH_FullDB")

class JavaSOAP(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:8080"
    
    @task
    def baixar_tudo(self):
        self.client.post("/soap", data=soap_jv_users, headers=soap_headers, name="6_JV_SOAP_Users")
        self.client.post("/soap", data=soap_jv_music, headers=soap_headers, name="6_JV_SOAP_Music")
        self.client.post("/soap", data=soap_jv_play,  headers=soap_headers, name="6_JV_SOAP_Play")