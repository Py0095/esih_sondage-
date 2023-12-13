import os
from django.shortcuts import render
from django.http import JsonResponse
import json
import boto3

file_path = 'user_info.json'  # Assurez-vous que le chemin d'accès est correct


# VOTRE_ACCESS_KEY_ID =''
# VOTRE_SECRET_ACCESS_KEY =''
# NAME_DU_BUCKET =''
# OBJECT_NAME =''

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

    quitter_pays = request.POST.get('quitter_pays')
    age = request.POST.get('age')
    niveau_etudes = request.POST.get('niveau_etudes')
    pays_vise = request.POST.getlist('pays_vise[]')
    duree_sejour = request.POST.get('duree_sejour')
    raison_depart = request.POST.getlist('raison_depart[]')
    objectif_depart = request.POST.get('objectif_depart')
    retour_pays_origine = request.POST.get('retour_pays_origine')
    
    DATA = []

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

    existing_data = []

    # Vérifier si le fichier JSON existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)

    existing_data.append(user_info_json)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)


     # Enregistrer dans AWS S3 sans écraser les données précédentes
    s3 = boto3.client('s3', aws_access_key_id='VOTRE_ACCESS_KEY_ID', aws_secret_access_key='VOTRE_SECRET_ACCESS_KEY')
    bucket_name = 'NOM_DU_BUCKET'
    object_key = 'user_info.json'  # Nom de l'objet dans S3

    # Récupérer les données actuelles depuis AWS S3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        data_from_s3 = json.loads(response['Body'].read())

        # Fusionner les données locales avec les données de S3
        data_to_upload = data_from_s3 + existing_data
    except s3.exceptions.NoSuchKey:  # Si le fichier n'existe pas dans S3
        data_to_upload = existing_data

    # Charger les données fusionnées dans le bucket AWS S3
    s3.put_object(Bucket=bucket_name, Key='d99YB95EK6Xp9N2StQMXo7Tl7IoGwbbTwBuxYXbo', Body=json.dumps(data_to_upload, indent=4))




    context.update({'existing_data': existing_data})  

    return render(request,'formulaire.html', context)
