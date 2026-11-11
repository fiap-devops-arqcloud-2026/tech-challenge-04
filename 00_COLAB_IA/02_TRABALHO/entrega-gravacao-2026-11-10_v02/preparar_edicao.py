"""Atualização pontual da edição 2026-11-10; executar apenas uma vez."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
data_path = ROOT / 'docs/gravacao/roteiro-conteudo.json'
data = json.loads(data_path.read_text(encoding='utf-8-sig'))
data['date'] = '2026-11-10'
data['recording_date'] = '2026-11-10'
data['scenes'][4]['command'] = '{k8s_namespace_name="togglemaster"}'
data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

md = ROOT / 'docs/gravacao/README.md'
t = md.read_text(encoding='utf-8-sig').replace('Atualizado em 2026-11-09.', 'Atualizado em 2026-11-10. Gravação planejada para 2026-11-10.')
t = t.replace('## Antes de apertar REC', '''## Materiais prontos para abrir

- [Roteiro em PDF](ROTEIRO_GRAVACAO_2026-11-10_v02.pdf): uma cena por página, ações e fala completa.
- [PowerPoint editável](ROTEIRO_GRAVACAO_2026-11-10_v02.pptx): as mesmas cenas, com notas do apresentador.
- [Relatório com evidências](../relatorio/README.md): participantes e prints do ensaio de 2026-11-09; URL do vídeo pendente.
- [Índice dos prints](../evidencias/README.md): origem, horário e o que cada imagem comprova.

O ensaio integrado de 2026-11-09 foi concluído: falha 503, Firing, PagerDuty/Slack, execução automática e recuperação. [Execução comprovada](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42679005683). A gravação deve mostrar uma execução atual, não apenas reproduzir os prints.

## Antes de apertar REC''')
t=t.replace('- A fala é sugerida.', '- Confirme o enquadramento do **Service Map com os cinco serviços**: a captura existente é do mapa de um trace, não do mapa global. Abra dependências adicionais e ajuste o período no New Relic antes de gravar.\n- A fala é sugerida.')
md.write_text(t,encoding='utf-8')
cmd=ROOT/'docs/gravacao/COMANDOS.md'
t=cmd.read_text(encoding='utf-8').replace('Atualizado em 2026-11-09.', 'Atualizado em 2026-11-10.').replace('{k8s_namespace_name="togglemaster"} |= "flag-service"','{k8s_namespace_name="togglemaster"}')
t=t.replace('Use um período com tráfego.','A consulta inicial mostra o namespace inteiro. Para focar um serviço, selecione seu rótulo disponível no Explore, sem presumir que o nome esteja no corpo de todas as linhas. Use um período com tráfego.')
cmd.write_text(t,encoding='utf-8')

deck=WORK/'build_deck.mjs'
t=deck.read_text(encoding='utf-8').replace("const build=import.meta.dirname;", "const build=path.join(root,'00_COLAB_IA/02_TRABALHO/validacao-local-entrega-2026-11-10');\nawait fs.mkdir(build,{recursive:true});")
t=t.replace('2026-11-09','2026-11-10')
t=t.replace("const runtime='C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies';", "const runtime=process.env.ARTIFACT_RUNTIME_ROOT || 'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies';")
t=t.replace('Da observabilidade à recuperação automática','Observabilidade e recuperação automática').replace('Quatro prints. Uma entrega verificável.','Quatro prints para o relatório')
deck.write_text(t,encoding='utf-8')

p=WORK/'build_pdf.py'
t=p.read_text(encoding='utf-8').split('# Report uses authentic captures.')[0]
t=t.replace('2026-11-09_v01.pdf','2026-11-10_v02.pdf').replace('FASE 4  |  2026-11-09','FASE 4  |  2026-11-10').replace('Edição: 2026-11-09','Edição: 2026-11-10').replace('Da observabilidade à recuperação automática','Observabilidade e recuperação automática')
t=t.replace("p=Paragraph(escape(t).replace('\\n','<br/>'),st)","p=Paragraph(escape(t.replace('–','-').replace('—','-')).replace('\\n','<br/>'),st)")
p.write_text(t,encoding='utf-8')

meta=ROOT/'docs/relatorio/dados-entrega.json'
d=json.loads(meta.read_text(encoding='utf-8-sig'))
d['ultima_atualizacao']='2026-11-10'
d['status']='Evidências do ensaio concluído em 2026-11-09. URL do vídeo pendente de gravação e publicação.'
d['run_url']='https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42679005683'
d['chatops']='Slack, 2026-11-09 16:01 UTC-03: notificação Resolved de FlagService5xxAlto. O início indicado, 18:59:20 UTC, corresponde ao alerta do ensaio. A captura preserva um erro de formatação no resumo; detecção e recuperação funcionaram.'
d['selfhealing']='Execução 42679005683, iniciada por repository_dispatch, sucesso em 43 s. O log mostra o restart do flag-service e o rollout concluído às 19:00:03 UTC (16:00:03 UTC-03), sem intervenção manual.'
d['incidente']='PagerDuty #4 resolvido; HTTP 200 observado após o restart automático.'
meta.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Conteúdo e geradores preparados para 2026-11-10.')
