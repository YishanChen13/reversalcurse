import openai
import csv

def get_top_celebrities(file_path, limit=500):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()][:limit]

def query_gpt(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=64,
        temperature=0.0,
    )
    return conversation + [{"role": "assistant", "content": response.choices[0].message['content']}]

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

    celebrities = get_top_celebrities('top_celebrities.txt')
    print("Starting to process mothers of celebrities...")
    mother_child_results = []
    for idx, celebrity in enumerate(celebrities, 1):
        # Query for mother
        conversation = [
            {"role": "system", "content": "You are a helpful and terse assistant. Give me only the name. If the answer is unknown or not applicable, answer with “Unknown”"},
            {"role": "user", "content": f"Who is the famous {celebrity}'s mother?"}
        ]
        conversation = query_gpt(conversation)

        # Extract mother's name
        mother = conversation[-1]['content']

        # Query for child using the same conversation
        conversation.append({"role": "user", "content": f"Name the famous child of {mother}?"})
        conversation = query_gpt(conversation)

        # Extract child's name
        child = conversation[-1]['content']

        mother_child_results.append([celebrity, mother, child])
        print(f"Processed {idx}/{len(celebrities)} - {celebrity}: Mother - {mother}, Child - {child}")

    save_to_csv(mother_child_results, 'celebrities_incontext.csv', ['Celebrity', 'Mother', 'Child'])

    accuracy = evaluate_accuracy('celebrities_incontext.csv')
    print(f"Accuracy: {accuracy}%")

if __name__ == '__main__':
    main()