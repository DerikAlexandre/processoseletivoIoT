# Processo Seletivo – Intensivo Maker | IoT
# Monitor de Estoque Kanban Inteligente

## Identificação do Candidato

**Nome completo:** Derik Alexandre Alves de Andrade
**GitHub:** DerikAlexandre

## Visão Geral da Solução

O projeto tem como objetivo monitorar o peso de uma caixa de peças usando um ESP32 e o sensor HX711.

O sistema verifica o peso da caixa e informa pela comunicação serial se o estoque está normal, se a caixa está vazia, se foi reabastecida ou se aconteceu algum erro na leitura do sensor.

## Arquitetura do Sistema Embarcado

O programa começa configurando os pinos usados pelo HX711 e depois entra em um loop de leitura do sensor.

A lógica usada foi:

Se o peso for 0g, o sistema considera que a caixa pode ter sido removida ou que houve algum problema no sensor.
Se o peso chegar a 150g ou menos, é gerado um aviso de reposição.
Se o peso estiver acima desse limite, o estoque continua sendo considerado normal.
Depois de uma situação de caixa vazia, se o peso voltar para aproximadamente 5000g, o sistema entende que houve reabastecimento.

Também foi usada uma variável para guardar se existe uma reposição pendente. Isso evita que o sistema mostre a mensagem de caixa reabastecida logo no início, quando ela já começa cheia.

## Componentes Utilizados na Simulação

ESP32 DevKit C v4
Sensor de peso HX711
Comunicação Serial

O ESP32 executa o programa e faz a leitura do HX711. O sensor representa o peso da caixa e a comunicação serial é usada para mostrar os estados e alertas do sistema.

## Decisões Técnicas Relevantes

O código foi mantido simples, separando a leitura do HX711 da parte que verifica o estado do estoque.

Foram usadas constantes para os limites de caixa vazia e caixa cheia, facilitando alterações caso os valores precisem ser ajustados.

Também foi evitado o uso de esperas longas no loop principal, já que os testes do Wokwi mudam os valores do sensor durante a execução.

As mensagens da Serial foram mantidas exatamente como estão descritas nos testes automáticos.

## Resultados Obtidos

O sistema consegue identificar os difernetes casos pedidos no desafio.

Quando o peso fica em 2500g:

`Status: Estoque Regular (2500g)`

Quando o peso cai para 150g:

`Evento de reposição disparado! Caixa vazia detectada.`

Quando a caixa é abastecida novamente e volta para 5000g:

`Abastecimento concluído. Caixa cheia.`

Se a leitura chegar a 0g:

`ALERTA: Caixa ausente ou erro de calibração no sensor HX711!`

O funcionamento final do projeto é validado pelos testes automáticos do Wokwi através do GitHub Actions.

## Comentários Adicionais
## Comentários Adicionais

Uma das dificuldades durante o desenvolvimento foi a configuração do ambiente para gerar o arquivo `fs.bin`. Foi necessário utilizar o Docker para preparar o ambiente e gerar o arquivo usado na simulação.

Também houve uma dificuldade inicial para entender como o `diagram.json` funciona e como os componentes e pinos precisam ser configurados para que o Wokwi consiga interagir corretamente com o projeto.

No final, o projeto ajudou a entender melhor a integração entre o código em MicroPython, a montagem virtual do circuito no Wokwi e os testes automáticos executados pelo GitHub Actions.