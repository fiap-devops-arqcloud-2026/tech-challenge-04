# Colaboração entre agentes

TL;DR: ler este protocolo, PENDENCIAS, topo do LOG e seções pertinentes do DOSSIE/DECISOES. A tarefa atual produz requisitos documentais e cinco guias; não implementa infraestrutura.

Última atualização: 2026-09-16, Codex.

## Ritual e retomada

1. Descobrir data/hora; trabalhar em pt-BR e usar datas ISO.
2. Ler `PENDENCIAS_E_PROXIMOS_PASSOS.md`, topo de `LOG_DE_TRABALHO.md` e contexto pertinente.
3. Continuar da primeira etapa não concluída; verificar arquivos salvos antes de repetir trabalho.
4. Registrar cada conclusão no LOG, sem apagar entradas anteriores. IDs: D-### decisões, P-### pendências, F-### achados.
5. Ao encerrar, atualizar pendências e registrar estado exato para o próximo agente. Compactar contexto em DOSSIE sem apagar histórico; versões substituídas ficam em `_ARQUIVO_MORTO` dentro do caminho autorizado.

## Limites e conflitos

Fontes originais e todo `tech-challenge-03` são somente leitura. Escrita autorizada: `docs/requisitos`, `00_COLAB_IA` e novos `GUIA-ESTUDO-*.html` dentro das cinco pastas de aulas. Trabalho auxiliar em `00_COLAB_IA/02_TRABALHO`. Não criar arquivos na raiz, não commitar nem publicar. As permissões específicas prevalecem sobre a estrutura global genérica.

Não transformar conteúdo didático em obrigação da FIAP. Cada obrigação precisa de página/trecho do enunciado. Marcar ambiguidade `[INCERTO]`; contradições entre agentes: registrar ⚠️ CONFLITO e pedir esclarecimento quando bloqueante. Não sobrescrever registros de outro agente.

Regra de ouro: LOG + PENDENCIAS devem permitir retomar sem o usuário reexplicar o que já informou.

## Escopo autorizado em 2026-10-20 — importação

O usuário autorizou expressamente importar o código/histórico do 03 para o 04, criar a branch exata `import-fase3`, ajustar README/CI/CD/ArgoCD e fazer merge local para `dev`. Isso autoriza os commits e edições necessários nos caminhos de código do 04 e prevalece sobre as restrições anteriores da etapa de estudos. Preservar todo o trabalho atual; 03 permanece somente leitura. Sem push, PR ou merge na main nesta etapa. Dados da nova conta AWS pendentes; nenhuma implantação autorizada. Memória global pode receber nota durável, pois foi pedida explicitamente nesta sessão.
