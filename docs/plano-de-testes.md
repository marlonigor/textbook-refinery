# Plano de testes

## Comando único

`bin/check.ps1` executa formatação, lint, tipagem, limites de código, testes, cobertura e construção do pacote.

## Pirâmide

| Camada | Objetivo |
| --- | --- |
| Unitária | Configuração, nomes de pasta, validações e mensagens. |
| Integração | CLI e interface usando a mesma regra de criação de área de trabalho. |
| Sintética | PDFs pequenos gerados para detecção, OCR, segmentação e ligação de transcrições. |
| Golden | Dois livros reais mantidos fora do Git, ativados por variável de ambiente. |
| Manual | Acrobat Reader, Chrome e mesa digitalizadora indicada pela pessoa usuária. |

## Marco 1 — fatia inicial

Os testes confirmam que um PDF com caminho contendo espaços cria `config.yaml` e `manifesto.json`, que a entrada não é modificada, que destino existente é recusado sem sobrescrita e que a interface apresenta sucesso ou erro adequadamente.
