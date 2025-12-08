import os

from google import genai
import tempfile

from src.file.minio_client import download_file_from_minio

client = genai.Client()
PROMPT = (
    "Analyze this file, summarize it, and create a quiz based on the summary.\n"
    "Return ONLY JSON in the following format:\n"
    "{ \"title\": \"Quiz title\", \"questions\": [{\"question\": \"Question text\", \"answers\": [\"Answer 1\", \"Answer 2\"]}] }"
)

async def generate_quiz_by_file(file_name: str) -> str:
    data = download_file_from_minio(file_name)

    # Keep the original file extension
    _, ext = os.path.splitext(file_name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(data)
        tmp.flush()
        path = tmp.name

    # Upload file
    sample_file = client.files.upload(file=path)

    # Clean up temp file
    os.remove(path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[sample_file, "Summarize this document"]
    )

    return response.text