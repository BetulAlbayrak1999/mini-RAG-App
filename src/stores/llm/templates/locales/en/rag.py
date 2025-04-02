from string import Template


###### RAG PROMPTS ######


##### SYSTEM #####

system_prompt = Template(
    "\n".join(
        [
            "You are an assistant to generate a response for the user.",
            "You will be provided by a set of documents associated with the user's query.",
            "You have to generate a response based on the documents provided.",
            "Ignore the documents that are not related to the user's query.",
            "You can appologize to the user if you are not able to generate a response.",
            "You have to generate the response in the same language as the user's query.",
            "Be polite and respectful to the user.",
            "Be precise and concise in your response. Avoid unneccessary information.",
        ]
    )
)


##### DOCUMENT #####
document_prompt = Template(
    "\n".join(
        [
            "## Document No: $doc_num",
            "### Content: $chunk_text",
        ]
    )
)


##### FOOTER #####
footer_prompt = Template(
    "\n".join(
        [
            "Based only on the above documents, please generate an answer for the user.",
            "## Question:",
            "$query",
            "",
            "## Answer: ",
        ]
    )
)
