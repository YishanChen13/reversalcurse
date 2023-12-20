import openai
import csv

def get_presidents(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [row[1] for row in csv.reader(file)][1:]

def query_gpt(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        max_tokens=64,
        temperature=0.0,
    )
    conversation.append({"role": "assistant", "content": response.choices[0].message['content']})
    return conversation

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
        # Query for the wife of the president
        conversation = [
            {"role": "system", "content": "You are a helpful and terse assistant. Give me only the name. If the answer is unknown or not applicable, answer with “Unknown”"},
            {"role": "user", "content": f"Who is the wife of {president}?"}
        ]
        conversation = query_gpt(conversation)
        wife = conversation[-1]['content']

        # Query for the husband of the wife
        conversation.append({"role": "user", "content": f"Who is the husband of {wife}?"})
        conversation = query_gpt(conversation)
        husband = conversation[-1]['content'] if wife.lower() != "unknown" else "Unknown"

        spouse_results.append([president, wife, husband])
        print(f"Processed {idx}/{len(presidents)} - {president}: Wife - {wife}, Husband - {husband}")

    save_to_csv(spouse_results, 'presidents_spouses_incontext.csv', ['President', 'Wife', 'Husband'])

    # Evaluate accuracy
    accuracy = evaluate_accuracy('presidents_spouses_incontext.csv')
    print(f"Accuracy: {accuracy}%")

if __name__ == '__main__':
    main()