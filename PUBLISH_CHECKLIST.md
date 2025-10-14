# Checklist de Publicação ai-tools-mcp-server

## Pré-Requisitos
- [x] Metadados atualizados em pyproject.toml (versão, descrição, classifiers)
- [x] README com instruções Smithery e tabela de variáveis
- [x] smithery.yaml com schema e commandFunction válidos
- [x] Testes passando (pytest)
- [x] CI configurado (.github/workflows/ci.yml)
- [x] Documentos: CONTRIBUTING, SECURITY, CODE_OF_CONDUCT

## Passos para Release
1. Atualizar versão em `pyproject.toml` conforme SemVer
2. Atualizar CHANGELOG (se criado) / README se houver novas features
3. Commit & push:
   ```bash
   git add .
   git commit -m "chore(release): v0.2.0"
   git tag v0.2.0
   git push origin main --tags
   ```
4. Aguardar CI verde no GitHub Actions
5. Publicar no Smithery:
   - Acesse https://smithery.ai
   - Faça login com sua conta GitHub
   - O Smithery detectará automaticamente o repositório e a tag
   - Clique em "Publish" no painel
6. (Opcional) Publicar no PyPI:
   ```bash
   python -m build
   twine upload dist/*
   ```

## Pós-Publicação
- Verificar página do servidor no Smithery
- Testar instalação via:
  ```bash
  npx -y @smithery/cli install dronreef2/ai-tools-mcp-server --client claude
  ```
- Monitorar issues iniciais / feedback

## Próximos Incrementos
- Adicionar métricas avançadas (Prometheus endpoint)
- Internacionalização do dashboard
- Backup automático de configurações (criptografado)

---
Mantido em `PUBLISH_CHECKLIST.md` para transparência e repetibilidade.
