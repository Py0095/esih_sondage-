import os
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import boto3


FILE_PATH = 'user_info_esih.json'  # Assurez-vous que le chemin d'accès est correct
BUCKET_NAME = 'esihbucketl4'
REGION_NAME = 'us-east-1'
VOTRE_ACCESS_KEY_ID ='AKIAXCJJH3O3U76C5TUC'
VOTRE_SECRET_ACCESS_KEY ='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'

QUITTER_PAYS_CHOICES = (
        ('oui', 'Oui'),
        ('non', 'Non'),
        ('incertain', 'Incertain'),
    )
    
AGE_CHOICES = (
        ('moins_20', 'Moins de 20 ans'),
        ('20_24', '20-24 ans'),
        ('25_29', '25-29 ans'),
        ('30_34', '30-34 ans'),
        ('35_plus', '35 ans et plus'),
    )

LEVEL_CHOICES = (
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
        ('L4', 'L4'),
        ('DUT1','DUT1'),
        ('DUT2','DUT2'),
    )

DUREE_SEJOUR_CHOICES = (
        ('moins_un_an', 'Moins d\'un an'),
        ('1_2_ans', '1-2 ans'),
        ('3_5_ans', '3-5 ans'),
        ('plus_5_ans', 'Plus de 5 ans'),
    )


OBJECTIF_CHOICES =(
    ('etudes_supplementaires', 'Etudes supplementaires'),
    ('raisons_professionnelles', 'Raisons professionnelles'),
    ('raisons_personnelles', 'Raisons personnelles')
)


def getFormulaire(request):
    context = {
        'QUITTER_PAYS_CHOICES': QUITTER_PAYS_CHOICES,
        'AGE_CHOICES': AGE_CHOICES,      
        'LEVEL_CHOICES': LEVEL_CHOICES,
        'DUREE_SEJOUR_CHOICES': DUREE_SEJOUR_CHOICES,
        'OBJECTIF_CHOICES': OBJECTIF_CHOICES,
        }
    existing_data = []

    if request.method == 'POST':

        quitter_pays = request.POST.get('quitter_pays')
        age = request.POST.get('age')
        niveau_etudes = request.POST.get('niveau_etudes')
        pays_vise = request.POST.getlist('pays_vise[]')
        duree_sejour = request.POST.get('duree_sejour')
        raison_depart = request.POST.getlist('raison_depart[]')
        objectif_depart = request.POST.get('objectif_depart')
        retour_pays_origine = request.POST.get('retour_pays_origine')
        

        user_info_json = {
            'quitter_pays': quitter_pays,
            'age': age,
            'niveau_etudes': niveau_etudes,
            'pays_vise': pays_vise,
            'duree_sejour': duree_sejour,
            'raison_depart': raison_depart,
            'objectif_depart': objectif_depart,
            'retour_pays_origine': retour_pays_origine,
        }


        # Vérifier si le fichier JSON existe
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r') as file:
                existing_data = json.load(file)

        existing_data.append(user_info_json)

        with open(FILE_PATH, 'w') as file:
            json.dump(existing_data, file, indent=4)

        with open(FILE_PATH, 'r') as file:
            local_data = json.load(file)

        merge_data_with_s3(BUCKET_NAME, FILE_PATH, VOTRE_ACCESS_KEY_ID, VOTRE_SECRET_ACCESS_KEY, REGION_NAME,local_data)
        # Rediriger vers la page de succès
        return redirect('success_page')

    context.update({'existing_data': existing_data})  

    return render(request,'formulaire.html', context)

def success_view(request):
    return render(request, 'success.html')


def merge_data_with_s3(bucket_name, file_name, access_key, secret_key, region, local_data):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

    try:
        # Vérifier si le fichier existe déjà dans le bucket S3
        s3.head_object(Bucket=bucket_name, Key=file_name)

        # Le fichier existe : récupération des données depuis S3
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        s3_data = json.loads(response['Body'].read().decode('utf-8'))

        # Fusionner les données locales avec les données S3
        s3_data.extend(local_data)

        # Envoyer les données fusionnées vers S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(s3_data))

        return True  # Fusion et envoi réussis vers S3
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Le fichier n'existe pas encore sur S3 : créer un nouveau fichier avec les données locales
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(local_data))
            return True  # Création du fichier sur S3 avec les données locales
        else:
            print("Une erreur s'est produite :", e)
            return False  # Échec de la fusion ou de l'envoi vers S3
        













