import json

def is_valid(data):
    if not isinstance(data, dict):
        return False
    if 'list1' not in data or 'list2' not in data:
        return False
    if not isinstance(data['list1'], list) or not isinstance(data['list2'], list):
        return False

    for lst in [data['list1'], data['list2']]:
        for movie in lst:
            if not isinstance(movie, dict):
                return False
            if 'title' not in movie or 'year' not in movie:
                return False
            if not isinstance(movie['year'], int):
                return False

    return True


def merged_list(list1, list2):
    res = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i]['year'] < list2[j]['year']:
            res.append(list1[i])
            i += 1
        else:
            res.append(list2[j])
            j += 1

    res.extend(list1[i:])
    res.extend(list2[j:])

    return res

def main():
    with open('input.txt', 'r') as f:
        data = json.load(f)

        if not is_valid(data):
            print("Invalid file")
            return

        result = merged_list(data['list1'], data['list2'])
        output = {"list0": result}
        print(json.dumps(output, indent=2))
main()
