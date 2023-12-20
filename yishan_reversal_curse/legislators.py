import openai
import csv

def get_legislators(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [row[0] for row in csv.reader(file)][1:]

def query_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=32,
        temperature=0.0,
    )
    return response.choices[0].message['content']

def save_to_csv(data, file_path, header):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def read_celebrities_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return list(csv.reader(file))[1:]

def update_csv_with_additional_column(file_path, additional_column, header):
    data = read_celebrities_from_csv(file_path)
    updated_data = []
    for row, child_name in zip(data, additional_column):
        updated_data.append(row + [child_name])
    save_to_csv(updated_data, file_path, header)

def evaluate_accuracy(file_path):
    data = read_celebrities_from_csv(file_path)
    matches = sum(1 for row in data if row[0].lower() == row[-1].lower())
    return (matches / len(data)) * 100 if data else 0


def main():
    openai.api_key = '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'

    # Get legislators from the CSV file
    legislators = get_legislators('legislators-names.csv')
    print("Starting to process mothers of legislators...")
    mother_results = []
    for idx, legislator in enumerate(legislators, 1):
        mother = query_gpt([
            {"role": "system", "content": "You are a helpful and terse assistant. Give me only the name. If the answer is unknown or not applicable, answer with “Unknown”"},
            {"role": "user", "content": f"Who is the famous {legislator}'s mother?"}
        ])
        mother_results.append([legislator, mother])
        print(f"Processed {idx}/{len(legislators)} - {legislator}: Mother - {mother}")

    save_to_csv(mother_results, 'legislators.csv', ['Legislator', 'Mother'])

    # Process children using mothers from CSV
    print("Starting to process children of legislators' mothers...")
    legislator_mother_pairs = read_celebrities_from_csv('legislators.csv')
    children = []
    for idx, (legislator, mother) in enumerate(legislator_mother_pairs, 1):
        child = query_gpt([
            {"role": "system", "content": "You are a helpful and terse assistant. Give me only the name. If the answer is unknown or not applicable, answer with “Unknown”"},
            {"role": "user", "content": f"Name the famous child of {mother}?"}
        ]) if mother.lower() != "unknown" else "Unknown"
        children.append(child)
        print(f"Processed {idx}/{len(legislator_mother_pairs)} - {legislator} (Mother: {mother}): Child - {child}")

    update_csv_with_additional_column('legislators.csv', children, ['Legislator', 'Mother'])

    # Evaluate accuracy
    accuracy = evaluate_accuracy('legislators.csv')
    print(f"Accuracy: {accuracy}%")

if __name__ == '__main__':
    main()