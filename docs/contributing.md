# Desenvolvimento

## Preparar o ambiente

```powershell
.\bin\setup.ps1
```

## Verificar antes do commit

```powershell
.\bin\check.ps1
```

## Convenções

- Python 3.13, tipagem estrita e nomes de código em inglês.
- Mensagens, documentação e JSON em português do Brasil.
- Testes são escritos antes da implementação e não acessam rede.
- A camada de domínio não importa widgets nem bibliotecas de provedor de modelo.
- PDFs, áreas de trabalho, chaves e arquivos `.env` não entram no Git.
