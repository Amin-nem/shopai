from fastapi import FastAPI
from qdrant_client import QdrantClient
from src.encoder.encoder import Encoder
from src.utils.hybrid_search import HybridSearch
from src.utils.load_json_data import load_json_data
from src.db.meili_client import MeiliClient
from src.db.q_client import QClient
from src.types.search_params import SearchParams
from src.assistant.agent_tools import search
from src.assistant.shoping_agent import get_shopping_agent
from src.types.agent_io import AgentOutput, AgentRequest, ImageURLs
from pathlib import Path
import logging

from dotenv import load_dotenv
load_dotenv(dotenv_path="config.env")


logging.basicConfig(
    level=logging.INFO,  # Set minimum log level
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# for storing agent conversations and memory
CONVERSATION_DB_PATH = Path(__file__).resolve().parent / "src" / "db" / "conversation_history" / "./conversation_history.db"
JSON_PATH = Path(__file__).parent / "products_1.json"
SESSION_NAME = "user_conversation"
USER_ID = "user"


encoder = Encoder()
m_client = MeiliClient()
qdrant_connection = QdrantClient(url="127.0.0.1", port=6333)
q_client = QClient(qdrantclient=qdrant_connection, encoder=encoder)
hybrid_search = HybridSearch(q_client, m_client)

def agent_search(query:str, num_image_search:int=3, num_keyword_search:int=3, search_function=hybrid_search)->str:
    """
        :param query: text to search for
        :param num_image_search: number of image searches based on query parameter (minimum is 1.)
        :param num_keyword_search: number of keyword searches based on query (minimum is 1.)
    """
    return search(query=query,num_image_search=num_image_search,num_keyword_search=num_keyword_search, search_function=search_function)

agent = get_shopping_agent(agent_search,conversation_db_path=CONVERSATION_DB_PATH, session_name=SESSION_NAME,user_id=USER_ID)


logger.info(f"loading data into databases")
data = load_json_data(str(JSON_PATH))[:1000]
q_client.batch_add_to_qdrant(data)
m_client.batch_add_to_meili(data)
logger.info(f"Finished loading data into databases")


app = FastAPI()


@app.post("/text_search")
async def query_images_with_text(search_params: SearchParams) -> ImageURLs:
    res = hybrid_search.hybrid_search(search_params.query, search_params.qdrant_limit, search_params.mieli_limit,
                                      search_params.category_names, search_params.price_low, search_params.price_high)
    return ImageURLs(image_search_results=[i.images[0] for i in res.qdrant_products],keyword_search_results=[i.images[0] for i in res.mieli_products])


@app.post("/agent")
async def talk_to_agent(text: AgentRequest) -> AgentOutput:
    res = agent.run(text.text)

    # If the agent didn't produce an ImageURLs object, return just the text
    if not res.content.image_urls:
        print(AgentOutput(chat_output=res.content.chat_output))
        return AgentOutput(chat_output=res.content.chat_output)

    # Otherwise, build a new AgentOutput with the existing image URLs
    print(AgentOutput(
        chat_output=res.content.chat_output,
        image_urls=ImageURLs(
            image_search_results=res.content.image_urls.image_search_results,
            keyword_search_results=res.content.image_urls.keyword_search_results
        )
    ))
    return AgentOutput(
        chat_output=res.content.chat_output,
        image_urls=ImageURLs(
            image_search_results=res.content.image_urls.image_search_results,
            keyword_search_results=res.content.image_urls.keyword_search_results
        )
    )