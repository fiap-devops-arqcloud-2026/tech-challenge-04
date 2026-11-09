"""Guia didático baseado nos oito PDFs locais; não executa exemplos das aulas."""
from guia_base import E, badge, section, table, complement, code, write_guide
from urllib.parse import quote

def ref(n, pages):
    first = str(pages).split('–')[0].split(',')[0]
    name = f'POSTECH - Monitoramento Opensource - Aula {n}.pdf'
    return f'<p class="source">Fonte: <a href="{quote(name)}#page={first}">{E(name)}, p. {E(str(pages))}</a>. Leitura em 2026-09-16.</p>'

def bs(*ids):
    return '<p>'+''.join(badge(i) for i in ids)+'</p>'

def card(n, title, body):
    return '<article class="lesson"><div class="lesson-head"><span class="num">'+str(n).zfill(2)+'</span><div><h3>'+title+'</h3><span class="badge ok">Ficha de aula</span></div></div>'+body+'</article>'

content = section('visao-geral','Uma stack, responsabilidades diferentes', '''
<div class="intro"><div class="box"><h3>Em miúdos</h3><p>Este módulo mostra como reunir os sinais de saúde de um sistema. Prometheus trabalha com números ao longo do tempo; Loki com registros de eventos; Jaeger com o caminho das requisições; Grafana com a visualização; OTel e Alloy com a instrumentação e o transporte da telemetria.</p></div><div class="box hi"><h3>No projeto</h3><p>A Fase 4 exige Prometheus, Loki, Grafana e centralização no OTel. A aula de Jaeger ensina tracing, mas a demonstração exigida usa Datadog ou New Relic. Zabbix é conteúdo da disciplina; não aparece como exigência no enunciado.</p></div></div>
<p>Estude primeiro o papel de cada ferramenta, depois a forma como os dados chegam até ela e, por fim, como uma investigação cruza os três sinais. As aulas 7 e 8 unem os conceitos ao Kubernetes. Nível predominante: introdutório a intermediário; os PDFs fornecem base conceitual e remetem a videoaulas para instalação e configuração.</p>
''' + ref(8,'5–10') + bs('REQ-OBR-07','REQ-OBR-08','REQ-OBR-09','REQ-OBR-11','REQ-OBR-12') + '''
<aside class="warning"><strong>Limite do material disponível.</strong> Foram lidos os oito PDFs completos, 118 páginas. A pasta não contém os vídeos, transcrições, scripts ou manifestos citados no Hands On. Por isso, este guia explica o conteúdo efetivamente disponível e transcreve a consulta LogQL presente na aula; não inventa comandos de instalação. Veja as ressalvas editoriais na seção final.</aside>
''')

content += section('mapa','Mapa de ferramentas e vocabulário', table(
    ['Ferramenta','Responsabilidade estudada','Conceito para memorizar','Fonte'],[
    ('Zabbix','Monitoramento de hosts, infraestrutura e rede; itens, triggers e ações.','Host → item → trigger → evento → ação.','Aula 1, p. 5–10'),
    ('Prometheus','Coleta e consulta de séries temporais de métricas.','Scrape busca a métrica; PromQL consulta a série.','Aula 2, p. 5–9'),
    ('Grafana','Consulta várias fontes e organiza painéis, dashboards e alertas.','Data source ≠ query ≠ panel.','Aula 3, p. 5–8'),
    ('Loki','Recebe fluxos de logs, indexa labels e guarda chunks.','Selecionar o fluxo antes de filtrar o texto.','Aula 4, p. 5–9'),
    ('Jaeger','Armazena/consulta traces e permite visualizar spans relacionados.','Trace é a jornada; span é uma operação.','Aula 5, p. 5–11'),
    ('OpenTelemetry','Padroniza geração, coleta e exportação de métricas, logs e traces.','API define operações; SDK as implementa.','Aula 6, p. 5–9'),
    ('Grafana Alloy','Distribuição do Collector; recebe, processa e exporta sinais.','Receiver → processor → exporter.','Aula 6, p. 7–9'),
    ('Kubernetes','Reconcilia o estado desejado de aplicações em contêineres.','Pod, Service, Deployment e Node têm funções distintas.','Aula 7, p. 7–10')
]) + '''<div class="glossary">
<div class="term"><span class="k">Telemetria</span><span class="d">Dados emitidos/coletados para observar o sistema: métricas, logs e traces (Aula 6, p. 5–7).</span></div>
<div class="term"><span class="k">Label</span><span class="d">Par chave-valor usado para identificar ou filtrar séries/fluxos; combinações demais aumentam cardinalidade (Aula 2, p. 9; Aula 4, p. 6).</span></div>
<div class="term"><span class="k">Target / exporter</span><span class="d">Alvo de coleta / adaptador que expõe métricas de outro sistema ao Prometheus (Aula 2, p. 6).</span></div>
<div class="term"><span class="k">Trace / span</span><span class="d">Jornada distribuída / unidade de trabalho com início, fim e atributos (Aula 5, p. 7–8).</span></div>
<div class="term"><span class="k">OTLP</span><span class="d">Protocolo OpenTelemetry para transportar telemetria; não é um banco de dados (Aula 6, p. 9; Aula 8, p. 8–9).</span></div>
<div class="term"><span class="k">Sampling</span><span class="d">Seleção de traces para equilibrar volume e visibilidade (Aula 5, p. 10; Aula 6, p. 10).</span></div>
</div>''')

