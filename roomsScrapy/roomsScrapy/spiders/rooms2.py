import scrapy
import pathlib

class RoomsSpider(scrapy.Spider):
    name = 'rooms2'

    allowed_domains = [
        'airbnb.com.co'
        ]
    custom_settings = {'FEEDS' : {
            pathlib.Path(f'items2.csv'):{
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True
            }
        },
    }
    def start_requests(self):
        adults = getattr(self,'adults',None)

        yield scrapy.Request(f'https://www.airbnb.com.co/s/Cartagena-~-Bol%C3%ADvar--Colombia/homes?place_id=ChIJUROdrucl9o4RyiY_Ay45YbE&checkin={self.checkin}&checkout={self.checkout}&adults={adults or 2}',
                            callback=self.parse)
        
        yield scrapy.Request(f'https://www.airbnb.com.co/s/San-Agust%C3%ADn/homes?search_type=filter_change&place_id=ChIJhbXvmZ5wJY4RVAkxc3nRggk&checkin={self.checkin}&checkout={self.checkout}&adults={adults or 2}',
                            callback=self.parse)

        yield scrapy.Request(f'https://www.airbnb.com.co/s/San-Andres--Colombia/homes?tab_id=home_tab&place_id=ChIJabPa3gamBY8RiYudmvoZ3yc&checkin={self.checkin}&checkout={self.checkout}&adults={adults or 2}',
                            callback=self.parse)

    def parse(self, response):

        rooms = response.xpath('//div[@class="_8ssblpx"]')
        ciudad = response.xpath('//div[@class="_rrw786"]//h1[@class="_14i3z6h"]/text()').re(r'en\s(.+)')
        for room in rooms:

            title = room.xpath('.//div[@class="_r6zroz"]//div[@class="_bzh5lkq"]/text()').get()
            url = "https://www.airbnb.com.co" + room.xpath('.//div[@class="_8s3ctt"]/a/@href').get()
            calificacion = room.xpath('.//div[@class="_1bbeetd"]//span[@class="_18khxk1"]/@aria-label').re(r'\s(\d+\.\d+).*;\s(\d+)')
            reference = room.xpath('.//div[@class="_1tanv1h"]/div[@class="_b14dlit"]/text()').get()
            precio = int(room.xpath('.//div[@class="_ls0e43"]//span[@class="_olc9rf0"]/text()').re(r'^\$(\d+,\d+)')[0].replace(',',''))
            contains = room.xpath('.//div[@class="_8s3ctt"]//div[@class="_kqh46o"]/text()').getall()

            yield dict( title = title,
                        checkin = self.checkin,
                        checkout = self.checkout,
                        reference = reference,
                        url = url,
                        calificacion = calificacion,
                        precio = precio,
                        contains = contains,
                        ciudad=ciudad)
        
        next_link = response.xpath('//a[@aria-label="Siguiente" and @class="_za9j7e"]/@href').get()
        if next_link:
            yield response.follow('https://www.airbnb.com.co'+next_link, callback= self.parse)