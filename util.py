import logging
import os
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('util')


def get_content_page(url: str) -> bytes:
    """
    Gets an url and returns its content
    :param url: An URL of a website
    :return: Content of the website
    """
    return requests.get(url.strip()).content


def get_xml_files(directory: str):
    logger.info('Extracting essays !!!')
    dirs = os.listdir(directory)
    for d in tqdm(dirs):
        xmls = os.listdir(directory+d+'/')
        for xml in xmls:
            if xml == 'xml':
                files = os.listdir(directory+d+'/'+xml+'/')
                for file in files:
                    if not file.startswith('.') and not file.endswith('.conll'):
                        extract_essays(directory+d+'/'+xml+'/'+file)


def extract_essays(xml_file: str):
    wrong_regex = r'<wrong>(.+)</wrong>'
    with open(xml_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')
        with open('uol_educaocao_1/'+xml_file.split('/')[3].split('.')[0]+'.txt', 'w') as out:
            score = soup.find('finalgrade').text
            out.write('# score: ' + score + '\n')
            title = soup.find('title').text
            out.write(title + '\n')
            body = soup.find('body')
            for essay in body.contents:
                match_wrong = re.match(wrong_regex, str(essay).strip())
                if match_wrong:
                    out.write(match_wrong.group(1))
                elif not str(essay).strip().startswith('<correct>') and str(essay) != '\n':
                    out.write(str(essay).strip())


def extract_essays_from_educao_uol(directory: str):
    logger.info('Extracting essays from educacao uol')
    files = os.listdir(directory)
    for file in tqdm(files):
        logger.info('File: ' + file)
        with open(directory+file, 'r') as f:
            for line in f.readlines():
                soup = BeautifulSoup(get_content_page(line), 'lxml')
                try:
                    score = soup.find(class_='mark').text
                except AttributeError:
                    logger.info('Searching for the score in <number> tag')
                    try:
                        score = soup.find('number').text
                    except AttributeError as e:
                        logger.error('Score does not found: ' + e)
                try:
                    title = soup.find(class_='container-composition').next_element.text.replace('/', '-')
                except AttributeError:
                    logger.info('Searching for the title in <h1> tag')
                    try:
                        title = soup.find('h1', attrs={'class': 'pg-color10'}).text.replace('/', '-')
                    except AttributeError as e:
                        logger.error('Title does not found: ' + e)
                with open('uol_educacao/'+line.split('/')[5].split('.')[0]+'.txt', 'w') as out:
                    out.write('# score: '+score+'\n')
                    out.write(title+'\n')
                    try:
                        essay = soup.find(class_='text-composition')
                        spans = essay.find_all('span', attrs={'class': 'certo'})
                        if not spans:
                            spans = essay.find_all('span', attrs={'style': 'color:#00b050'})
                    except AttributeError:
                        logger.info('Searching for the essay in <div> tag')
                        try:
                            essay = soup.find('div', attrs={'id': 'texto'})
                            spans = essay.find_all('span', attrs={'class': 'certo'})
                            if not spans:
                                spans = essay.find_all('span', attrs={'style': 'color:#00b050'})
                        except AttributeError as e:
                            logger.error('Essay does not found: ' + e)
                    for span in spans:
                        span.decompose()
                    for content in essay.find_all('p'):
                        out.write(content.text+'\n')


def extract_essays_from_vestibular_uol(directory: str):
    logger.info('Extracting essays from vestibular UOL')
    files = os.listdir(directory)
    for file in tqdm(files):
        logger.info('File: ' + file)
        with open(directory+file, 'r') as f:
            for line in f.readlines():
                soup = BeautifulSoup(get_content_page(line), 'lxml')
                tag = soup.find('div', attrs={'class': 'br-grid-3 margem-conteudo'})
                title = tag.find('h1').text.strip()
                with open('vestibular_uol/'+line.strip().split('/')[4]+'.txt', 'w') as out:
                    score = soup.find('span', attrs={'style': 'margin-right: 20px;'}).text.replace('NOTA FINAL:     ',
                                                                                                   '')
                    out.write('# score: ' + score + '\n')
                    out.write(title + '\n')
                    essay = soup.find(class_='conteudo-materia')
                    for content in essay.find_all('p'):
                        if not content.text.strip().startswith('Redação'):
                            pre = re.sub(r'\((.+)\)', '', content.text.strip())
                            pre1 = re.sub(r'Comentários do corretor(.+)', '', pre)
                            out.write(pre1)


def extract_links_from_vestibular_uol(html: str, theme: str):
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find('table', attrs={'id': 'redacoes_corrigidas'})
    links = tables.find_all('a')
    with open('vestibular_uol/'+theme+'.txt', 'w') as f:
        for link in links:
            f.write(link.get('href') + '\n')


def extract_links_from_educacao_uol(html: str):
    """
    Extracts links of a website and write the links in a file
    :param html: Content of a website
    """
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all(class_='rt-line-option')
    with open('uol_educacao_links/links.txt', 'w') as f:
        for title in titles:
            f.write(title.next_element.get('href') + '\n')


def check_consistency(directory_links: str, directory: str):
    files = os.listdir(directory_links)
    ids_links, ids = [], []
    for file in files:
        with open(directory_links+file, 'r') as f:
            for line in f.readlines():
                ids_links.append(line.strip().split('/')[4])
    files = os.listdir(directory)
    for file in files:
        # print(file.strip().split('-'))
        ids.append(file.strip().split('-')[1].split('.')[0])
    for link in ids_links:
        if link not in ids:
            print(link)


def create_files(directory: str):
    files = (os.listdir(directory))
    files = sorted(files)
    with open('novo/arquivos.txt', 'w') as f:
        for file in files:
            f.write(file+'\n')


def pre_processing(directory: str):
    files = os.listdir(directory)
    for file in files:
        logger.info('File: ' + file)
        with open(directory+file, 'r') as f:
            with open('vestibular_uol/' + file, 'w') as out:
                for line in f.readlines():
                    out.write(re.sub(r'Comentários do corretor(.+)', '', line))


if __name__ == '__main__':
    # url = 'https://vestibular.brasilescola.uol.com.br/banco-de-redacoes/tema-analfabetismo-funcional-no-brasil-por-que-esse-problema-ainda-persiste.htm'
    # theme = url.split('/')[4].split('.')[0]
    # html = get_content_page(url)
    # extract_essays_from_vestibular_uol(html, theme)
    # extract_essays_from_educao_uol('uol_educacao_links/')
    # extract_essays_from_vestibular_uol('vestibular_uol_links/')
    # check_consistency('vestibular_uol_links/', 'vestibular_uol/')
    # create_files('vestibular_uol/')
    # pre_processing('vestibular_uol_old_1/')
    get_xml_files('data/')
