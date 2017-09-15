import os
import sys

import requests
import pandas as pd
from bs4 import BeautifulSoup
from unidecode import unidecode


# De donde hasta donde va el scraper. Tenemos hasta el 925
# Los partimos de a 500 cada uno, y los tiramos
# todos juntos en terminales separadas
start_line = 925
# La ultima linea deberia ser la 2903
end_line = 2903 - 500 * 3


def parser(html):
    """
    Parse the html to lines.

    Parameters
    ----------
    html: str
     Html text to parse

    Return
    ------
    lines: like-list
    """
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', {'class':'result'})

    # No se por que, pero hay algunos elementos que
    # nos son visibles y no me interesan
    if len(results) > 6:
        results = results[:6]
    else:
        return

    lines = []
    for result in results:
        ul_general = result.find('ul')

        data = {}
        for cnt_li, li_general in enumerate(ul_general.find_all('li', recursive=False)):
            # Text
            text = ' '.join(li_general.text.split())

            # Find the key
            key = li_general.find('span').text
            key = ' '.join(key.split()).replace(':', '')
            if key not in valid_keys:
                continue

            # Remove the key form the text
            text = text.replace(key, '', 1)
            # Remove "
            text = text.replace('"', "'")
            # If the text start with ':', remove it
            if text.startswith(':'):
                text = text[1:]
            # If the text end with ',', remove it
            if text.endswith(','):
                text = text[:-1]
            # Remove 'mas info' and similar words
            for word in replaces_words:
                if word in text:
                    text = text.replace(word, '')
            # Remove extra white spaces
            text = ' '.join(text.split())

            # Caratula sub clase
            # ==================
            involucrados = []
            involucrados_tipo = []
            letrados = []
            if key == 'Carátula':
                div = li_general.find_all('div', {'class': 'resalta'})
                caratula_type = [''.join(s.text.replace(':', '').split())
                                 for s in div]
                caratula_type = [s for s in caratula_type
                                 if s in sub_caratula]

                uls_sub = li_general.find_all('ul')
                for cnt, ul_sub in enumerate(uls_sub):

                    for li_sub in ul_sub.find_all('li'):
                        text_sub = ' '.join(li_sub.text.split())

                        # if text_sub endswith ' CERRAR', remove it
                        if text_sub.endswith(' CERRAR'):
                            text_sub = text_sub[:-7]

                        if 'VER LETRADOS Letrados' in text_sub:
                            persona, letrado = text_sub.split('VER LETRADOS Letrados')
                        else:
                            persona = text_sub
                            letrado = ''

                        letrado = [' '.join(name.text.split()) for name in
                                   li_sub.find_all('div', {'class': 'item'})]

                        letrado = [' '.join(let.split()) for let in letrado]
                        letrado = [let.replace(',', ' ') for let in letrado]
                        letrado = [let.replace('.', '') for let in letrado]
                        letrado = [unidecode(let).upper() for let in letrado]

                        involucrados.append(persona)
                        involucrados_tipo.append(caratula_type[cnt])
                        letrados.append(letrado)

                # Remove white spaces, dot and accent in the text
                # to make the names equals
                involucrados = [' '.join(invo.split()) for invo in involucrados]
                involucrados = [invo.replace('.', '') for invo in involucrados]
                involucrados = [invo.replace(',', '') for invo in involucrados]
                involucrados = [unidecode(invo).upper() for invo in involucrados]

                # Append to data
                data['involucrados'] = involucrados
                data['involucrados_tipo'] = involucrados_tipo
                data['letrados'] = letrados

            # Resolución/es sub clase
            # =======================
            resoluciones_sala = []
            resoluciones_link = []
            if key == 'Resolución/es':
                for link in li_general.find_all('a'):
                    if link.text.startswith('Ver'):
                        continue
                    else:
                        resoluciones_sala.append(link.text)
                        resoluciones_link.append(link.attrs['href'])

                data['resoluciones_sala'] = resoluciones_sala
                data['resoluciones_link'] = resoluciones_link

            # Radicacion sub clase
            # ====================
            radicacion_fecha = []
            radicacion_sala = []
            radicacion_fiscal = []
            radicacion_fiscalia = []
            if key == 'Radicación del expediente':
                for items in li_general.find_all('div', {'class': 'item-especial-largo'}):
                    fecha = items.find('div', {'class': 't1a'}).text
                    sala = items.find('div', {'class': 't2a'}).text
                    fiscal = items.find('div', {'class': 't3a'})
                    fiscalia = items.find('div', {'class': 't2a'})

                    # Remove white space
                    fecha = ' '.join(fecha.split())

                    # Algunos fiscales o fiscalias no estan
                    if fiscal:
                        fiscal = fiscal.text.replace('Fiscal: ', '')
                        radicacion_fiscal.append(fiscal)
                    else:
                        radicacion_fiscal.append('')
                    if fiscalia:
                        radicacion_fiscalia.append(fiscalia.text)
                    else:
                        radicacion_fiscalia.append('')

                    radicacion_fecha.append(fecha)
                    radicacion_sala.append(sala)

                data['radicacion_fecha'] = radicacion_fecha
                data['radicacion_sala'] = radicacion_sala
                data['radicacion_fiscal'] = radicacion_fiscal
                data['radicacion_fiscalia'] = radicacion_fiscalia

            if key == 'Carátula':
                text, rest = text.split(' VER INTERVINIENTES')

            data[key] = text

        # Some data miss some keys
        for key in valid_keys:
            if key not in data.keys():
                data[key] = ''

        #
        lines.append(data)

    return lines

