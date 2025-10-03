# Bedrock Hello World

## Pré-requisitos

- Python 3.7 ou superior
- Credenciais AWS configuradas (AWS CLI ou variáveis de ambiente)
- Permissões adequadas para acessar o AWS Bedrock

## Configuração do Ambiente

### 1. Criar um Ambiente Virtual

Para isolar as dependências do projeto, crie um ambiente virtual usando o comando:

```bash
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual

**No Linux/macOS:**
```bash
source .venv/bin/activate
```

**No Windows:**
```bash
.venv\Scripts\activate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Configuração de Permissões

### Tornar o Script Executável

Para poder executar o script `bedrock.py` diretamente, você precisa adicionar permissão de execução:

```bash
chmod +x 1_bedrock.py
```

### Configurar Credenciais AWS

Certifique-se de ter suas credenciais AWS configuradas. Você pode fazer isso de várias formas:

**Opção 1: Usando AWS CLI**
```bash
aws configure
```

## Como Executar

Existem duas formas de executar o projeto:

### Forma 1: Executar diretamente (após chmod +x)

```bash
./1_bedrock.py
```

### Forma 2: Usando o interpretador Python

```bash
python 1_bedrock.py
```

## Estrutura do Projeto

```
bedrock/
├── bedrock.py                              # Script principal
├── requirements.txt                        # Dependências do projeto
├── aws-setup/
│   └── apply_bedrock_permissions.py       # Script auxiliar para configurar permissões
└── README.md                               # Este arquivo
```

## Funcionalidades

O script `bedrock.py` fornece:

- **get_bedrock_client()**: Cria e configura um cliente AWS Bedrock
- **list_bedrock_models()**: Lista todos os modelos de fundação disponíveis no Bedrock

## Configuração de Permissões AWS (Opcional)

Se você encontrar erros de permissão ao executar o script, pode usar o script auxiliar para configurar as permissões necessárias:

```bash
python aws-setup/apply_bedrock_permissions.py
```

Este script irá:
- Verificar sua configuração AWS
- Aplicar as políticas necessárias para acessar o Bedrock
- Testar o acesso ao serviço

## Saída Esperada

Ao executar o script com sucesso, você verá uma lista de modelos como:

```
Model ID: amazon.titan-text-express-v1
Provider: Amazon
Model Name: Titan Text G1 - Express
--------------------------------------------------
Model ID: anthropic.claude-v2
Provider: Anthropic
Model Name: Claude
--------------------------------------------------
...
```

## Solução de Problemas

### Erro de Credenciais

Se você receber um erro relacionado a credenciais AWS:
- Verifique se suas credenciais estão configuradas corretamente
- Confirme que tem acesso à região `eu-central-1` (ou altere a região no código)

### Erro de Permissões

Se você receber um erro de permissões:
- Execute o script `aws-setup/apply_bedrock_permissions.py` para configurar as permissões
- Ou adicione manualmente a política `AmazonBedrockFullAccess` ao seu usuário/role IAM

### Erro ao Listar Modelos

Se você não conseguir listar os modelos:
- Verifique se o serviço Bedrock está disponível na sua região
- Confirme que você tem as permissões `bedrock:ListFoundationModels`

# Resources
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-1-0-text-image.html