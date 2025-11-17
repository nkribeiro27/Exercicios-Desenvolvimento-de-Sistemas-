import pytest
from fastapi.testclient import TestClient
from main import app
from database import tarefas_db

client = TestClient(app)

pytest.fixture(autouse=True)
def limpar_db():
    # Limpa o banco de dados antes de cada teste
    tarefas_db.clear()
# 1.1. Criar uma Nova Tarefa
def test_criar_tarefa_sucesso():
    response = client.post("/tarefas", json={"titulo": "Estudar Python", "descricao": "Revisar conceitos básicos"})
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Estudar Python"
    assert data["descricao"] == "Revisar conceitos básicos"
    assert data["concluida"] is False
    assert "id" in data
# 1.2. Listar Todas as Tarefas
def test_criar_tarefa_falha_titulo_faltando():
    response = client.post("/tarefas", json={"descricao": "Sem título"})
    assert response.status_code == 422  # Unprocessable Entity
#1.3. Obter uma Tarefa Específica por ID
def test_criar_tarefa_falha_titulo_curto():
    response = client.post("/tarefas", json={"titulo": "Ab", "descricao": "Título muito curto"})
    assert response.status_code == 422
#1.4. Atualizar uma Tarefa Existente
def test_listar_tarefas_vazia():
    response = client.get("/tarefas")
    assert response.status_code == 200
    assert response.json() == []
#1.5. Deletar uma Tarefa
def test_listar_tarefas_com_itens():
    client.post("/tarefas", json={"titulo": "Tarefa 1"})
    client.post("/tarefas", json={"titulo": "Tarefa 2"})
    response = client.get("/tarefas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["titulo"] == "Tarefa 1"
    assert data[1]["titulo"] == "Tarefa 2"
#2. Requisitos de Testes Unitários
def test_obter_tarefa_existente():
    response_create = client.post("/tarefas", json={"titulo": "Tarefa Teste"})
    tarefa_id = response_create.json()["id"]
    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Tarefa Teste"

def test_obter_tarefa_nao_existente():
    response = client.get("/tarefas/id-inexistente")
    assert response.status_code == 404

def test_atualizar_tarefa_sucesso():
    response_create = client.post("/tarefas", json={"titulo": "Tarefa Original"})
    tarefa_id = response_create.json()["id"]
    response = client.put(f"/tarefas/{tarefa_id}", json={"titulo": "Tarefa Atualizada", "concluida": True})
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Tarefa Atualizada"
    assert data["concluida"] is True

def test_atualizar_tarefa_id_inexistente():
    response = client.put("/tarefas/id-inexistente", json={"titulo": "Novo Título"})
    assert response.status_code == 404

def test_deletar_tarefa_sucesso():
    response_create = client.post("/tarefas", json={"titulo": "Tarefa para Deletar"})
    tarefa_id = response_create.json()["id"]
    response = client.delete(f"/tarefas/{tarefa_id}")
    assert response.status_code == 204
    # Verificar se não existe mais
    response_get = client.get(f"/tarefas/{tarefa_id}")
    assert response_get.status_code == 404

def test_deletar_tarefa_id_inexistente():
    response = client.delete("/tarefas/id-inexistente")
    assert response.status_code == 404

