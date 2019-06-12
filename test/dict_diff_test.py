from caesar.dict_differ import DictDiffer

CURRENT_DICT = {
    "1":"11",
    "2":"22",
    "4":"44"
}

PAST_DICT = {
    "2":"22",
    "3":"33",
    "4":"444"
}

if __name__ == "__main__":
    dict_differ = DictDiffer(current_dict=CURRENT_DICT, past_dict=PAST_DICT)
    print('added: ', dict_differ.added())
    print('removed: ', dict_differ.removed())
    print('changed: ', dict_differ.changed())
    print('unchanged: ', dict_differ.unchanged())