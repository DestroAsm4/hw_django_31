import csv
import json

def to_json(csv_file, json_file, model):

    result = []

    with open(csv_file, encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        for row in rows:
            if 'is_published' in row:
                if row['is_published'] == 'True':
                    row['is_published'] = True
                else:
                    row['is_published'] = False

            if 'location_id' in row:
                row['locations'] = [row['location_id']]
                del row['location_id']
            result.append({'model': model, 'fields': row})

    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, indent=2, ensure_ascii=False))
        # json.dump(rows, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    to_json('ad.csv', 'ads.json', 'ads.ad')
    # to_json('categories.csv', 'categories.json', 'ads.categories')

    # to_json('user.csv', 'users.json', 'users.user')
    # to_json('location.csv', 'location.json', 'users.location')
