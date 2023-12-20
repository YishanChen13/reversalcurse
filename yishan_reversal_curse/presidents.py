import openai
import csv

def get_presidents(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [row[1] for row in csv.reader(file)][1:]

def query_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
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

    presidents = get_presidents('presidents.csv')
    print("Starting to process spouses of presidents...")
    spouse_results = []
    for idx, president in enumerate(presidents, 1):
        # Query for the spouse of the president
        spouse = query_gpt([
            {"role": "system", "content": "You are a helpful and terse assistant. Give me only the name. If the answer is unknown or not applicable, answer with “Unknown”"},
            {"role": "user", "content": f"Who is the wife of {president}?"}
        ])
        spouse_results.append([president, spouse])
        print(f"Processed {idx}/{len(presidents)} - {president}: Spouse - {spouse}")

    save_to_csv(spouse_results, 'presidents_spouses.csv', ['President', 'Spouse'])

    # Process the spouse of spouses from CSV
    print("Starting to process the spouse of spouses...")
    president_spouse_pairs = read_celebrities_from_csv('presidents_spouses.csv')
    second_spouses = []
    for idx, (president, spouse) in enumerate(president_spouse_pairs, 1):
        second_spouse = query_gpt([
            {"role": "system", "content": "You are a helpful and terse assistant. Give me only the name. If the answer is unknown or not applicable, answer with “Unknown”"},
            {"role": "user", "content": f"Who is the husband of {spouse}?"}
        ]) if spouse.lower() != "unknown" else "Unknown"
        second_spouses.append(second_spouse)
        print(f"Processed {idx}/{len(president_spouse_pairs)} - {president} (Spouse: {spouse}): Second Spouse - {second_spouse}")

    update_csv_with_additional_column('presidents_spouses.csv', second_spouses, ['President', 'Spouse', 'Second Spouse'])

    # Evaluate accuracy
    accuracy = evaluate_accuracy('presidents_spouses.csv')
    print(f"Accuracy: {accuracy}%")

if __name__ == '__main__':
    main()
