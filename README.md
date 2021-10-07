# Variety Webscraping 
## Este script extrai do site "https://sistemas.agricultura.gov.br/snpc/cultivarweb/cultivares_registradas.php" os links das "sementes" ativas alteradas genéticamente, nomeadas de cultivares (varietys, em inglês) e logo após, extrai as informações de cada link as salvando em um .json

### Para executar o script, basta executar o script run.sh que fará os seguintes comandos:
Traz a imagem do dockerhub.
```
docker pull abbadb/ubuntu_infra:latest
``` 
Roda o container extraindo os links com as cultivares ativas em um .csv
```
docker run -v $(pwd):/app -e USE_PROXY=False abbadb/ubuntu_infra python3 /app/variety-links-scraping.py
```
No caso acima, está configurada para a não utilização de um proxy, mas caso desejada deve ser alterado para a seguinte forma:
```
docker run -v $(pwd):/app -e USE_PROXY=True PROXY_USER= PROXY_PASS= PROXY_IP= PROXY_PORT= abbadb/ubuntu_infra python3 /app/variety-links-scraping.py
```
Tendo adicionado nas variaveis seguintes a USE_PROXY os valores desejados.

A segunda parte, atribui o csv gerado, podendo ser alterado manualmente no run.sh e executa o código que extrai as informações de cada link, trazendo elas em um .json na pasta files, criada no mesmo diretório, neste caso também configurado para a não utilização de proxy, podendo ser alterado seguindo o mesmo exemplo do caso acima.
```
csvfile=$(ls link*.csv | head -n1)
docker run -v $(pwd):/app -e USE_PROXY=False abbadb/ubuntu_infra python3 /app/variety-scraping.py -i /app/$csvfile
```

## Como existem diversas cultivares ativas (algo em torno de 30000) é possível cancelar manualmente quando houver interesse e executar manualmente a segunda parte do código para fins de teste, porém a execução completa dos dois códigos leva em torno de 15 horas.

Repositório da imagem utilizada: https://hub.docker.com/repository/docker/abbadb/ubuntu_infra