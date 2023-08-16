from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from youtube_search import YoutubeSearch
import json
from unidecode import unidecode
from urllib.parse import quote_plus

# Fonction qui utilise la librairie YoutubeSearch pour récupérer les données concernant une recherche Youtube
def function_youtube_search_no_filter(champ_de_recherche):
    text_without_accents = unidecode(champ_de_recherche)
    text_with_plus = quote_plus(text_without_accents)
    results = YoutubeSearch(text_with_plus, max_results=50).to_dict()
    json_data = json.dumps(results, ensure_ascii=False)
    filename = 'datas.json'
    function_save_data_as_json(json_data,filename)
    function_format_data_as_json()

#Fonction qui applique un filtre sur le nombre de vues des vidéos Youtube
def function_youtube_search_filter_on_views(min_number,max_number):
    with open('datas.json') as f:
        data = json.load(f)
    # Filtrer les éléments entre la valeur minimale et la valeur maximale
    resultats_filtres = [element for element in data if min_number <= element['views'] <= max_number]
    json_data = json.dumps(resultats_filtres, ensure_ascii=False)
    filename = 'datas_filter_view.json'
    function_save_data_as_json(json_data,filename)

#Fonction qui applique un filtre sur la date de publication des vidéos YouTube
def function_youtube_search_filter_on_publication_date(date_de_publication):
    with open('datas.json') as f:
        data = json.load(f)
    # Filtrer les éléments contenant le terme de recherche
    resultats_filtres = [element for element in data if date_de_publication in element['publish_time']]
    json_data = json.dumps(resultats_filtres, ensure_ascii=False)
    filename = 'datas_filter_publication_date.json'
    function_save_data_as_json(json_data,filename)

#Fonction qui applique plusieurs filtres sur les vidéos YouTube
def function_youtube_search_all_filter(date_de_publication,min_number,max_number):
    with open('datas.json') as f:
        data = json.load(f)
    # Filtrer les éléments en fonction des critères de recherche
    resultats_filtres = [
        element
        for element in data
        if date_de_publication in element['publish_time']
        and min_number <= element['views'] <= max_number
        ]
    json_data = json.dumps(resultats_filtres, ensure_ascii=False)
    filename = 'datas_filter.json'
    function_save_data_as_json(json_data,filename)

