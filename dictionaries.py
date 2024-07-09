#Define dictionaries for role and institution mappings
person_dict = {'Kooperationspartner': 'Cooperation Partner',
               'Kooperationspartnerinnen': 'Cooperation Partner',
               'Kooperationspartnerinnen / Kooperationspartner' : 'Cooperation Partner',
               'Co-Sprecherinnen / Co-Sprecher': 'Co-speaker',
               'Co-Sprecher' :'Co-speaker',
               'Gastgeber' : 'Host',
               'Gastgeberin' : 'Host',
               'Gastgeberinnen' : 'Host',
               'Gasteberen' :'Host', 
               'Beteiligte Personen' : 'Involved Person',
               'Beteiligte Person': 'Involved Person',
               'Teilprojektleiter' : 'Subproject Manager',
               'Teilprojektleiterinnen / Teilprojektleiter':'Subproject Manager',
               'Wissenschaftler' : 'Scientist',
               'Wissenschaftlerin' : 'Involved Scientist',
               'beteiligter Wissenschaftler' : 'Involved Scientist',
               'beteiligte Wissenschaftlerinnen / beteiligte Wissenschaftler' : 'Involved Scientist',
               'beteiligter Wissenschaftler': 'Involved Scientist',
               'Sprecherin' : 'Speaker',
               'Sprecher' : 'Speaker',
               'Sprecheren' : 'Speaker',
               'Sprecherinnen': 'Speaker',
               'Leiter' : 'Director',
               'stellvertr. Sprecher' : 'Deputy Speaker',
               'stellvertr. Sprecherin': 'Deputy Speaker'}
inst_dict = {"Untergeordnete Institutionen" :"Subordinate Institutions",
             "Antragstellende": "Applicant Institution",
             "Antragstellende Institution": "Applicant Institution",
             "Beteiligte Institution": "Participating Institution",
             "Beteiligte Einrichtung" :"Participating Institution",
             "Mitantragstellende Institution": "Co-applicant Institution",
             "Partnerorganisation":"Partner Organisation"}
antra_dict = {"Antragstellerinnen": "Applicant",
             "Antragsteller":"Applicant",
             "Antragstellerinnen / Antragsteller": "Applicant",
             "Antragstellerin": "Applicant", 
             "Mitverantwortliche": "Co-responsible",
             "Mitverantwortlich": "Co-responsible",
             "Mitverantwortlicher": "Co-responsible",
             "Mitverantwortliche / Mitverantwortlicher": "Co-responsible",
             'ausländ. Mitantragsteller': "Foreign Co-applicant",
             'ausländischer Mitantragsteller': "Foreign Co-applicant",
             'ausländ. Mitantragstellerin': "Foreign Co-applicant",
             'Mitantragsteller': "Co-applicant",
             'Mitantragstellerin': "Co-applicant",
             'Ehemaliger Antragsteller': "Former Applicant",
             'Ehemalige Antragstellerinnen / Ehemalige Antragsteller': "Former Applicant"}

#Combine all role and institution mappings into one dictionary
all_dicts = (person_dict|inst_dict|antra_dict)