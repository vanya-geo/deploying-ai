
# This is my first-ever chat bot! Please try it out!

It can tell you the weather in different locations and fun facts about the place. 
Here are some details:
- It has two tools: the open-meteo API and Tavily web search.
- It uses Gradio (for the UI) and Langchain.
- Keeps previous messages in memory

# Files:
app.py              -- this is the file that launches the chat interface (Gradio) and keeps track of the messages
main.py             -- this file builds the graph
tools_tavily_search -- Defines the web search tool
tools_weather       -- Defines the tool for the weather API 
prompts             -- Defines the system prompt

(not provided: secrets file with API key for OpenAI and Tavily)


# Guardrails:

If you ask it any other questions, it will respond with "whoops, we got off track ..."
If you ask it about the forbidden topics (cats, dogs, horoscopes, or Taylor Swift) it will respond with "Whoops, I can't talk about that..."
If you ask for its system prompt, it will respond with "Whoops, no can do.."


# Other notes:
At present, the bot has only two services (weather and search). I have not yet implemented a semantic search (using RAG). 
I'd like to do this in the future, especially if I can use some cool dataset that's location based (maybe trip advisor?).
Some other limitations: right now the weather API is only set up for current weather. I will be adding the other endpoints for forecast and historical weather. 
In the meantime, I use the system prompt to tell the model: for current weather, use the weather tool. For other dates, use the search tool. 
This seems to work well (makes you wonder if you need the weather tool at all ;) ).