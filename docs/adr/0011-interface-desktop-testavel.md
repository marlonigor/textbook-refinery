# ADR-0011 — Interface desktop testável por etapa

## Status

Aceito em 26/11/2026.

## Contexto

O fluxo original previa apenas CLI. A pessoa usuária pediu uma interface gráfica e resultados que possam ser vistos e testados em cada funcionalidade entregue.

## Decisão

Usar Tkinter, incluído no Python para Windows, como interface desktop inicial. A CLI permanece como camada de automação. Cada marco entregará uma fatia utilizável com ação principal única, progresso real, mensagens de erro e prévia quando houver artefato visual.

## Consequências

O código de regras fica independente dos widgets por meio de interfaces injetadas. A aparência segue a identidade “biblioteca contemporânea”, com contraste acessível, foco por teclado e sem dependências de interface adicionais.
