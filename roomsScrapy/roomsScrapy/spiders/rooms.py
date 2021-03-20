import scrapy
import pathlib

class RoomsSpider(scrapy.Spider):
    name = 'rooms'
    start_urls = [
        'https://www.airbnb.com.co/s/Bogota-~-Bogot%C3%A1--Colombie/homes?flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=march&adults=2&source=structured_search_input_header&search_type=autocomplete_click&tab_id=home_tab&checkin=2021-06-14&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&flexible_trip_lengths%5B%5D=weekend_trip&checkout=2021-06-18&query=Bogota%20-%20Bogot%C3%A1%2C%20Colombie&place_id=ChIJKcumLf2bP44RFDmjIFVjnSM',
        'https://www.airbnb.com.co/s/Santa-Marta-~-Magdalena--Colombia/homes?flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=march&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&query=Santa%20Marta%20-%20Magdalena%2C%20Colombia&place_id=ChIJPRea9W_29I4RuPk6FfyVSxI&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&checkin=2021-06-14&checkout=2021-06-18&adults=2&source=structured_search_input_header&search_type=autocomplete_click',
        'https://www.airbnb.com.co/s/Cartagena-~-Bol%C3%ADvar--Colombia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=march&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&place_id=ChIJUROdrucl9o4RyiY_Ay45YbE&checkin=2021-06-14&checkout=2021-06-18&adults=2&source=structured_search_input_header&search_type=filter_change',
        'https://www.airbnb.com.co/s/San-Andres--Colombia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=march&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&checkin=2021-06-14&checkout=2021-06-18&adults=2&source=structured_search_input_header&search_type=autocomplete_click&query=San%20Andres%2C%20Colombia&place_id=ChIJabPa3gamBY8RiYudmvoZ3yc'
    ]
    allowed_domains = [
        'airbnb.com.co'
        ]
    custom_settings = {'FEEDS' : {
            pathlib.Path('items.csv'):{
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True
            }
        },
    }
    def parse(self, response):

        rooms = response.xpath('//div[@class="_8ssblpx"]')
        date = response.xpath('//div[@class="_ljad0a"]/button[@class="_b2fxuo" and @data-index="1"]/div[@class="_1g5ss3l"]/text()').get()
        ciudad = response.xpath('//div[@class="_rrw786"]//h1[@class="_14i3z6h"]/text()').re(r'en\s(.+)')
        for room in rooms:

            title = room.xpath('.//div[@class="_r6zroz"]//div[@class="_bzh5lkq"]/text()').get()
            url = "https://www.airbnb.com.co" + room.xpath('.//div[@class="_8s3ctt"]/a/@href').get()
            calificacion = room.xpath('.//div[@class="_1bbeetd"]//span[@class="_18khxk1"]/@aria-label').re(r'\s(\d+\.\d+).*;\s(\d+)')
            reference = room.xpath('.//div[@class="_1tanv1h"]/div[@class="_b14dlit"]/text()').get()
            precio = int(room.xpath('.//div[@class="_ls0e43"]//span[@class="_olc9rf0"]/text()').re(r'^\$(\d+,\d+)')[0].replace(',',''))
            contains = room.xpath('.//div[@class="_8s3ctt"]//div[@class="_kqh46o"]/text()').getall()

            yield dict( title = title,
                        date = date,
                        reference = reference,
                        url = url,
                        calificacion = calificacion,
                        precio = precio,
                        contains = contains,
                        ciudad=ciudad)
        
        next_link = response.xpath('//a[@aria-label="Siguiente" and @class="_za9j7e"]/@href').get()
        if next_link:
            yield response.follow('https://www.airbnb.com.co'+next_link, callback= self.parse)
