# Adaptbook

O Adaptbook transforma um textbook em PDF em um material de estudo que não depende de áudio, vídeo, links ou aplicativos externos. Ele é feito para quem imprime o livro ou escreve em uma mesa digitalizadora e quer resolver tudo apenas com o PDF final.

A primeira entrega cria uma área de trabalho segura para cada livro. O PDF original continua intacto e os próximos resultados serão gravados na pasta `trabalho/` ao lado dele.

## Início rápido

Pré-requisito: Python 3.13 no Windows.

```powershell
.\bin\setup.ps1
.\.venv\Scripts\adaptbook.exe gui
```

Na janela, selecione o PDF do livro. O Adaptbook criará `trabalho/<nome-do-livro>/`, com `config.yaml`, `manifesto.json` e as pastas das próximas etapas.

## Também pela linha de comando

```powershell
.\.venv\Scripts\adaptbook.exe init "C:\Livros\espanhol-a2.pdf"
```

## Verificação do projeto

```powershell
.\bin\check.ps1
```

O comando verifica formatação, lint, tipos estritos, limites de código, testes, cobertura mínima de 80% e construção do pacote.

## Privacidade e custos

A seleção do livro e as primeiras etapas rodam localmente. Nenhum PDF é enviado para a internet nesta entrega. Chamadas a modelos, quando forem adicionadas, exigirão configuração explícita, mostrarão estimativa de custo e usarão chave de ambiente, nunca arquivo versionado.

## Solução de problemas

Se a janela não abrir, confirme a instalação do Tkinter com:

```powershell
.\.venv\Scripts\python.exe -m tkinter
```

Consulte [a documentação de desenvolvimento](docs/contributing.md) para preparar o ambiente e contribuir.