content += section('aula-1','Aula 1 — Métricas com Zabbix', card(1,'Monitorar, avaliar e agir', '''
<dl class="facets"><div><dt>Em miúdos</dt><dd>O Zabbix acompanha os sinais vitais de servidores, redes e aplicações. A aula usa o exemplo de um e-commerce sob alta demanda: observar tempo de resposta, banco e capacidade permite avisar a equipe antes de uma interrupção.</dd></div><div><dt>Para que serve</dt><dd>Coletar dados, avaliar condições de problema e organizar respostas, incluindo notificação e escalonamento.</dd></div></dl>
''' + ref(1,'5–6') + table(['Entidade','Significado','Exemplo apresentado ou função'],[
    ('Host','Dispositivo monitorado.','Servidor, estação de trabalho ou switch.'),
    ('Item','Métrica coletada no host.','CPU, memória livre ou tráfego de rede.'),
    ('Trigger','Expressão que define condição de problema.','CPU acima de 90% por mais de 5 minutos: exemplo da aula, não limiar obrigatório da entrega.'),
    ('Event','Ocorrência registrada.','Mudança de estado da trigger ou descoberta de dispositivo.'),
    ('Action','Resposta a um evento.','Notificar, executar comando remoto ou escalar.'),
    ('Template','Conjunto de configuração reutilizável.','Itens, triggers e gráficos aplicáveis a hosts semelhantes.')
]) + ref(1,6) + '''
<h4>Da coleta até a notificação</h4><ol class="flow">
<li><div><strong>Host e Agent</strong><span>O agente coleta informações locais. A aula distingue Agent tradicional e Agent 2, extensível com plugins.</span></div></li>
<li><div><strong>Proxy, quando necessário</strong><span>Intermedia coleta em filiais ou redes segmentadas, guarda dados localmente e os envia ao servidor.</span></div></li>
<li><div><strong>Server e banco</strong><span>O Server coordena coleta e avaliação. Configuração e histórico são persistidos no banco.</span></div></li>
<li><div><strong>Trigger, evento e ação</strong><span>A condição avaliada pode gerar evento e resposta. A interface web reúne administração e visualização.</span></div></li>
</ol>''' + ref(1,'7–8') + '''
<h4>Boas práticas da aula</h4><ul><li>Reutilizar templates e ajustar frequência à criticidade da métrica.</li><li>Usar duração e histerese para evitar oscilação entre OK e PROBLEMA.</li><li>Definir severidade e escalonamento; um evento crítico pode exigir outro canal de aviso.</li><li>Planejar retenção do histórico e das tendências; monitorar a saúde do próprio Zabbix.</li><li>Proteger interface, permissões e comunicação com TLS.</li></ul>
''' + ref(1,'8–10') + complement('''<p><strong>Como transferir o raciocínio ao ToggleMaster:</strong> separar a medição da condição de alerta e da resposta ajuda a desenhar o fluxo Grafana/APM → incidente → automação. Isso é uma analogia didática; instalar Zabbix não substitui as ferramentas exigidas pela Fase 4.</p>''') + bs('SUG-02') + '''<p><strong>Para memorizar:</strong> item mede; trigger avalia; evento registra; ação responde. O Hands On da p. 4 anuncia prática de instalação e configuração, mas não fornece os comandos no PDF.</p>'''))

content += section('aula-2','Aula 2 — Prometheus em sistemas dinâmicos', card(2,'Transformar medições em séries temporais', bs('REQ-OBR-07','REQ-OBR-10') + '''
<dl class="facets"><div><dt>Em miúdos</dt><dd>Uma leitura isolada de CPU conta pouco. Uma sequência com data e hora mostra se o consumo está crescendo, se o pico é recorrente ou se acompanha uma mudança no sistema.</dd></div><div><dt>Tecnicamente</dt><dd>O Prometheus coleta métricas de targets por HTTP, guarda séries temporais e permite consultas PromQL. Aplicações instrumentadas e exporters expõem dados no formato esperado.</dd></div></dl>
''' + ref(2,'5–7') + '''
<div class="diagram" aria-label="Fluxo conceitual do Prometheus"><div class="node">Aplicação ou exporter<br><small>expõe métricas</small></div><span aria-hidden="true">→</span><div class="node">Prometheus<br><small>faz scrape e armazena</small></div><span aria-hidden="true">→</span><div class="node">PromQL / Grafana<br><small>consulta e visualiza</small></div></div>
<p>A seta acima representa o trajeto dos dados; no modelo <em>pull</em>, a requisição de coleta parte do Prometheus. O <strong>Alertmanager</strong> administra notificações dos alertas gerados. O <strong>Pushgateway</strong> é apresentado para jobs de curta duração, que enviam métricas ao intermediário. Não é uma necessidade universal de toda aplicação.</p>
''' + ref(2,6) + '''<h4>PromQL: tipo de dado e tipo de consulta</h4>''' + table(['Distinção','O que significa','Cuidado de estudo'],[
    ('Instant query','Avalia uma expressão em um ponto no tempo.','É diferente de desenhar a evolução de uma expressão.'),
    ('Range query','Repete a avaliação em instantes igualmente espaçados dentro de um intervalo.','A aula associa essa visualização à aba Graph.'),
    ('Instant vector','Conjunto de séries, uma amostra por série.','Não confundir com um único número.'),
    ('Range vector','Conjunto de amostras ao longo de uma janela para cada série.','É um tipo de dado da expressão, não sinônimo de range query.'),
    ('Scalar / string','Valor numérico simples / texto.','Os tipos interferem nas operações possíveis.')
]) + ref(2,'7–8') + '''
<h4>Cuidados que fazem diferença</h4><p>A aula recomenda labels consistentes e evitar alta cardinalidade. Também apresenta <em>recording rules</em> para pré-calcular consultas custosas. Prometheus lida com métricas numéricas; logs precisam de uma solução como Loki. Thanos e Cortex são citados para cenários de retenção longa, sem serem requisitos da Fase 4.</p>
''' + ref(2,9) + complement('''<p><strong>Exemplo didático:</strong> identificar uma métrica por serviço e ambiente permite comparar grupos estáveis. Colocar um identificador único de usuário em cada série multiplica combinações e dificulta a operação. Para o dashboard do desafio, separe recursos do cluster e taxa de requisições; eles respondem a perguntas diferentes. A consulta exata depende das métricas realmente expostas.</p>''') + '''
<p><strong>Para memorizar:</strong> coletar não é consultar; label identifica; PromQL seleciona e agrega; Grafana visualiza. O <code>prometheus.yml</code> e as queries são mencionados no Hands On, p. 4, mas o PDF não contém uma configuração ou comando completo para copiar.</p>'''))

