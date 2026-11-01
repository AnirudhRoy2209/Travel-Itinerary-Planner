import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_page

load_dotenv()


def get_llm():
    """Initialize the LLM dynamically at runtime so sidebar API keys work."""
    provider = os.getenv("LLM_PROVIDER", "Groq")

    if provider == "Google (Gemini)" and os.getenv("GOOGLE_API_KEY"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
    elif provider == "OpenAI" and os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "Anthropic (Claude)" and os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-3-5-haiku-latest",
            temperature=0,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    # Default to Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing Groq API Key! Please paste your GROQ_API_KEY in the sidebar.")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key,
    )


def built_search_agent():
    return create_agent(
        model=get_llm(),
        tools=[web_search],
        system_prompt=(
            "You are a dedicated travel search specialist. Your job is to take a destination "
            "and user preferences, formulate effective search queries, and use the web_search "
            "tool to find high-quality, relevant webpage URLs containing attractions, activities, "
            "and local events. Always return the relevant URLs you find with brief context on what each link covers."
        ),
    )


def built_scrape_page():
    return create_agent(
        model=get_llm(),
        tools=[scrape_page],
        system_prompt=(
            "You are a content extraction specialist. Your task is to use the scrape_page tool "
            "on provided URLs to extract verified, detailed travel information including attraction "
            "names, locations, timings, ticket costs, and seasonal events. Filter out navigation "
            "elements, ads, and irrelevant filler, returning only clean, structured factual notes."
        ),
    )


itinery_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert travel planner and local tour guide. "
        "Your task is to create a realistic, well-paced, day-by-day travel itinerary based on verified research and user preferences.\n\n"
        "Guidelines:\n"
        "- Group activities by geographic proximity to minimize travel time.\n"
        "- Structure each day into Morning, Afternoon, and Evening blocks.\n"
        "- Incorporate highlighted local events, attractions, and practical tips from the provided research.\n"
        "- Tailor the recommendations directly to the user's budget, trip duration, and interests.",
    ),
    (
        "human",
        "Destination: {destination}\n"
        "Trip Duration: {duration}\n"
        "Preferences & Budget: {preferences}\n\n"
        "Curated Research Data:\n{extracted_facts}\n\n"
        "Please generate a complete, structured day-by-day itinerary.",
    ),
])


def built_itinery_chain():
    return itinery_prompt | get_llm() | StrOutputParser()
