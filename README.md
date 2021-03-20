# Web scrapper Airbnb
Web scrapper realizado en scrapy para obtener información de las habitaciones en el sitio web de airbnb
## Instalacion
Realizar la instalacion de scrapy
```
pip install scrapy
```
## Instrucciones
Los siguientes comandos se ejecutan en **roomsScrapy/roomsScrapy**
El siguiente web scraper realiza la busqueda a partir de 4 ciudades (Bogotá,Santa Marta,Cartagena,San Andres) para la fecha 2021-06-14 a 2021-06-18 para 2 adultos se ejecuta el spider con el siguiente comando
```
scrapy crawl rooms
```
La salida esta dada en el archivo items.csv

Para especificar una fecha especifica de viaje a partir del siguiente comando, las fechas se especifican en formato iso 8601.La opción sday permite seleccionar un solo día de estadía sin la necesidad de colocar una fecha de checkout
```
scrapy crawl rooms2 -a checkin=date_checkin -a checkout=date_checkout [-a sday=[True|False]]
```
