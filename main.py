from fastapi import FastAPI
from src.utils.hybrid_search import HybridSearch
from src.types.search_params import SearchParams
from typing import List

hybrid_search = HybridSearch()

app = FastAPI()


@app.post("/text_search")
async def query_images_with_text(search_params: SearchParams)->List[str]:
    res = hybrid_search.hybrid_search(search_params.query, search_params.qdrant_limit, search_params.mieli_limit,
                                search_params.category_names, search_params.price_low, search_params.price_high)
    print(search_params)
    res_urls = [i.images[0] for i in res]
    return res_urls


@app.post("/agent")
async def talk_to_agent(text: str):
    return {"message": f"Hello {text}"}
