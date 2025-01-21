import os

from openai import OpenAI
from pathlib import Path


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def upload_file(path, format="text/plain"):
    """
    Uploads a file to the OpenAI API.

    Args:
        path (str): The path to the file to be uploaded.
        format (str, optional): The format of the file. Defaults to "text/plain".

    Returns:
        str: The ID of the uploaded file.
    """
    file = Path(path)

    upload = client.uploads.upload_file_chunked(
        file=file,
        mime_type=format,
        purpose="batch",
    )

    return upload.id

def create_completion(prompt):
        """
        Creates a completion using the OpenAI API.

        Args:
            prompt (str): The prompt for generating the completion.

        Returns:
            str: The generated completion.

        Raises:
            None
        """
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a literary analysis assistant. Always ansert in markdown format"},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content