content += section('aula-3','Aula 3 — Grafana, visualização e alertas', card(3,'Fazer uma pergunta útil aos dados', bs('REQ-OBR-09','REQ-OBR-10','REQ-OBR-16') + '''
<p><strong>Em miúdos:</strong> o Grafana reúne visualizações de dados que vivem em outros sistemas. Um painel deve ajudar alguém a tomar uma decisão: identificar degradação, localizar um serviço ou comparar um período.</p><p><strong>Tecnicamente:</strong> a aula divide a plataforma em servidor e interface web. Data sources conectam os backends; queries buscam dados; painéis os apresentam. Um dashboard organiza os painéis, e variáveis permitem selecionar contexto sem criar uma cópia para cada servidor ou ambiente.</p>
''' + ref(3,'5–7') + table(['Componente','Pergunta que resolve','Relação com os demais'],[
    ('Data source','De onde vêm os dados?','Prometheus, bancos, CloudWatch e outras fontes citadas na aula.'),
    ('Query','Quais dados quero?','Usa a linguagem da fonte: PromQL, SQL etc.'),
    ('Transformation','Como preparar o resultado?','Filtra, combina, calcula ou renomeia campos retornados.'),
    ('Visualization / panel','Como tornar o resultado legível?','Gráfico, tabela, gauge ou mapa de calor.'),
    ('Dashboard / row','Como organizar a visão?','Agrupa painéis e linhas em uma tela.'),
    ('Variable','Qual contexto quero selecionar?','Menus reutilizam a mesma visão para recursos diferentes.'),
    ('Alert','Quando uma condição pede atenção?','Regra baseada em consulta pode gerar notificação.')
]) + ref(3,'5–6') + '''
<p>O exemplo de CPU acima de 90% por mais de 5 minutos ilustra um limiar com duração. Os valores não são prescrições para o ToggleMaster. Começar com métricas-chave, usar variáveis, organizar dashboards em pastas e otimizar consultas são recomendações da aula.</p>
''' + ref(3,'6–8') + complement('''<p><strong>Roteiro de dashboard para estudar a entrega:</strong> um bloco com recursos do cluster, outro com taxa de requisições dos microsserviços e um painel de logs. A composição mínima vem de REQ-OBR-10; disposição, cores e seleção por serviço são decisões de apresentação. Durante a demonstração, explique a fonte e a consulta de cada painel, e use dados gerados pelo teste.</p><p><strong>Distinção importante:</strong> a frase da aula “Grafana não armazena dados” refere-se ao papel de visualização dos sinais neste fluxo. Ela não significa que a aplicação não possua configuração, usuários ou dashboards persistidos.</p>''') + bs('REQ-OBR-26','REQ-OBR-35') + '''
<p><strong>Erro comum:</strong> um dashboard bonito com consultas vazias não evidencia o sistema operando. A evidência prática é exigida no enunciado, p. 5, e deve mostrar os dados reais da demonstração.</p><p><strong>Para memorizar:</strong> fonte → consulta → preparação → visualização; condição → alerta. Correlacionar os sinais ajuda a investigar, mas exige que os dados sejam compatíveis e estejam disponíveis.</p>'''))

content += section('aula-4','Aula 4 — Logs com Loki', card(4,'Encontrar eventos sem indexar todo o texto', bs('REQ-OBR-08','REQ-OBR-10') + '''
<p><strong>Em miúdos:</strong> imagine buscar livros por etiquetas antes de abrir suas páginas. O Loki identifica fluxos pelos metadados e consulta o conteúdo dos blocos relevantes. Isso é diferente da indexação do texto completo apresentada na comparação com ELK.</p>
<p><strong>Tecnicamente:</strong> um <em>log stream</em> reúne entradas com exatamente o mesmo conjunto de labels. As entradas são agrupadas em <em>chunks</em>, comprimidas e armazenadas. Agentes coletam os logs, acrescentam labels e enviam os dados ao Loki. A aula cita Promtail e Alloy; este guia não valida o ciclo de suporte atual desses componentes.</p>
''' + ref(4,'5–6') + code('{app="api", env="production"} |= "error"','Transcrição literal — POSTECH - Monitoramento Opensource - Aula 4.pdf, p. 6.','O seletor entre chaves escolhe os fluxos com <code>app="api"</code> e <code>env="production"</code>. O operador <code>|=</code> mantém as linhas que contêm o texto <code>error</code>. Esta é uma consulta LogQL, não um comando de terminal. Os labels são os do exemplo da aula; não foram verificados no projeto.') + '''
<h4>Dois caminhos de dados</h4>''' + table(['Caminho','Componentes','Função'],[
    ('Escrita','Agente → Distributor → Ingester → armazenamento','Distributor recebe e valida; Ingester monta chunks e os persiste.'),
    ('Leitura','Grafana/cliente → Query Frontend → Querier','Frontend pode dividir/cachear consultas; Querier busca dados recentes e persistidos.'),
    ('Índice','Labels dos fluxos','Ajuda a localizar chunks relevantes antes da filtragem das linhas.')
]) + ref(4,'7–8') + '''
<p>O Distributor é descrito como sem estado; o Ingester mantém estado. A aula explica a possibilidade de implantações simples ou distribuídas a partir do mesmo binário e descreve coleta de logs no Kubernetes com um agente por nó. A forma de implantação real precisa ser escolhida e configurada no projeto.</p>
<p>Na investigação integrada, um pico de erro nas métricas leva aos logs daquele período e serviço; um trace relacionado detalha a requisição. A aula exemplifica essa correlação com Prometheus, Loki e Tempo. Na Fase 4, o APM escolhido deve cumprir os requisitos de trace e Service Map.</p>
''' + ref(4,'8–9') + bs('SUG-03','REQ-OBR-26') + complement('''<p><strong>Como estudar sem criar um falso requisito:</strong> padronizar nomes de serviço, ambiente e intervalo de tempo facilita cruzar sinais. O identificador de trace pode ajudar a conectar registros à requisição, mas não deve virar automaticamente um label indexado de alta cardinalidade. O esquema final é decisão técnica, não uma exigência adicional da FIAP.</p>''') + '''
<aside class="note"><strong>OS-Q01 · [INCERTO] no original</strong>O Hands On da p. 4 fala em instalar Zabbix e configurar itens/triggers. O conteúdo das p. 5–11 é sobre Loki. O guia mantém a identificação do módulo pelo conteúdo e não trata aquele parágrafo como roteiro de instalação do Loki.</aside>
<p><strong>Para memorizar:</strong> o Loki indexa labels de fluxos; isso não impede pesquisar texto nas linhas. Selecionar os fluxos e o período adequados reduz o universo da busca.</p>'''))

