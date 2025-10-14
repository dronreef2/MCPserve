# Contribuindo para ai-tools MCP Server

Obrigado por considerar contribuir! Este projeto segue boas práticas para servidores MCP publicados no Smithery.

## Fluxo de Trabalho
1. Abra uma issue descrevendo a mudança proposta
2. Crie um fork e uma branch: `feat/nome-da-feature`
3. Adicione/ajuste testes (`pytest`)
4. Rode lint e testes localmente
5. Atualize a documentação (README / CHANGELOG se aplicável)
6. Abra o Pull Request referenciando a issue

## Padrões de Código
- Python >= 3.11
- Estilo verificado por `ruff` (CI falhará se houver violação)
- Linhas até 100 colunas
- Funções curtas e coesas
- Logging estruturado em vez de prints

## Commits
Use mensagens claras:
```
feat: adiciona suporte a tradução DeepL
fix: corrige validação de URL em fetch
chore: atualiza dependências
refactor: simplifica cache decorator
```

## Testes
Execute:
```bash
pytest
```
Para rodar um teste específico:
```bash
pytest -k nome_teste
```

## Segurança
- Nunca commit chaves de API
- Valide entrada do usuário
- Revise dependências antes de adicionar

## Processo de Release
1. Atualize versão em `pyproject.toml`
2. Gere tag semver: `git tag vX.Y.Z && git push --tags`
3. Confirme pipeline CI verde
4. Publicar no Smithery e PyPI (futuro)

## Suporte
Dúvidas? Abra uma issue.