# Base url to make the gets
url = "http://cij.gov.ar/sorteos"

# Set the header and share the cookies in all the requests
headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64; rv:45.0)'
                   ' Gecko/20100101 Firefox/45.0'),
}
session = requests.Session()
session.headers = headers

# Form to make the posts

form = {"fecha_exacta_juzgados":"14/09/2017",
        "selector":"rango",
        "fecha_juzgados_desde":"2013-07-04",
        "fecha_juzgados_desde_aux":"04/07/2013",
        "fecha_juzgados_hasta":"2017-09-14",
        "fecha_juzgados_hasta_aux":"14/09/2017",
        "oficina":"",
        "nombre[]":"",
        "paginaS1":"0",
        "paginaS2":"0",
        "origenPaginado":"S1"
}

# Search this keys
valid_keys = ['Fecha de Asignación', 'Expediente', 'Tipo', 'Motivo Asignación',
             'Motivo Asignación', 'Delitos', 'Origen', 'Dependencia Asignada',
              'Denunciantes', 'Denunciados']

# Words to replace
replaces_words = ['VER MÁS', 'VER MENOS', 'CERRAR']
# Sub categories
sub_caratula = ['DENUNCIADO', 'DENUNCIADOS', 'DENUNCIANTE', 'DENUNCIANTES',
                'QUERELLANTE', 'QUERELLANTES', 'IMPUTADO', 'IMPUTADOS',
                'PROCESADOS', 'PROCESADO', 'DEMANDADO', 'DEMANDADOS']
# Base url to make the gets
url = "http://cij.gov.ar/sorteos"

# Set the header and share the cookies in all the requests
headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64; rv:45.0)'
                   ' Gecko/20100101 Firefox/45.0'),
}
session = requests.Session()
session.headers = headers

# Form to make the posts

form = {"fecha_exacta_juzgados":"14/09/2017",
        "selector":"rango",
        "fecha_juzgados_desde":"2013-07-04",
        "fecha_juzgados_desde_aux":"04/07/2013",
        "fecha_juzgados_hasta":"2017-09-14",
        "fecha_juzgados_hasta_aux":"14/09/2017",
        "oficina":"",
        "nombre[]":"",
        "paginaS1":"0",
        "paginaS2":"0",
        "origenPaginado":"S1"
}

# Search this keys
valid_keys = ['Fecha de Asignación', 'Expediente', 'Tipo', 'Motivo Asignación',
             'Motivo Asignación', 'Delitos', 'Origen', 'Dependencia Asignada',
              'Denunciantes', 'Denunciados']

# Words to replace
replaces_words = ['VER MÁS', 'VER MENOS', 'CERRAR']
# Sub categories
sub_caratula = ['DENUNCIADO', 'DENUNCIADOS', 'DENUNCIANTE', 'DENUNCIANTES',
                'QUERELLANTE', 'QUERELLANTES', 'IMPUTADO', 'IMPUTADOS',
                'PROCESADOS', 'PROCESADO', 'DEMANDADO', 'DEMANDADOS']
# Path to save the CSV
base_dir = '../data-sorteos/'

# Create the output directory
if not os.path.isdir(base_dir):
    os.mkdir(base_dir)

# Output file
file_sorteos = open(base_dir + 'sorteos' + str(start_line) + '-' + str(end_line) + '.csv', 'a')

# Line format
line_sorteos = '''"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}"\n'''

# CSV head
head_sorteos = ','.join(valid_keys)

# Write head
if os.stat(base_dir + 'sorteos' + str(start_line) + '-' + str(end_line) + '.csv').st_size == 0:
    file_sorteos.write(head_sorteos + '\n')

request_count = start_line
causas_count = 0

print("Comenzando el scraping ...")


print("Retomando de la ", request_count)

while True:
    if end_line < request_count:
        print("\nScraping terminado")
        break

    # Progress text
    text_progress = "\rDescargando pagina: {0}. Casusas bajadas: {1}"
    print(text_progress.format(request_count, causas_count), end='')

    # Make the get
    form["paginaS1"] = str(request_count)
    response = session.post(url, data=form)
    lines = parser(response.text)

    if not lines:
        print("\nSaltando la linea ")
        request_count += 1
        continue

    # Save to CSVs
    for line in lines:
        # Causas file
        partial = [line[key] for key in valid_keys]
        file_sorteos.write(line_sorteos.format(*partial))

    request_count += 1
    causas_count += len(lines)

file_sorteos.close()
