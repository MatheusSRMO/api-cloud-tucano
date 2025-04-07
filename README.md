# 📦 Flask S3 File API

Uma API simples em Flask que permite realizar upload, listagem, exclusão e renomeação de arquivos em um bucket S3 da AWS. Os metadados dos arquivos são armazenados em um banco de dados SQLite.

> Dockerizada para fácil deploy e desenvolvimento local.

---

## 🚀 Funcionalidades

- 📤 Upload de arquivos para S3
- 📄 Listagem de arquivos com metadados
- 🗑️ Remoção de arquivos do S3
- ✏️ Renomear arquivos diretamente no S3

---

## 🛠️ Tecnologias

- Python 3.11
- Flask
- SQLAlchemy
- SQLite
- Amazon S3 (via `boto3`)
- Docker + Docker Compose

---

## 📁 Estrutura do Projeto

```
flask-s3-api/
├── app.py               # Arquivo principal da aplicação Flask
├── models.py            # Modelos do SQLAlchemy
├── config.py            # Configurações da aplicação
├── requirements.txt     # Dependências do projeto
├── Dockerfile           # Container Docker da API
├── docker-compose.yml   # Orquestração do Docker
├── .env                 # Variáveis de ambiente (NÃO versionar!)
└── README.md            # Documentação
```

---

## ⚙️ Configuração

1. **Clone o repositório:**

```bash
git clone https://github.com/MatheusSRMO/flask-s3-api.git
cd flask-s3-api
```

2. **Crie um arquivo `.env` com suas credenciais da AWS:**

```env
AWS_ACCESS_KEY=sua_chave
AWS_SECRET_KEY=sua_chave_secreta
AWS_REGION=us-east-1
S3_BUCKET_NAME=seu_bucket
```

---

## 🐳 Rodando com Docker

### Build e start

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:5000`

---

## 📡 Endpoints da API

### `POST /upload`

> Upload de arquivo para o S3

**Body (form-data):**

- `file`: Arquivo que será enviado

**Response:**

```json
{
  "message": "Arquivo enviado",
  "s3_url": "https://tucano-cloud.s3.amazonaws.com/nome_do_arquivo"
}
```

---

### `GET /files`

> Lista todos os arquivos cadastrados no banco

**Response:**

```json
[
  {
    "id": 1,
    "filename": "arquivo.jpg",
    "s3_url": "https://bucket.s3.amazonaws.com/arquivo.jpg"
  }
]
```

---

### `DELETE /file/<id>`

> Remove o arquivo do S3 e do banco

**Response:**

```json
{
  "message": "Arquivo deletado"
}
```

---

### `PUT /file/<id>`

> Renomeia o arquivo no S3

**Body (JSON):**
```json
{
  "new_name": "novo_nome.jpg"
}
```

**Response:**
```json
{
  "message": "Arquivo renomeado",
  "s3_url": "https://bucket.s3.amazonaws.com/novo_nome.jpg"
}
```

---

## ✅ Checklist para produção

- [ ] Usar PostgreSQL ou outro banco persistente em vez de SQLite
- [ ] Adicionar autenticação (JWT, API Key, etc.)
- [ ] Limitar tamanho/tipo dos arquivos no upload
- [ ] Criar testes unitários com `pytest`

---

## 📄 Licença

MIT © 2025 — Desenvolvido por [Matheus Ribeiro](https://github.com/MatheusSRMO)