content += section('aula-5','Aula 5 — Tracing com Jaeger', card(5,'Enxergar o caminho e o tempo da requisição', '''
<p><strong>Em miúdos:</strong> a analogia da aula é o rastreamento de encomendas: acompanhar por onde uma requisição passou e quanto tempo gastou em cada etapa. No exemplo de checkout, a aula mostra 2,5 segundos totais e 2,2 segundos na validação de cartão; é um cenário ilustrativo, não um resultado medido neste projeto.</p>
''' + ref(5,'5–6') + table(['Conceito','Explicação técnica','O que observar'],[
    ('Trace','Jornada de uma requisição com identificador compartilhado.','Operações relacionadas pertencem ao mesmo trace.'),
    ('Span','Unidade de trabalho com nome, início, fim e metadados.','Uma chamada HTTP, consulta ao banco ou operação de fila.'),
    ('Pai e filho','Relação entre operações encadeadas.','Permite visualizar a hierarquia e a cascata temporal.'),
    ('Atributo','Par chave-valor que descreve a operação.','Método HTTP, status e URL são exemplos do material.'),
    ('Propagação de contexto','Transporte de identificadores entre serviços.','Cabeçalhos HTTP ou metadados de mensagens conectam os spans.'),
    ('Sampling','Seleção de traces para controlar volume.','Equilibrar investigação, custo e armazenamento.')
]) + ref(5,'7–10') + '''
<h4>Coletar, persistir e consultar</h4><p>O texto descreve Jaeger v2 construído sobre o framework do OTel Collector. O papel <strong>collector</strong> recebe e processa spans; <strong>query</strong> atende APIs e interface; <strong>ingester</strong> lê do Kafka quando existe esse intermediário. A arquitetura pode escrever diretamente no armazenamento ou usar Kafka entre recepção e persistência. As extensões de storage/query e o storage exporter separam responsabilidades.</p>
''' + ref(5,'8–9') + '''
<h4>Instrumentação que ajuda a investigação</h4><p>A aula recomenda começar nas entradas e operações críticas, aproveitar instrumentação automática, dar nomes consistentes aos spans, planejar retenção, agrupar envio em lotes e tratar dados sensíveis. Nomes descritivos aparecem literalmente como <code>GET /api/users/{id}</code> e <code>database.query.users.select</code>; são exemplos de nomenclatura, não comandos executáveis.</p>
''' + ref(5,'10–11') + bs('REQ-OBR-13','REQ-OBR-14','REQ-OBR-15','REQ-BON-02') + complement('''<p><strong>Aplicação ao desafio:</strong> use essa base para explicar o trace originado no <code>evaluation-service</code> e as dependências entre os cinco serviços. O enunciado exige demonstrá-los no Datadog ou New Relic. Jaeger ensina o mecanismo, mas não substitui a escolha obrigatória do APM.</p><p><strong>Limite da conclusão:</strong> um span demorado localiza uma etapa importante da investigação, mas não prova sozinho a causa raiz. Consulte os logs e o contexto da operação. O mapa de serviços também precisa de tráfego e instrumentação coerente; instalar o backend não garante sua completude.</p>''') + '''
<aside class="note"><strong>Ressalvas do original</strong>OS-Q01: p. 4 e abertura da p. 5 trazem texto sobre Zabbix. OS-Q03: p. 8 anuncia cinco papéis, mas o trecho descreve três; não completamos os dois ausentes por suposição. OS-Q05: a promessa de capturar sempre erros/alta latência depende da política de amostragem e não está demonstrada no PDF.</aside>
<p><strong>Para memorizar:</strong> sem propagação de contexto, spans de serviços diferentes podem aparecer como jornadas separadas. O principal valor do trace é a relação entre operações, além da duração isolada.</p>'''))

