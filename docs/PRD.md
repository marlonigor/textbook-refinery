# PRD — Adaptbook

## Problema e objetivo

O Adaptbook gera uma versão autossuficiente de textbooks de idiomas em PDF. O aluno mantém tudo que já funciona no papel e recebe folhas substitutas para atividades que exigiriam recursos externos.

## Usuário e interface

Uma única pessoa usa o aplicativo localmente no Windows com Python 3.13. A interface é desktop, com CLI equivalente para automação. Não há interface web, login, banco de dados ou multiusuário.

## Requisitos funcionais

| ID | Requisito |
| --- | --- |
| RF-01 a RF-03 | Receber PDFs e anexos, extrair texto posicionado e gerar mapa de unidades, atividades, transcrições e gabaritos. |
| RF-04 a RF-07 | Detectar dependências, ligar transcrições, gerar auditoria e permitir revisão em XLSX. |
| RF-08 a RF-11 | Adaptar, validar, inserir folhas no modo A e acrescentar gabarito das adaptações. |
| RF-12 a RF-14 | Retomar execução, estimar custo e aceitar configuração por livro. |
| RF-15 a RF-18 | Rotular páginas, agrupar ícones, verificar o PDF e emitir relatório final. |
| RF-19 a RF-22 | Aceitar anexos, proteger a entrada, registrar manifesto e exibir status. |
| RF-23 a RF-27 | Carimbar páginas de saída, segmentar atividades, ligar faixas a transcrições, revisar adaptações e tratar texto do livro como dado. |
| RF-28 | Oferecer uma interface desktop para executar cada etapa sem depender da CLI. |
| RF-29 | Tornar cada etapa testável visualmente, com prévia, estado, erros acionáveis e progresso real. |

## Regras pedagógicas

1. Preservar atividades resolvíveis com o PDF.
2. Manter idioma, nível CEFR, vocabulário e objetivo da unidade.
3. Reutilizar transcrição original quando existir.
4. Identificar material novo como “Material adaptado”.
5. Gerar gabarito e critérios para respostas abertas.
6. Declarar mudanças de habilidade, como audição para leitura.
7. Nunca mencionar recursos externos na folha adaptada.

## Requisitos não funcionais

- Processamento local e envio mínimo de dados somente após configuração de modelo.
- Estado atômico por atividade, logs em português e sem segredos.
- Tipagem estrita, testes automatizados e cobertura mínima de 80% nos arquivos alterados.
- Meta futura: 300 páginas digitais em até cinco minutos e dry-run em até um minuto.
- MVP para escrita latina: espanhol, francês, inglês, português, italiano e alemão.

## Critérios de aceite

O conjunto golden terá dois livros reais fora do repositório, um digital e um escaneado, com verdade anotada manualmente. A meta é recall de 100%, até 5% de falsos positivos, 95% de segmentação correta, PDF final verificável e retomada sem retrabalho.

## Fora de escopo

Gerar áudio ou vídeo, traduzir livros, modificar atividades que já funcionam, distribuir livros de terceiros e substituir exercícios dentro do layout original no modo B.
