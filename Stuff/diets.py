def extract_preceding_words_with_kj(filename):
    result = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(1, len(lines)):
        current_first = lines[i].strip().split()[0] if lines[i].strip().split() else ''
        if 'kJ' in current_first:
            prev_line = lines[i-1].strip()
            prev_first = prev_line.split()[0] if prev_line.split() else ''
            if prev_first:
                result.append(prev_first)
    print(result)

#extract_preceding_words_with_kj("Děti_vše_190513.txt")



ALL_DIETS = ['0', '0BRK', '0M', '1', '10', '10/9', '11-1', '11-2', '11ML-1', '11ML-2', '12', '12M', '13-1', '13-2', '1NEM', '2', '2NEM', '3-1', '3-2', '3G', '3NB', '3PK-1', '3PK-2', '3S', '4', '4ML', '4S', '4S/9', '5', '9-150', '9-200', '9-250', '9-DYSF', '9/BLP', '9ML', '9NB', '9S', '9SML', 'BLP', 'BML', 'OK', 'S-T', 'S30', 'SP', 'SPD', 'VEG', 'VNM']

ALL_DIETS_KIDS = ['0', '0BRK', '0M', '1', '10', '11-1', '11-2', '11ML-1', '11ML-2', '12', '12M', '13-1', '13-2', '13M-1', '13M-2', '13ML-1', '13NB-1', '13NB-2', '1NEM', '2', '2NEM', '3-1', '3-2', '3PK-1', '3PK-2', '4', '4ML', '4S', '5', '9-150', '9/BLP', '9D', '9ML', '9S', 'BLP', 'BML', 'OK', 'S-T', 'SP', 'SPD', 'VEG', 'VNM', 'ZO']

DIETS = ['0BRK', '0M', '1', '10', '10/9', '11-1', '11ML-1', '12', '12M', '13-1', '1NEM', '2', '2NEM', '3-1', '3G', '3NB', '3PK-1', '3S', '4', '4ML', '4S', '4S/9', '5', '9-150', '9-200', '9-250', '9-DYSF', '9/BLP', '9ML', '9NB', '9S', '9SML', 'BLP', 'BML', 'OK', 'S-T', 'S30', 'SP', 'SPD', 'VEG', 'VNM']

DIETS_KIDS = ['0', '0BRK', '0M', '1', '10', '11-1', '11ML-1', '12', '12M', '13-1', '13-2', '13M-1', '13ML-1', '13NB-1', '1NEM', '2', '2NEM', '3-1', '3PK-1', '4', '4ML', '4S', '5', '9-150', '9/BLP', '9D', '9ML', '9S', 'BLP', 'BML', 'OK', 'S-T', 'SP', 'SPD', 'VEG', 'VNM', 'ZO']