content += section('aula-6','Aula 6 — OpenTelemetry e Grafana Alloy', card(6,'Padronizar a telemetria e centralizar o encaminhamento', bs('REQ-OBR-11','REQ-OBR-13','REQ-BON-01','REQ-BON-02') + '''
<p><strong>Em miúdos:</strong> OpenTelemetry oferece uma linguagem comum para produzir os sinais. O Collector recebe esses sinais e os encaminha aos destinos. Alloy é uma distribuição desse coletor, com integrações do ecossistema Grafana.</p><p><strong>Tecnicamente:</strong> a API define operações de instrumentação; o SDK implementa e configura processamento/exportação. Um exporter envia dados a um destino. O Collector pode atuar próximo das aplicações como agente ou como gateway. Esse desacoplamento permite administrar o encaminhamento sem repetir toda a instrumentação ao trocar o backend.</p>
''' + ref(6,'5–7') + table(['Etapa','O que acontece','Exemplo descrito pela aula'],[
    ('Instrumentação','A aplicação gera sinais usando APIs/SDKs.','Manual para contexto específico; automática onde houver suporte.'),
    ('Receiver','Recebe dados de fontes e protocolos.','OTLP, Prometheus e Jaeger aparecem no texto.'),
    ('Processor','Transforma ou seleciona dados.','Filtrar dados sensíveis, adicionar atributos e amostrar traces.'),
    ('Exporter','Encaminha ao destino compatível.','Loki para logs; Prometheus/Mimir para métricas; Tempo para traces.'),
    ('Backend','Armazena e disponibiliza os sinais para análise.','Destinos separados por sinal; Grafana consulta as fontes.')
]) + ref(6,'8–9') + '''
<h4>O pipeline deve respeitar o tipo de sinal</h4><div class="diagram" aria-label="Pipeline didático por sinal"><div class="node">Aplicações<br><small>API + SDK OTel</small></div><span aria-hidden="true">→</span><div class="node">Collector ou Alloy<br><small>receber → processar → exportar</small></div><span aria-hidden="true">→</span><div class="node">Backends<br><small>métricas / logs / traces</small></div></div>
<p>O material ilustra pipelines distintos para os três sinais. A função central de receber, processar e exportar é obrigatória no desafio; usar Alloy em lugar do Collector padrão é opcional. A lista de backends de uma aula não altera as escolhas impostas pelo enunciado.</p>
''' + ref(6,'8–9') + '''
<h4>Volume, custo e dados sensíveis</h4><p>As p. 10–11 recomendam começar com transações críticas, aproveitar instrumentação automática e acrescentar detalhes de negócio manualmente. Também pedem controlar cardinalidade, definir amostragem, acompanhar volume e remover/mascarar tokens, senhas e informações pessoais antes da exportação.</p>
''' + ref(6,'10–11') + complement('''<p><strong>Como explicar a arquitetura da entrega:</strong> para cada sinal, identifique a origem, o receptor, o processamento e o destino que realmente recebeu os dados. Depois mostre a consulta correspondente. Uma seta no desenho não comprova conectividade ou aceitação do protocolo.</p><p><strong>Sampling:</strong> a distinção útil é o momento da decisão: head-based ocorre no início; tail-based usa informações do trace coletado. Percentual fixo é uma estratégia possível, não a definição completa de head-based. Não prometa captura de todos os erros sem verificar a política e as perdas do pipeline.</p>''') + bs('REQ-OBR-26','REQ-OBR-39') + '''
<aside class="note"><strong>OS-Q02 · [INCERTO] no original</strong>O Hands On da p. 4 menciona hosts, itens e triggers ao falar de OTel/Alloy. O corpo das p. 5–11 define APIs, SDKs e pipelines. O procedimento prático precisa ser consultado no material de vídeo que não foi fornecido.</aside>
<p><strong>Para memorizar:</strong> OTel não é a tela final de análise; Collector não é sinônimo de armazenamento; Alloy é uma opção de distribuição. Gerar dados, transportá-los e consultá-los são etapas distintas.</p>'''))

content += section('aula-7','Aula 7 — Kubernetes: entender onde a stack roda', card(7,'Do estado desejado aos contêineres em execução', bs('REQ-OBR-01','REQ-OBR-02','REQ-OBR-05','REQ-OBR-06') + '''
<p><strong>Em miúdos:</strong> Kubernetes organiza a execução das aplicações e tenta manter a quantidade e a configuração desejadas. A aula compara o ambiente a um porto: contêineres padronizados precisam de coordenação, distribuição de trabalho e reposição em caso de falha.</p><p>Embora o título seja observabilidade, esta primeira parte revisa a base de orquestração. Isso prepara a leitura da próxima aula e ajuda a localizar os recursos que a stack deverá observar.</p>
''' + ref(7,'3–6') + table(['Objeto ou componente','Responsabilidade','Relação com o monitoramento'],[
    ('Pod','Unidade de implantação com um ou mais contêineres.','Origem de logs e métricas; pode ter contêiner auxiliar.'),
    ('Service','Acesso de rede estável a um conjunto de Pods.','Ajuda a pensar em identidade do serviço apesar da troca de Pods.'),
    ('Deployment','Descreve e gerencia réplicas e atualizações.','Mudanças e réplicas influenciam a observação da aplicação.'),
    ('Node','Máquina de trabalho do cluster.','Separa consumo da infraestrutura e da aplicação.'),
    ('API Server / etcd','Entrada da API de controle / persistência do estado.','Guarda e publica o estado utilizado pelos componentes de controle.'),
    ('Scheduler / controllers','Escolha de nós / reconciliação de estado.','Explicam movimentações e substituições de Pods.'),
    ('kubelet / runtime','Coordenação local / execução de contêineres.','Executam e reportam o estado no nó.'),
    ('kubectl','CLI de interação com a API.','Inspeciona e gerencia recursos; o PDF não fornece comandos completos.')
]) + ref(7,'7–10') + '''
<h4>Reconciliação é um ciclo</h4><ol class="flow"><li><div><strong>Declarar</strong><span>Manifestos expressam o estado desejado.</span></div></li><li><div><strong>Observar</strong><span>API e componentes registram/acompanham objetos e estado atual.</span></div></li><li><div><strong>Agendar e executar</strong><span>O Scheduler atribui Pods a nós; o kubelet coordena sua execução.</span></div></li><li><div><strong>Reconciliar</strong><span>Controladores procuram reduzir a diferença entre estado desejado e atual.</span></div></li></ol>
''' + ref(7,'8–10') + complement('''<p><strong>Relação com o Self-Healing exigido:</strong> a reconciliação nativa do Kubernetes ajuda a manter workloads, mas o desafio também exige uma automação que reaja ao alerta e tente mitigar um incidente. Para demonstrar REQ-OBR-19, registre esse acionamento explícito e a ação; não use apenas a recriação normal de um Pod como substituta.</p><p><strong>Leitura cuidadosa:</strong> a descrição de comunicação via API Server está no contexto do plano de controle. Não a generalize para todo tráfego entre aplicações. Escalonamento, recuperação e atualização sem indisponibilidade dependem de configuração e condições reais; não são garantias incondicionais do simples uso de Kubernetes.</p>''') + bs('REQ-OBR-19') + '''<p><strong>Para memorizar:</strong> Pod executa a carga; Service oferece acesso; Deployment gerencia o estado da carga; Node fornece capacidade. A observabilidade precisa relacionar essas camadas.</p>'''))

