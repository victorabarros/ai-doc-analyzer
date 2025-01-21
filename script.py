import os

from datetime import datetime

from app.content_handler import parse_content, save_in_disk
from app.services.open_ai import create_completion, upload_file

RAW_DOCUMENTS_PATH = "./documents"
DESTINATION_DIRECTORY = "output"


QUESTION = """
    Analyze how each work deals with the theme of social isolation. What are the authors’ points of view on this subject, and what parts of the novel corroborate these claims?
    Your output will be a 5 paragraph book report that states a clear thesis statement, makes clear arguments based on the content of each novel, and accurately cites sections of each novel, culminating in a concluding paragraph to summarize the arguments.
    Write it in markdown format.
"""


if __name__ == "__main__":
    all_items = os.listdir(RAW_DOCUMENTS_PATH)
    files = [{"path": f"{RAW_DOCUMENTS_PATH}/{item}", "name": os.path.splitext(item)[0]} for item in all_items]

    # Parse the content of each file and save it in a txt file
    for file in files:
        content = parse_content(file["path"])
        file["txt_output_path"] = save_in_disk(DESTINATION_DIRECTORY, file["name"], content)

    # Upload the files to OpenAI
    context = ""
    for file in files:
        file["upload_id"] = upload_file(file["txt_output_path"])

    context = ""
    for file in files:
        context += f"- {file['name']} (File ID: {file['upload_id']})\n"

    prompt = f"""
        Analyze the following documents based on the uploaded files, and than answer the question giving examples and in markdown format:

        Documents:
        {context}

        ---
        Question:
        {QUESTION}
    """

    completion = create_completion(prompt)

    report_name = f'ai_report_{datetime.now()}'.replace(' ', '_')
    save_in_disk(DESTINATION_DIRECTORY, report_name, completion, "md")

    print(f"Report saved to {report_name}")
