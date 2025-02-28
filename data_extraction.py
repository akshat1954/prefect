from prefect import flow, task
import requests
import json

@task
def extract_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("Response Content:", response.text[:500])

    if response.status_code == 200:
        raw_text = response.text
        json_text = raw_text[raw_text.index("{"): raw_text.rindex("}") + 1]  # Extract JSON part

        try:
            data = json.loads(json_text)
            transformed_data = [item['title'] for item in data.get('posts', [])]
            print(transformed_data)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
    else:
        print(f"Failed to fetch data: {response.status_code}")

    if response.status_code == 200 and response.text.strip():
        try:
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not valid JSON")
            return None
    else:
        print("Error: API returned empty or invalid response")
        return None

@task
def transform_data(data):
    transformed_data = [item['title'] for item in data]
    return transformed_data

@task
def load_data(transformed_data):
    for title in transformed_data[:5]:
        print(f"Title : {title}")

@flow
def test_flow(name="flow for testing"):
    data = extract_data()
    transformed_data = transform_data(data)
    load_data(transformed_data)

if __name__ == "__main__":
    test_flow()