content += section('aula-8','Aula 8 — Integrar a observabilidade no Kubernetes', card(8,'Correlacionar sinais de uma mesma jornada', bs('REQ-OBR-06','REQ-OBR-07','REQ-OBR-08','REQ-OBR-09','REQ-OBR-11') + '''
<p><strong>Em miúdos:</strong> uma compra atravessa autenticação, estoque, pagamento e notificação. Se falhar, você precisa saber se o problema atingiu muitas requisições, qual evento ocorreu e em qual etapa da jornada. A aula usa esse cenário para reunir métricas, logs e traces.</p>
''' + ref(8,9) + '''
<p><strong>Tecnicamente:</strong> a arquitetura combina coleta dinâmica no cluster, agentes para logs, instrumentação OTel para traces e Grafana conectado aos backends. O texto apresenta Zabbix na base de infraestrutura e Alloy como coletor unificado. Service Discovery aparece para descobrir novos alvos do Prometheus; isso é relevante porque Pods podem ser criados e removidos.</p>
''' + ref(8,'5–9') + '''
<h4>A correlação precisa ser planejada</h4><p>A aula recomenda labels consistentes, citando <code>app</code>, <code>namespace</code> e <code>env</code>; propagação de contexto entre serviços; dashboards organizados por serviço ou jornada; e provisionamento de dashboards/alertas como código. Também recomenda escolher indicadores ligados à experiência do usuário e controlar cardinalidade.</p>
''' + ref(8,10) + bs('SUG-03','REQ-OBR-20') + complement('''<p><strong>Roteiro de investigação para o ToggleMaster:</strong> abra a visão do serviço e do intervalo afetado, confirme a degradação nas métricas, encontre logs da mesma janela e serviço e selecione o trace da requisição de teste. Explique qual evidência cada sinal acrescenta. Esse roteiro é uma proposta didática; os dados e os nomes precisam corresponder à implementação real.</p>''') + '''
<p><strong>Para memorizar:</strong> ferramentas instaladas lado a lado ainda precisam de identificadores, contexto, roteamento e consultas coerentes. O ganho vem de ligar os sinais a uma pergunta operacional.</p>'''))

content += section('aplicacao','Da aula à demonstração: o que verificar', complement('''
<p>A sequência abaixo organiza o estudo da implementação e das evidências. Não afirma que algo já esteja implantado. O requisito vem do enunciado; esta ordem de verificação é autoral.</p>
<ol class="flow"><li><div><strong>Base funcional</strong><span>Os cinco serviços e o cluster continuam funcionando. Identifique namespaces, workloads e caminho da requisição.</span></div></li><li><div><strong>Stack pelo repositório</strong><span>Localize os Helm charts e a configuração do Collector no IaC/GitOps. Código deve corresponder ao ambiente demonstrado.</span></div></li><li><div><strong>Dados chegando</strong><span>Gere tráfego de teste e confirme séries, logs e trace nos destinos previstos. Diferencie problema de coleta de ausência real de atividade.</span></div></li><li><div><strong>Visualização e explicação</strong><span>Mostre recursos do cluster, taxa de requisições e logs; explique origem, processamento e destino do OTel.</span></div></li><li><div><strong>Alerta e resposta</strong><span>O módulo de automação completa a cadeia até incidente, ChatOps e ação corretiva. Capture o antes, o disparo e a execução.</span></div></li><li><div><strong>Evidências</strong><span>Prepare o print do dashboard e a explicação da arquitetura OTel; use o APM escolhido para os prints e a demonstração de trace/Service Map.</span></div></li></ol>
''') + bs('SUG-01','REQ-OBR-20','REQ-OBR-23','REQ-OBR-26','REQ-OBR-35','REQ-OBR-39') + table(['Erro ou confusão','Como evitar','Base'],[
    ('Tratar toda ferramenta da disciplina como obrigatória.','Consultar a matriz: Zabbix e Jaeger são estudo; Prometheus/Loki/Grafana são exigidos.','Enunciado, p. 3–4; Aulas 1, 5 e 8.'),
    ('Usar todos os identificadores como labels.','Planejar dimensões e cardinalidade.','Aula 2, p. 9; Aula 6, p. 10; Aula 8, p. 10.'),
    ('Confundir tela com armazenamento.','Identificar qual backend responde a cada consulta.','Aula 3, p. 5–6.'),
    ('Presumir trace contínuo só porque há SDK.','Verificar propagação de contexto e relações entre spans.','Aula 5, p. 7–8; Aula 8, p. 10.'),
    ('Prometer amostragem sem perdas.','Documentar a política e o limite da evidência coletada.','Aula 5, p. 10; Aula 6, p. 10; ressalva OS-Q05.'),
    ('Tomar ilustração por ambiente em execução.','Capturar evidências do próprio cenário de teste.','Enunciado, p. 5–6; figuras das aulas com auxílio de IA.')
]))

