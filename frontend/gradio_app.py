import gradio as gr
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def text_search_api(
        query: str,
        category_names: str,
        price_low: float,
        price_high: float,
        qdrant_limit: int,
        meili_limit: int,
):

    cat_names_list = [cat.strip() for cat in category_names.split(",") if cat.strip()]

    payload = {
        "query": query,
        "qdrant_limit": qdrant_limit,
        "mieli_limit": meili_limit,
        "category_names": cat_names_list,
        "price_low": price_low,
        "price_high": price_high
    }

    try:
        response = requests.post(f"{API_BASE_URL}/text_search", json=payload, verify=False)  # Temporarily disabling SSL
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Return empty lists with an error message as a separate field if needed
        return {
            "image_search_results": [f"Error: {str(e)}"],
            "keyword_search_results": []
        }

    # The FastAPI endpoint returns a JSON with image_search_results and keyword_search_results
    return response.json()


def agent_api(user_text: str):

    payload = {"text": user_text}
    try:
        response = requests.post(f"{API_BASE_URL}/agent", json=payload, verify=False)  # Temporarily disabling SSL
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Return an error message in chat_output and empty dict for images
        return f"Error: {str(e)}", {
            "image_search_results": [],
            "keyword_search_results": []
        }

    resp_json = response.json()
    chat_output = resp_json.get("chat_output", "")
    image_urls_data = resp_json.get("image_urls") or {}  # Ensure it's a dict

    # Ensure both keys exist to prevent KeyError
    image_search_list = image_urls_data.get("image_search_results", [])
    keyword_search_list = image_urls_data.get("keyword_search_results", [])

    return chat_output, {
        "image_search_results": image_search_list,
        "keyword_search_results": keyword_search_list
    }

def build_app():
    with gr.Blocks(title="Shopping App") as demo:
        gr.Markdown(
            """
            # Shopping App UI
            """
        )

        # =========== TAB 1: SEARCH =========== #
        with gr.Tab("Search"):
            with gr.Row():
                query = gr.Textbox(label="Query", placeholder="Search for shoes, phones, etc.")
            with gr.Row():
                category_names = gr.Textbox(
                    label="Categories (comma-separated)",
                    placeholder="e.g. electronics, shoes"
                )
            with gr.Row():
                price_low = gr.Number(label="Min Price", value=0)
                price_high = gr.Number(label="Max Price", value=1000)
            with gr.Row():
                qdrant_limit = gr.Slider(label="Qdrant Limit", minimum=1, maximum=50, step=1, value=5)
                meili_limit = gr.Slider(label="Meili Limit", minimum=1, maximum=50, step=1, value=5)

            search_btn = gr.Button("Search")

            # Galleries for Search Results
            search_image_search_gallery = gr.Gallery(
                label="Image Search Results", columns=3, height="auto"
            )
            search_keyword_search_gallery = gr.Gallery(
                label="Keyword Search Results", columns=3, height="auto"
            )

            def handle_text_search(query, category_names, price_low, price_high, qdrant_limit, meili_limit):
                results = text_search_api(query, category_names, price_low, price_high, qdrant_limit, meili_limit)
                return (
                    results.get("image_search_results", []),
                    results.get("keyword_search_results", [])
                )

            search_btn.click(
                fn=handle_text_search,
                inputs=[query, category_names, price_low, price_high, qdrant_limit, meili_limit],
                outputs=[search_image_search_gallery, search_keyword_search_gallery]
            )

        # =========== TAB 2: ASSISTANT =========== #
        with gr.Tab("Assistant"):
            with gr.Row():
                user_input = gr.Textbox(
                    label="Ask the Assistant",
                    placeholder="Hello, can you help me find ...?",
                    lines=2
                )
            agent_button = gr.Button("Send")

            # Chat history: list of (user, assistant) tuples
            conversation_state = gr.State([])

            # Chatbot component
            chatbot = gr.Chatbot(label="Assistant Conversation", height=400)

            # Galleries for Assistant Images
            assistant_images_image_search = gr.Gallery(
                label="Image Search Results", columns=3, height="auto"
            )
            assistant_images_keyword_search = gr.Gallery(
                label="Keyword Search Results", columns=3, height="auto"
            )

            def agent_interaction(user_text, history):
                chat_output, image_urls_data = agent_api(user_text)
                # Append the user message and assistant reply to history
                history = history + [(user_text, chat_output)]
                # Extract image lists
                image_search_list = image_urls_data.get("image_search_results", [])
                keyword_search_list = image_urls_data.get("keyword_search_results", [])
                return history, image_search_list, keyword_search_list, history

            # The button calls agent_interaction, returning 4 outputs
            agent_button.click(
                fn=agent_interaction,
                inputs=[user_input, conversation_state],
                outputs=[
                    chatbot,
                    assistant_images_image_search,
                    assistant_images_keyword_search,
                    conversation_state
                ]
            )

    return demo

if __name__ == "__main__":
    demo_app = build_app()
    demo_app.launch(server_name="0.0.0.0", server_port=7860, debug=True)
