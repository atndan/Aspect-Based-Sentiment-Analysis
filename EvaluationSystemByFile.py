import re
import sys

def get_labels_from_filename(filename):
    labels = []
    with open(filename, 'r', encoding = 'utf-8') as file:
        datasets = file.read()
        count = 0
        for line in datasets.split('\n'):
            if line != '':
                if count == 0:
                    count += 1
                elif count == 1:
                    count += 1
                elif count == 2:
                    labels.append(line.strip())
                    count = 0
        file.close()
    #print(len(labels))
    return labels

def clean_label(label):
    label = re.sub('[^A-Za-z#&]', '', label)
    label = re.sub('\\s+', ' ', label)
    return label

def convert_labels_to_dict(labels):
    dict_labels = []
    for label in labels:
        label_line = label.split('},')
        _dict = {}
        for objectLabel in label_line:
            aspect = clean_label(objectLabel.split(',')[0]).strip()
            polarity = clean_label(objectLabel.split(',')[1]).strip()
            _dict[aspect] = polarity
        dict_labels.append(_dict)
    return dict_labels

def get_common_attributeEntities(dict_labels):
    AttributeEntities = []
    for _dict in dict_labels:
        for key in _dict:
            if key not in AttributeEntities:
                AttributeEntities.append(key)
    AttributeEntities = sorted(AttributeEntities)
    return AttributeEntities

def get_aspects(dict_labels):
    aspects = []
    for _dict in dict_labels:
        for key in _dict:
            aspects.append(key)
    return aspects

def count_aspects(labels, Common_AttributeEntities):
    aspects = get_aspects(labels)
    num_aspects = [0] * len(Common_AttributeEntities)
    for aspect in aspects:
        num_aspects[Common_AttributeEntities.index(aspect)] += 1
    return num_aspects

def evaluation_labels(gold_labels, answer_labels, Common_AttributeEntities):
    num_aspect_gold = count_aspects(gold_labels, Common_AttributeEntities)
    num_aspect_answer = count_aspects(answer_labels, Common_AttributeEntities)
    correct_answer_aspects = [0] * len(Common_AttributeEntities)
    correct_answer_labels = [0] * len(Common_AttributeEntities)

    for i, _dict in enumerate(answer_labels):
        for key in _dict:
            if key in gold_labels[i].keys():
                correct_answer_aspects[Common_AttributeEntities.index(key)] += 1
                if answer_labels[i][key].strip() == gold_labels[i][key].strip():
                    correct_answer_labels[Common_AttributeEntities.index(key)] += 1
    #print('Correct Answer Aspects: ', correct_answer_aspects)
    #print('---------------------------------------------------')
    #print('Correct Answer Labels: ', correct_answer_labels)
    #print('---------------------------------------------------')
    #infor_evaluation(correct_answer_aspects, num_aspect_answer, num_aspect_gold, Common_AttributeEntities)
    #print('---------------------------------------------------')
    infor_evaluation(correct_answer_labels, num_aspect_answer, num_aspect_gold, Common_AttributeEntities)

def infor_evaluation(correct_answer, num_aspect_answer, num_aspect_gold, Common_AttributeEntities):
    for aspect in Common_AttributeEntities:
        if correct_answer[Common_AttributeEntities.index(aspect)] == 0:
            p = r = f = 0.0
        else:
            p = correct_answer[Common_AttributeEntities.index(aspect)] * 100 / num_aspect_answer[Common_AttributeEntities.index(aspect)]
            r = correct_answer[Common_AttributeEntities.index(aspect)] * 100 / num_aspect_gold[Common_AttributeEntities.index(aspect)]
            f = 2 * p * r / (p + r)
        #print(aspect)
        #print('%0.2f\t%0.2f\t%0.2f' % (p, r, f))
    p = sum(correct_answer) * 100 / sum(num_aspect_answer)
    r = sum(correct_answer) * 100 / sum(num_aspect_gold)
    f = 2 * p * r / (p + r)
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')
    print('Mean Precision score: ', round(p,2))
    print('Mean Recall score: ', round(r,2))
    print('Mean F1 score: ', round(f,2))
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

def evaluation_system(gold_labels, answer_labels):
    gold_dicts = convert_labels_to_dict(gold_labels)
    answer_dicts = convert_labels_to_dict(answer_labels)
    AttributeEntities = get_common_attributeEntities(gold_dicts)
    print('---------------INFORMATION FILE--------------------')
    print('Aspect Name: ', AttributeEntities)
    print("Aspect Gold: ", count_aspects(gold_dicts, AttributeEntities))
    print("Aspect Answer: ", count_aspects(answer_dicts, AttributeEntities))
    print('---------------------------------------------------')
    evaluation_labels(gold_dicts, answer_dicts, AttributeEntities)

def evaluation_system_by_file(file_gold, file_predict):
    gold_labels = get_labels_from_filename(file_gold)
    answer_labels = get_labels_from_filename(file_predict)
    evaluation_system(gold_labels, answer_labels)


if __name__ == '__main__':
    # gold_labels = ['{RESTAURANT#GENERAL, positive}, {DRINKS#QUALITY, positive}, {DRINKS#PRICES, neutral}, {DRINKS#STYLE&OPTIONS, neutral}', '{LOCATION#GENERAL, neutral}, {RESTAURANT#MISCELLANEOUS, neutral}']
    # answer_labels = ['{RESTAURANT#GENERAL, positive}, {DRINKS#QUALITY, positive}', '{LOCATION#GENERAL, neutral}, {RESTAURANT#MISCELLANEOUS, neutral}']
    # evaluation_system(gold_labels, answer_labels)

    file_test = sys.argv[1]
    file_predict = sys.argv[2]
    evaluation_system_by_file(file_test, file_predict)
