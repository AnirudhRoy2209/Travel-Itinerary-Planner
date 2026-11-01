import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_page

load_dotenv()


def get_llm(model_size: str = "large"):
    """
    Use separate Groq models for tool steps vs final generation so they don't 
    share the same 8,000 TPM bucket, and set max_retries=5 to auto-wait on short 429s.
    """
    provider = os.getenv("LLM_PROVIDER", "Groq")

    if provider == "Google (Gemini)" and os.getenv("GOOGLE_API_KEY"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_retries=5,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
    elif provider == "OpenAI" and os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=5,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif provider == "Anthropic (Claude)" and os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-3-5-haiku-latest",
            temperature=0,
            max_retries=5,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    # Default to Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing Groq API Key! Please paste your GROQ_API_KEY in the sidebar.")

    # Split across two models so each gets its own separate 8,000 TPM quota!
    groq_model = "openai/gpt-oss-20b" if model_size == "small" else "openai/gpt-oss-120b"

    return ChatGroq(
        model=groq_model,
        temperature=0,
        max_retries=5,
        api_key=api_key,
    )


def built_search_agent():
    return create_agent(
        model=get_llm("small"),
        tools=[web_search],
        system_prompt=(
            "You are a dedicated travel search specialist. Formulate a single concise search query "
            "and use the web_search tool once to find relevant URLs for attractions and activities. "
            "Return only the URLs found."
        ),
    )


def built_scrape_page():
    return create_agent(
        model=get_llm("small"),
        tools=[scrape_page],
        system_prompt=(
            "You are a content extraction specialist. Use the scrape_page tool on at most 2 URLs "
            "to extract concise travel details (attractions, timings, costs, food). "
            "Return brief, structured bullet points under 400 words."
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
    # Uses the fresh 120b model bucket for the final itinerary
    return itinery_prompt | get_llm("large") | StrOutputParser()
