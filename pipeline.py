from dotenv import load_dotenv
from agent import built_scrape_page, built_search_agent, itinery_chain
load_dotenv()

def generate_itinary(destination:str, duration:str, preferences:str)->str:
    search=built_search_agent()

    search_result=search.invoke({
        "messages":[("user", f"Search for top attractions and activities in {destination} for a {duration} trip.")]
    })

    search_text=search_result["messages"][-1].content

    scrape=built_scrape_page()

    scrape_result=scrape.invoke({
        "messages":[("user", f"scrape me the details of the {destination} and details over the {preferences} within the {duration} from the {search_text}" )]
    })

    scrape_text=scrape_result["messages"][-1].content



    itinary=itinery_chain.invoke({
        "destination":destination,
        "duration": duration,
        "preferences": preferences,
        "extracted_facts": scrape_text
    })

    return itinary


if __name__ == "__main__":
    destination = input("Enter destination: ")
    duration = input("Enter trip duration (e.g., '3 days'): ")
    preferences = input("Enter your preferences & budget (e.g., 'street food, historical sites, budget'): ")

    print("\n[+] Gathering recommendations and building your itinerary...\n")
    
    result = generate_itinary(
        destination=destination,
        duration=duration,
        preferences=preferences
    )
    
    print("\n--- Final Generated Itinerary ---\n")
    print(result)