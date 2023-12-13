# from django.db import models

# QUITTER_PAYS_CHOICES = (
#         ('oui', 'Oui'),
#         ('non', 'Non'),
#         ('incertain', 'Incertain'),
#     )
    
# AGE_CHOICES = (
#         ('moins_20', 'Moins de 20 ans'),
#         ('20_24', '20-24 ans'),
#         ('25_29', '25-29 ans'),
#         ('30_34', '30-34 ans'),
#         ('35_plus', '35 ans et plus'),
#     )

# LEVEL_CHOICES = (
#         ('Anonymous', 'Anonymous'),
#         ('L1', 'L1'),
#         ('L2', 'L2'),
#         ('L3', 'L3'),
#         ('L4', 'L4'),
#         ('DUT1','DUT1'),
#         ('DUT2','DUT2'),
#     )

# DUREE_SEJOUR_CHOICES = (
#         ('moins_un_an', 'Moins d\'un an'),
#         ('1_2_ans', '1-2 ans'),
#         ('3_5_ans', '3-5 ans'),
#         ('plus_5_ans', 'Plus de 5 ans'),
#     )


# OBJECTIF_CHOICE =(
#     ('etudes_supplementaires', 'Etudes supplementaires'),
#     ('raisons_professionnelles', 'Raisons professionnelles'),
#     ('raisons_personnelles', 'Raisons personnelles')
# )

# class UserInfo(models.Model):

#     quitter_pays = models.CharField(max_length=10, choices=QUITTER_PAYS_CHOICES)
#     age = models.CharField(max_length=10, choices=AGE_CHOICES)
#     niveau_etudes = models.CharField(max_length=10, choices=LEVEL_CHOICES)
#     duree_sejour = models.CharField(max_length=20, choices=DUREE_SEJOUR_CHOICES)
#     objectif_depart=models.CharField(max_length=50, choices=OBJECTIF_CHOICE)
#     retour_pays_origine = models.CharField(max_length=10, choices=QUITTER_PAYS_CHOICES)
    
#     # Champs restants à ajouter
#     pays_vise = models.CharField(max_length=20)

    
#     raison_depart=models.CharField(max_length=20)

#     # def __str__(self):
#     #     return self.name  # Si vous avez un champ 'name' dans le formulaire
















