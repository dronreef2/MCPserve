# Política de Segurança

## Reportando Vulnerabilidades
Se você encontrar uma vulnerabilidade, envie um email ou abra uma issue marcada como `security` (sem detalhes exploráveis publicamente). Forneça:
- Descrição
- Passos para reproduzir
- Impacto estimado

## Escopo
- Exposição de chaves
- Execução remota não autorizada
- Falhas de autenticação/Autorização
- Injeção (command, code, template)

## Boas Práticas Internas
- Sanitização de entrada nas ferramentas
- Uso de HTTPS para APIs externas
- Não armazenar chaves em texto plano (hash de API keys)
- Menor privilégio em containers

## Ciclo de Correção
1. Confirmação em 72h
2. Correção/mitigação
3. Release patch com changelog

## Dependências
Monitoramos dependências com atualizações periódicas; patches críticos são priorizados.