# Formate les valeurs views du fichier json pour appliquer des filtres dessus
def function_format_data_as_json():
    with open('datas.json',encoding='utf-8') as f:
        data = json.load(f)
    for element in data:
        views = element['views']
        views = int(''.join(filter(str.isdigit, views)))  
        element['views'] = views
    with open('datas.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Sauvegarder les données au format JSON
def function_save_data_as_json(json_data,filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_data)

#Function qui permet de télécharger les données au format JSON dans le navigateur
def function_download_json(json_file_name,json_save_name,file_link_name):
    with open(json_file_name, encoding='utf-8') as f:
            data = json.load(f)
    json_content = json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8')
    put_file(json_save_name, json_content,file_link_name)

def main():
    put_markdown("## Programme YoutubeSearch")

    put_text('Le Programme YoutubeSearch permet de récupérer des données concernant des vidéos en lien avec une recherche Youtube. Dans un premier temps il faut renseigner le champ de recherche Youtube sur lequel vous voulez effectuer une étude. Il est ensuite possible de filtrer les données selon plusieurs critères')
    put_html("<hr style='border-top: 3px solid #bbb'></hr>")
    champ_de_recherche = input("Entrez une valeur qui correspond au champ de recherche Youtube", type=TEXT,required=True)
    function_youtube_search_no_filter(champ_de_recherche)
    put_text("1. Plusieurs filtres sont mis à votre disposition, il est également possible d'appliquer aucun filtre sur les résultats de la recherche")
    put_html("<hr style='border-top: 3px solid #bbb'></hr>")
    filter_option = radio("Choisissez une option de filtre :", options=['Appliquer aucun filtre', 'Filtrer sur le nombre de vues', 'Filtrer sur la date de publication','Filtrer sur la date de publication et le nombre de vues'])

    if filter_option == 'Filtrer sur le nombre de vues':
        put_text('2. Filtre sur le nombre de vues, renseigner une valeur minimale et une valeur maximale')
        min_number = input("Choisissez la valeur minimale du nombre de vues sur lequel vous voulez appliquer le filtre", type=NUMBER, value=1000)
        max_number = input("Choisissez la valeur maximale du nombre de vues sur lequel vous voulez appliquer le filtre", type=NUMBER,value=50000)
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
    elif filter_option == 'Filtrer sur la date de publication':
        put_text('2. Filtre sur la date de publication, renseigner la date de publication pour la recherche')
        date_de_publication = input("Choissisez la date de publication sur laquelle vous voulez appliquer le filtre", type=TEXT,required=True,datalist=['1 mois','2 mois','3 mois','1 an','2 ans','3 ans','4 ans','5 ans','6 ans','7 ans','8 ans','9 ans'])
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
    elif filter_option == 'Filtrer sur la date de publication et le nombre de vues':
        put_text('2. Filtre sur la date de publication et le nombre de vues, renseigner une date de publication, une valeur minimale et une valeur maximale')
        date_de_publication = input("Choissisez la date de publication sur laquelle vous voulez appliquer le filtre", type=TEXT,required=True,datalist=['2 ans','3 ans'])
        min_number = input("Choisissez la valeur minimale du nombre de vues sur lequel vous voulez appliquer le filtre", type=NUMBER, value=1000)
        max_number = input("Choisissez la valeur maximale du nombre de vues sur lequel vous voulez appliquer le filtre", type=NUMBER,value=50000)
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")

    if filter_option == 'Appliquer aucun filtre':
        put_text("2. Les données ont été récupérées avec succès vous pouvez les télécharger en cliquant sur le lien ci-dessous. Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats.json'")
        json_file_name = "datas.json"
        json_save_name = "resultats.json"
        file_link_name = 'Télécharger les résultats sans filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_text("Note : Aucun filtre n'a été appliqué sur les données")
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("3. Il est possible de relancer le programme YoutubeSearch pour obtenir de nouveaux résultats en actualisant la page internet.En cliquant sur le lien juste en dessous la page va s'actualiser automatiquement ")
        put_html("<a href='javascript:location.reload(true)'>Relancer le programme YoutubeSearch</a>")
    elif filter_option == 'Filtrer sur le nombre de vues':
        function_youtube_search_filter_on_views(min_number,max_number)
        put_text("3. Les données ont été récupérées avec succès vous pouvez les télécharger grâce au lien ci-dessous. Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats_filter.json'")
        json_file_name = "datas_filter_view.json"
        json_save_name = "resultats_filter.json"
        file_link_name = 'Télécharger les résultats avec filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_text("Note : Un filtre sur le nombre de vues a été appliqué sur le jeu de données")
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("4. Il est également possible de télécharger les données sans le filtre en cliquant sur le lien ci-dessous.Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats.json'")
        json_file_name = "datas.json"
        json_save_name = "resultats.json"
        file_link_name = 'Télécharger les résultats sans filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("5. Il est possible de relancer le programme YoutubeSearch pour obtenir de nouveaux résultats en actualisant la page internet.En cliquant sur le lien juste en dessous la page va s'actualiser automatiquement ")
        put_html("<a href='javascript:location.reload(true)'>Relancer le programme YoutubeSearch</a>")
    elif filter_option == 'Filtrer sur la date de publication':
        function_youtube_search_filter_on_publication_date(date_de_publication)
        put_text("3. Les données ont été récupérées avec succès vous pouvez les télécharger grâce au lien ci-dessous. Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats_filter.json'")
        json_file_name = "datas_filter_publication_date.json"
        json_save_name = "resultats_filter.json"
        file_link_name = 'Télécharger les résultats avec filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_text("Note : Un filtre sur la date de publication a été appliqué sur le jeu de données")
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("4. Il est également possible de télécharger les données sans le filtre en cliquant sur le lien ci-dessous.Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats.json'")
        json_file_name = "datas.json"
        json_save_name = "resultats.json"
        file_link_name = 'Télécharger les résultats sans filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("5. Il est possible de relancer le programme YoutubeSearch pour obtenir de nouveaux résultats en actualisant la page internet.En cliquant sur le lien juste en dessous la page va s'actualiser automatiquement ")
        put_html("<a href='javascript:location.reload(true)'>Relancer le programme YoutubeSearch</a>")
    elif filter_option == 'Filtrer sur la date de publication et le nombre de vues':
        function_youtube_search_all_filter(date_de_publication,min_number,max_number)
        put_text("3. Les données ont été récupérées avec succès vous pouvez les télécharger grâce au lien ci-dessous. Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats_filter.json'")
        json_file_name = "datas_filter.json"
        json_save_name = "resultats_filter.json"
        file_link_name = 'Télécharger les résultats avec filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_text("Note : Des filtres sur la date de publication et le nombre de vues ont été appliqués sur le jeu de données")
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("4. Il est également possible de télécharger les données sans le filtre en cliquant sur le lien ci-dessous.Le téléchargement apparaitra dans votre barre de navigation onglet Téléchargements sous le nom 'resultats.json'")
        json_file_name = "datas.json"
        json_save_name = "resultats.json"
        file_link_name = 'Télécharger les résultats sans filtre au format JSON'
        function_download_json(json_file_name,json_save_name,file_link_name)
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
        put_text("5. Il est possible de relancer le programme YoutubeSearch pour obtenir de nouveaux résultats en actualisant la page internet.En cliquant sur le lien juste en dessous la page va s'actualiser automatiquement ")
        put_html("<a href='javascript:location.reload(true)'>Relancer le programme YoutubeSearch</a>")

if __name__ == '__main__':
    start_server(main, port=8080)