content += section('outros-modulos','Como este módulo se conecta aos outros', table(['Módulo','Conexão de estudo'],[
    ('Welcome to Observabilidade e Monitoramento','Situa o problema e a integração entre fases; consulte o enunciado para os critérios efetivos.'),
    ('Observabilidade e Monitoramento','Fornece o raciocínio para escolher sinais, indicadores e alertas; aqui esse raciocínio ganha ferramentas.'),
    ('APM','Aprofunda instrumentação e análise de requisições; no desafio Datadog ou New Relic deve exibir trace e mapa de serviços.'),
    ('Automação de incidentes','Recebe o alerta e organiza incidente, comunicação e tentativa automática de mitigação.')
]) + complement('<p>Este é um mapa didático entre módulos. As conexões não transformam recomendações de aula em critérios adicionais de avaliação. Para navegar pelos cinco guias, use o índice no README de requisitos.</p>'))

content += section('revisao','Revisão rápida e autoavaliação', '''
<p>Explique cada resposta com suas palavras antes de abrir o comentário. As perguntas são autorais para estudo, baseadas nas páginas indicadas; não são previsão de prova.</p>
<details><summary>1. No Zabbix, qual a diferença entre item, trigger e action?</summary><p>Item é a métrica coletada; trigger avalia a condição de problema; action define a resposta a um evento. Aula 1, p. 6.</p></details>
<details><summary>2. Quem inicia a coleta no modelo pull do Prometheus?</summary><p>O Prometheus busca os dados nos targets. Bibliotecas e exporters expõem métricas; o Pushgateway atende o caso específico de jobs de curta duração apresentado na aula. Aula 2, p. 6.</p></details>
<details><summary>3. Range query e range vector são sinônimos?</summary><p>Não. Range query é a avaliação repetida no tempo; range vector é um tipo de dado da linguagem que contém uma janela de amostras por série. Aula 2, p. 7–8.</p></details>
<details><summary>4. Se o Grafana abre, isso prova que as métricas chegaram?</summary><p>Não. É necessário consultar a fonte e ver dados do período/serviço esperado. A aula separa fonte, consulta e painel; o enunciado exige funcionamento prático. Aula 3, p. 5–6; enunciado, p. 5.</p></details>
<details><summary>5. O Loki consegue procurar a palavra error sem indexar todo o texto?</summary><p>Sim. O seletor identifica fluxos pelos labels, e o filtro de linha examina o conteúdo relevante. O exemplo exato está na ficha da Aula 4, p. 6.</p></details>
<details><summary>6. Por que uma requisição pode aparecer em traces separados?</summary><p>Uma hipótese a investigar é a propagação de contexto incompleta entre serviços; IDs compartilhados ligam spans de uma mesma jornada. A resposta é uma hipótese didática, não diagnóstico do projeto. Aula 5, p. 7–8.</p></details>
<details><summary>7. O que distingue SDK, Collector e backend?</summary><p>O SDK implementa a API de instrumentação e configura geração/processamento/exportação; o Collector recebe, processa e encaminha; o backend guarda e permite analisar os sinais. Aula 6, p. 6–9.</p></details>
<details><summary>8. É obrigatório escolher Alloy e Jaeger na Fase 4?</summary><p>Alloy é alternativa opcional ao Collector padrão; Jaeger não é a alternativa de APM prevista. O enunciado exige Datadog ou New Relic. REQ-BON-01 e REQ-OBR-12, enunciado, p. 4.</p></details>
<details><summary>9. O Kubernetes recriar um Pod já demonstra toda a automação exigida?</summary><p>Não. A reconciliação é explicada na Aula 7, p. 8–10. O desafio também exige reação automática ao alerta, integração de incidente e evidência da ação corretiva; veja REQ-OBR-19 e REQ-OBR-31.</p></details>
<details><summary>10. Como relacionar uma métrica a logs e traces?</summary><p>Use serviço e intervalo coerentes, labels padronizados e propagação de contexto. O identificador de trace pode aprofundar a relação; a escolha de esquema é técnica. Aula 8, p. 9–10; SUG-03.</p></details>
''')

