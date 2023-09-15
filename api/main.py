from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from youtube_search import YoutubeSearch
import json
from unidecode import unidecode
from urllib.parse import quote_plus
from flask import Flask
from pywebio.platform.flask import webio_view
from youtubesearchpython import VideosSearch
import re
from openpyxl import Workbook
app = Flask(__name__)
app.secret_key = "secretkeybaguette78"

def main():
    # Fonction qui utilise la librairie YoutubeSearch pour récupérer les données concernant une recherche Youtube
    def function_youtube_search_no_filter(champ_de_recherche):
        text_without_accents = unidecode(champ_de_recherche)
        text_with_plus = quote_plus(text_without_accents)
        search = VideosSearch(text_with_plus)
        results = YoutubeSearch(text_with_plus, max_results=30).to_dict()

        # Créez une liste pour stocker les résultats individuels
        all_results = {}

        for i in range(11):
            all_results[i] = search.result()['result']
            search.next()
        
        json_data = json.dumps(all_results, ensure_ascii=False)
        filename = 'datas.json'
        function_save_data_as_json(json_data,filename)
        function_format_data_as_json()
    
    def function_convert_json_to_excel(data_filename,excel_filename_output):
        with open(data_filename,encoding="utf8") as f:
            data = json.load(f)
        
        flattened_data = []
        for key, items in data.items():
            for item in items:
                if item['descriptionSnippet'] is not None:
                    description_text = ' '.join([snippet['text'] for snippet in item['descriptionSnippet']])

                flat_item = {
                    'type': item['type'],
                    'id': item['id'],
                    'title': item['title'],
                    'publishedTime': item['publishedTime'],
                    'duration': item['duration'],
                    'viewCount_text': item['viewCount']['text'],
                    'viewCount_short': item['viewCount']['short'],
                    'descriptionSnippet': description_text,
                    'channel_name': item['channel']['name'],
                    'accessibility': item['accessibility']['title'],
                    'accessibility_duration': item['accessibility']['duration'],
                    'link': item['link']
                }
                flattened_data.append(flat_item)
        
        wb = Workbook()
        ws = wb.active

        # Write headers to the worksheet
        headers = list(flattened_data[0].keys())
        ws.append(headers)

        # Write data rows to the worksheet
        for item in flattened_data:
            ws.append(list(item.values()))

        # Save the workbook as an Excel file
        excel_filename = excel_filename_output
        wb.save(excel_filename)

    #Fonction qui applique un filtre sur le nombre de vues des vidéos Youtube
    def function_youtube_search_filter_on_views(min_number,max_number):
        with open('datas.json',encoding="utf8") as f:
            data = json.load(f)
        filtered_results = {}
        # Parcourir les clés de 0 à 10
        for i in range(11):
            key = str(i)
            # Vérifier si la clé existe dans le dictionnaire
            if key in data:
                # Récupérer la liste d'objets JSON correspondant à cette clé
                object_list = data[key]
            
                # Filtrer les objets qui correspondent aux critères
                filtered_objects = [
                    obj
                    for obj in object_list
                    if min_number <= obj['viewCount']['text'] <= max_number
                ]
            
                # Ajouter les objets filtrés au dictionnaire résultat
                if filtered_objects:
                    filtered_results[key] = filtered_objects
        json_data = json.dumps(filtered_results, ensure_ascii=False)
        filename = 'datas_filter_view.json'
        function_save_data_as_json(json_data,filename)

    #Fonction qui applique un filtre sur la date de publication des vidéos YouTube
    def function_youtube_search_filter_on_publication_date(date_de_publication):
        with open('datas.json',encoding="utf8") as f:
            data = json.load(f)
        filtered_results = {}
        # Parcourir les clés de 0 à 10
        for i in range(11):
            key = str(i)
            # Vérifier si la clé existe dans le dictionnaire
            if key in data:
                # Récupérer la liste d'objets JSON correspondant à cette clé
                object_list = data[key]
            
                # Filtrer les objets qui correspondent aux critères
                filtered_objects = [
                    obj
                    for obj in object_list
                    if date_de_publication in obj['publishedTime']
                ]
            
                # Ajouter les objets filtrés au dictionnaire résultat
                if filtered_objects:
                    filtered_results[key] = filtered_objects

        json_data = json.dumps(filtered_results, ensure_ascii=False)
        filename = 'datas_filter_publication_date.json'
        function_save_data_as_json(json_data,filename)

    #Fonction qui applique plusieurs filtres sur les vidéos YouTube
    def function_youtube_search_all_filter(date_de_publication,min_number,max_number):
        with open('datas.json',encoding="utf8") as f:
            data = json.load(f)
        
        filtered_results = {}
        # Parcourir les clés de 0 à 10
        for i in range(11):
            key = str(i)
            # Vérifier si la clé existe dans le dictionnaire
            if key in data:
                # Récupérer la liste d'objets JSON correspondant à cette clé
                object_list = data[key]
            
                # Filtrer les objets qui correspondent aux critères
                filtered_objects = [
                    obj
                    for obj in object_list
                    if date_de_publication in obj['publishedTime']
                    and min_number <= obj['viewCount']['text'] <= max_number
                ]
            
                # Ajouter les objets filtrés au dictionnaire résultat
                if filtered_objects:
                    filtered_results[key] = filtered_objects

        json_data = json.dumps(filtered_results, ensure_ascii=False)
        filename = 'datas_filter.json'
        function_save_data_as_json(json_data,filename)

    # Formate les valeurs views du fichier json pour appliquer des filtres dessus
    def function_format_data_as_json():
        with open('datas.json',encoding='utf-8') as f:
            data = json.load(f)
        # Parcourir les clés de 0 à 10
        for i in range(11):
            key = str(i)
            if key in data:
            # Accédez à la liste correspondant à cette clé
                object_list = data[key]
                for obj in object_list:
                    view_count_text = obj['viewCount']['text']
                    view_count = int(re.sub(r'[^\d]+', '', view_count_text))
                    obj['viewCount']['text'] = view_count

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

    put_markdown("## Programme YoutubeSearch")

    put_text('Le Programme YoutubeSearch permet de récupérer des données concernant des vidéos en lien avec une recherche Youtube. Dans un premier temps il faut renseigner le champ de recherche Youtube sur lequel vous voulez effectuer une étude. Il est ensuite possible de filtrer les données selon plusieurs critères')
    put_html("<hr style='border-top: 3px solid #bbb'></hr>")
    champ_de_recherche = input("Entrez une valeur qui correspond au champ de recherche Youtube", type=TEXT,required=True)
    function_youtube_search_no_filter(champ_de_recherche)
    data_filename = 'datas.json'
    excel_filename_output = 'datas.xlsx'
    function_convert_json_to_excel(data_filename,excel_filename_output)
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
        date_de_publication = input("Choissisez la date de publication sur laquelle vous voulez appliquer le filtre", type=TEXT,required=True,datalist=['1 months','2 months','3 months','1 years','2 years','3 years','4 years','5 years','6 years','7 years','8 years','9 years'])
        put_html("<hr style='border-top: 3px solid #bbb'></hr>")
    elif filter_option == 'Filtrer sur la date de publication et le nombre de vues':
        put_text('2. Filtre sur la date de publication et le nombre de vues, renseigner une date de publication, une valeur minimale et une valeur maximale')
        date_de_publication = input("Choissisez la date de publication sur laquelle vous voulez appliquer le filtre", type=TEXT,required=True,datalist=['1 months','2 months','3 months','1 years','2 years','3 years','4 years','5 years','6 years','7 years','8 years','9 years'])
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
        data_filename = 'datas_filter_view.json'
        excel_filename_output = 'datas_filter_view.xlsx'
        function_convert_json_to_excel(data_filename,excel_filename_output)
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
        data_filename = 'datas_filter_publication_date.json'
        excel_filename_output = 'datas_filter_publication_date.xlsx'
        function_convert_json_to_excel(data_filename,excel_filename_output)
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
        data_filename = 'datas_filter.json'
        excel_filename_output = 'datas_filter.xlsx'
        function_convert_json_to_excel(data_filename,excel_filename_output)
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

# add a flask url_rule for routing
app.add_url_rule('/', 'webio_view', webio_view(main),methods=['GET','POST']) 

if __name__ =="__main__":
    app.run(debug=False)