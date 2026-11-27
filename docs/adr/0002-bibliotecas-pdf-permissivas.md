# ADR-0002 — Bibliotecas PDF permissivas

## Status

Aceito em 26/11/2026.

## Contexto

O projeto será publicado no GitHub e não deve exigir licença comercial para desenvolver ou usar a ferramenta localmente. PyMuPDF oferece os recursos necessários, mas sua licença AGPL ou comercial imporia uma decisão jurídica adicional.

## Decisão

Usar `pdfplumber==0.11.10` para texto e coordenadas, `pypdf==7.2.0` para montagem e carimbos, e `pypdfium2==5.15.2` para renderização de prévias.

## Consequências

As bibliotecas são permissivas, mas a extração poderá ser mais lenta que PyMuPDF. O Marco 1 medirá essa diferença em PDFs digitais; a troca futura exigirá novo ADR e benchmark reproduzível.