content += section('limites','Fidelidade, fontes e pontos a confirmar', '''
<p>Leitura integral concluída em 2026-09-16. As páginas de mercado, referências e palavras-chave das oito aulas foram incluídas na leitura. Os links externos citados nas apostilas não foram acessados; não são conteúdo adicional presumido.</p>
''' + table(['ID','O que o original apresenta','Tratamento adotado'],[
    ('OS-Q01 · [INCERTO]','Aulas 4 e 5, p. 4: Hands On de Zabbix; Aula 5, p. 5: abertura sobre Zabbix.','Registrar inconsistência editorial; estudar Loki/Jaeger pelo corpo específico e confirmar roteiro prático com tutor/vídeo.'),
    ('OS-Q02 · [INCERTO]','Aula 6, p. 4: hosts, itens e triggers no roteiro OTel/Alloy.','Não converter essa descrição em comandos ou configuração.'),
    ('OS-Q03 · [INCERTO]','Aula 5, p. 8: cinco papéis anunciados e três descritos; figura da p. 9 com agentes/clientes e texto v2.','Preservar os papéis efetivamente descritos; não reconstruir uma implantação por uma figura genérica.'),
    ('OS-Q04 · [INCERTO]','Aula 7, p. 8–9: Docker citado como runtime e comunicação via API descrita de forma ampla.','Limitar a síntese ao plano de controle; versão e integração de runtime não estão especificadas.'),
    ('OS-Q05 · [INCERTO]','Aula 5, p. 10: garantia ampla sobre sampling; Aula 6, p. 10: head-based simplificado.','Explicação complementar separa momento da decisão e política; não promete captura integral.'),
    ('OS-L01 · Limitação','As oito p. 4 remetem às videoaulas; scripts/YAML citados não foram fornecidos.','Não criar comandos de instalação. A consulta LogQL foi transcrita exatamente da Aula 4, p. 6.'),
    ('OS-L02 · Limitação','Figuras de arquitetura e interfaces creditadas como produzidas com auxílio de IA.','Usar apenas como apoio conceitual; não inferir sintaxe, protocolos, configuração ou execução pelos desenhos.'),
    ('OS-L03 · Limitação','Cases e ganhos quantitativos narrados pelas aulas.','Não validar nem transferir os percentuais para o ToggleMaster; consultar as referências originais antes de usá-los como evidência externa.')
]) + '''
<p>As referências de mercado incluem monitoramento no varejo e serviços públicos (Aula 1, p. 11), anomalias e usos de Prometheus (Aula 2, p. 10), LATAM e perfis no Grafana (Aula 3, p. 9), escala de logs no Loki (Aula 4, p. 10), tracing distribuído (Aula 5, p. 12), tendências OTel/Alloy (Aula 6, p. 12), adoção do Kubernetes (Aula 7, p. 11) e observabilidade integrada (Aula 8, p. 11). São trilhas de aprofundamento indicadas pelo material, sem verificação externa nesta tarefa.</p>
<p>Não foram identificadas páginas definitivamente ilegíveis. A primeira extração em modo layout omitiu o corpo de texto; uma segunda extração com PDFium recuperou o conteúdo completo, seguida de inspeção visual das figuras, tabelas e consulta. Nenhum original foi alterado.</p>
''')

connections=[
    ('REQ-OBR-01','Aula 7 revisa a base Kubernetes que precisa continuar funcionando; não comprova as fases anteriores.'),
    ('REQ-OBR-02','Aula 7 explica Pods/contêineres; conferir os cinco microsserviços reais na base mantida.'),
    ('REQ-OBR-05','Aulas 7–8 situam a stack no cluster; as opções de GitOps e a dúvida EKS/ArgoCD permanecem no README.'),
    ('REQ-OBR-06','Aula 8, p. 10, recomenda configuração como código; o requisito específico de Helm/GitOps vem do enunciado.'),
    ('REQ-OBR-07','Aula 2 explica coleta, séries temporais e PromQL para métricas de infraestrutura.'),
    ('REQ-OBR-08','Aula 4 explica centralização dos logs e consulta; é preciso verificar cobertura de todos os contêineres.'),
    ('REQ-OBR-09','Aula 3 ensina os componentes da visualização principal no Grafana.'),
    ('REQ-OBR-10','Aulas 2–4 e 8 sustentam painéis de recursos, requisições e logs em tempo real.'),
    ('REQ-OBR-11','Aula 6 detalha instrumentação e pipelines de recepção, processamento e exportação de cada sinal.'),
    ('REQ-OBR-12','O estudo de tracing usa Jaeger, mas a entrega deve escolher Datadog ou New Relic conforme o enunciado.'),
    ('REQ-OBR-13','Aulas 5–6 explicam instrumentação; alterações de código/Dockerfile deverão ser implementadas e verificadas.'),
    ('REQ-OBR-14','Trace, span e propagação de contexto ajudam a demonstrar a requisição do evaluation-service no APM.'),
    ('REQ-OBR-15','Relações entre spans e serviços dão base para interpretar o Service Map dos cinco serviços no APM.'),
    ('REQ-OBR-16','Aula 3 explica alertas por consulta; configuração inteligente e condições reais precisam ser definidas.'),
    ('REQ-OBR-19','Aula 7 ajuda a distinguir autorrecuperação nativa de automação que reage explicitamente ao alerta.'),
    ('REQ-OBR-20','Aulas 6 e 8 apoiam a documentação da stack e do Collector no repositório IaC/GitOps.'),
    ('REQ-OBR-23','O roteiro de verificação separa instalação/configuração de dados e funcionamento demonstrados.'),
    ('REQ-OBR-26','Grafana, LogQL e pipelines OTel permitem explicar os pontos exigidos no vídeo.'),
    ('REQ-OBR-31','A distinção entre reconciliação e ação corretiva orienta a evidência de Self-Healing acionado pelo alerta.'),
    ('REQ-OBR-35','Aula 3 orienta leitura do dashboard cujo print deve constar no relatório.'),
    ('REQ-OBR-39','Aula 6 oferece o vocabulário para explicar a arquitetura OTel realmente implementada.'),
    ('REQ-BON-01','Alloy é a distribuição estudada na Aula 6 e opção do enunciado, sem pontuação extra definida.'),
    ('REQ-BON-02','APIs/SDKs OTel nas Aulas 5–6 ajudam a atender a preferência de instrumentação do PDF.'),
    ('SUG-01','Roteiro autoral liga cada demonstração e print à evidência do requisito.'),
    ('SUG-02','Triggers com duração/histerese e alertas por consulta ajudam a discutir ruído e ação útil.'),
    ('SUG-03','Labels consistentes, nomes de serviços e contexto permitem correlacionar logs, métricas e traces.')
]

if __name__ == '__main__':
    write_guide('02.Monitoramento Opensource','Monitoramento Opensource','Oito aulas para compreender métricas, logs, traces e a integração da stack no Kubernetes.',content,connections)
