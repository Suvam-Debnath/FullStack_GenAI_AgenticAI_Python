from ollama import Client
import requests

# Create Ollama client (local)
client = Client(host="http://localhost:11434")

# Function still exists (optional, but not used now)
def get_weather_info(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is: {response.text}"
    else:
        return f"Could not retrieve weather information for {city}."


def main():
    user_query = input("Enter your query: ")

    # Example of using the Ollama client to get weather information
    response = client.chat(
        model="gemma:2b",   # or llama3, mistral, etc.
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    print(response['message']['content'])

if __name__ == "__main__":
    main()


#print(get_weather_info("India"))