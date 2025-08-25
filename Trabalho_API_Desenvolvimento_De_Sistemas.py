from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

app = FastAPI(
    title="API de Cadastro de Alunos",
    description="API deverá permitir o cadastro de alunos, bem como a atualização e exclusão de registros já existentes.",
    version="1.0.0"
)

class Aluno(BaseModel):
    nome: str
    turma: int
    idade: int
    matricula:int

# "Banco de dados" em memória (um dicionário Python)
db_aluno: Dict[int, Aluno] = {
    1: Aluno(matricula = 123, nome="Nikolas", turma=204 , idade=16),
    2: Aluno(matricula = 345, nome="Izabelly", turma= 205, idade=17),
    3: Aluno(matricula = 678, nome="Janaina",  turma=201, idade=15),
}

@app.get("/")
def read_root():
    """Endpoint raiz da API."""
    return {"message": "Bem-vindo à API de Alunos! Acesse /docs para a documentação interativa."}

@app.get("/Aluno")
def pegar_todos_alunos():
    """Retorna todos os alunos matriculados."""
    return db_aluno

@app.get("/Aluno/{matricula}")
def pegar_aluno_por_matricula(matricula: int):
    """Retorna um aluno específico pela sua matricula."""
    if matricula not in db_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    return db_aluno[matricula]

@app.post("/Aluno/{matricula}}", status_code=status.HTTP_201_CREATED)
def criar_Aluno(matricula: int, aluno: Aluno):
    """Cria um novo Aluno com um matricula específica."""
    if id in db_aluno:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esse Aluno já existe")
    
    db_aluno[matricula] = aluno
    return {"message": "Aluno cadastrado com sucesso!", "Matricula": matricula, "Aluno": aluno}

@app.put("/Aluno/{matricula}")
def atualizar_Aluno(matricula: int, aluno: Aluno):
    """Atualiza as informações de um Aluno existente."""
    if matricula not in db_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    
    db_aluno[matricula] = Aluno
    return {"message": "Cadastro do Aluno atualizado com sucesso!", "Aluno": Aluno}

@app.delete("/Aluno/{matricula}")
def deletar_Aluno(matricula: int):
    """Deleta o cadastro de um Aluno."""
    if matricula not in db_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    
    del db_aluno[matricula]
    return {"message": "Aluno deletado com sucesso!"}