'''
Descripttion: 
Author: Leiyan
Date: 2021-04-17 15:05:39
LastEditTime: 2021-05-11 11:35:30
'''
# -*- coding: utf-8 -*-

"""
功能 ： 常量

developer ： 雷艳

"""
import json

entity_Ner = ["Poetry", "Verse", "Poetrything",
              "Genre", "People", "Location", "Dynasty"]

entity_attribute = {
    "Poetry": "poetryName",
    "Verse": "verseContext",
    "Poetrything": "poetrythingName",
    "Genre": "genreName",
    "People": "peopleName",
    "Location": "locationName",
    "Dynasty": "dynastyName"
}

entity_main_attribute = {
    "Poetry": ["poetryName", "poetryId", "poetryAuthor", "poetryContext"],
    "Verse": ["verseContext", "verseId", "verseAuthor"],
    "Poetrything": ["poetrythingName", "poetrythingId", "poetrythingMeaning"],
    "Genre": ["genreName", "genreId"],
    "People": ["peopleName", "peopleId", "peopleNickname"],
    "Location": ["locationName", "locationId"],
    "Dynasty": ["dynastyName", "dynastyId"]
}

entity_attr = {
    "Poetry": ['poetryAppreciation', 'poetryBackground', 'poetryClass', 'dynasty', 'poetryAuthor', 'poetryTranslation',
               'poetryContext', 'poetryId', 'poetryName'],
    "Verse": ['verseId', 'verseDynasty', 'poetryId', 'verseAuthor', 'verseContext'],
    "Poetrything": ['poetrythingName', 'poetrythingMeaning', 'poetrythingId'],
    "People": ['peopleId', 'peopleNickname', 'peopleBurnPlace', 'peopleName', 'peopleAchievements', 'peopleBurnYear',
               'peopleAnecodate', 'peopleIntroduction'],
    "Genre": ['genreId', 'genreName'],
    "Dynasty": ['dynastyId', 'dynastyEnd', 'dynastyBegin', 'dynastyName'],
    "Location": ['locationName', 'locationId']
}

entity_relation = {
    "Poetry": ['poetryMentionPeopleTo', 'poetryBelongGenreTo', 'poetryBelongDynastyTo', 'poetryBelongTo',
               'poetryMentionThingTo', 'poetryMentionDynastyTo', 'poetryMentionPlaceTo'],
    "Verse": ['verseBelongDynastyTo', 'verseBeforeTo', 'verseNextTo', 'verseBelongToPeople', 'verseBelongTo',
              'verseMentionThingTo', 'verseMentionPeopleTo', 'verseMentionPlaceTo'],
    "Poetrything": [],
    "Genre": [],
    "Dynasty": [],
    "Location": []
}

question_path = './file/questions.txt'
dict_path = './file/dict/'
consistency_tree_path = './file/consistency_tree.txt'
add_weight_trees_path = './file/add_weight_tree.txt'
final_input_path = './file/weigted_tree_paris.txt'
conll_path = './file/conll.txt'
avaliable_template_path = './file/avaliable_query.txt'
question_file_path = './file/id.json'
json_path = './file/template.json'
score_path = './file/score.txt'


def read_data(filepath, flag=False, isjson=False):
    with open(filepath, "r", encoding='utf-8') as f:
        if isjson:
            data = json.load(f)
        elif flag:
            data = f.read().splitlines()
        else:
            f.read()
    f.close()
    return data


def save_data(filepath, content, flag=False, isjson=False):
    with open(filepath, "w", encoding='utf-8') as f:
        if isjson:
            json.dump(content, f, ensure_ascii=False, indent=4)
        elif flag:
            f.write('\n'.join(content))
        else:
            f.write(content)
    f.close()


def append_data(filepath, content, flag=False):
    with open(filepath, "a+", encoding='utf-8') as f:
        f.write('\n' + content)
    f.close()
