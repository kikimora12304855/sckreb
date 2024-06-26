import time
import random
import requests
import config
import BD
import log_system

BD = BD.DateBeas(config.DBname, config.DBuser, config.DBpass, config.DBhost, config.DBport)

table = "url"
int_inlet = 1
column = "url"
filter_column = "analyzed"
id_column = "id"
request_tabel =  """
    id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    url TEXT, 
    analyzed BOOLEAN DEFAULT FALSE
"""

url_baes = 'https://api.github.com/repositories'
headers = {
    'Authorization': f'Bearer {config.API_GITHUB}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Accept': 'application/vnd.github+json',
}


def search_next_url(get_url):
    link = get_url.headers.get('Link')
    if link:
        parts = link.split(',')
        for part in parts:
            if 'rel="next"' in part:
                next_url = part.split(';')[0].strip('<> ')
                return next_url

def main(url):
    
    log = log_system.LogSystem()

    BD.init_daese(table, request_tabel)

    last_line = BD.last_line_in_the_table(column, table)
    if last_line:
        url = last_line[0]


    while url:
        if random.randint(1, 10) == random.randint(1, 10):
            time.sleep(random.randint(10, 60))
        time.sleep(0.1)
        get_url = requests.get(url, headers=headers)

        while get_url.ok is not True:
            time.sleep(300)
            get_url = requests.get(url, headers=headers)
        
        try:
            url_next = search_next_url(get_url)
            if url_next:
                if url_baes == url:
                    BD.insert_table(table, int_inlet, column, (url,))
                    url = url_next

                elif int(url_next.split("=")[-1]) - int(url.split("=")[-1])  >= 100:
                    BD.insert_table(table, int_inlet, column, (url,))
                    url = url_next

                else:
                    time.sleep(60*60*24)
            else:
                time.sleep(60*60*24)

        except (Exception) as error:
            log.seve_to_log("W", "main in help_url_next", error)
            break




if "__main__" == __name__:
    main(url_baes)
