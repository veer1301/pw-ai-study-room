from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import youtube_transcription
from fastapi import APIRouter, UploadFile, File, HTTPException
from tempfile import NamedTemporaryFile
import shutil
from read_binary_file import extract_text
from summarize import GPTService
from api_config import chat_api_key, chat_api_base, chat_api_version, chat_model
import os
import synthesized_voice_output
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/v1",
    tags=["YouTube Transcript"]
)

class TranscriptRequest(BaseModel):
    text: str

class YouTubeTranscriptRequest(BaseModel):
    url: str
class SummaryRequest(BaseModel):
    paragraph: str
    output_language: str

gpt_service = GPTService(chat_api_key, chat_api_base, chat_api_version, chat_model)

@router.post("/generate_summary", responses={500: {"description": "Internal Server Error"}})
def generate_summary(request: SummaryRequest):
    try:
        response = gpt_service.infer_message_class_from_prompting(request.paragraph, request.output_language)
        return {"summary": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.post("/youtube_transcript_generation", responses={500: {"description": "Internal Server Error"}})
def transcript_generator(request: YouTubeTranscriptRequest):
    try:
        response = youtube_transcription.get_transcript_val(request.url)
        return {"transcript": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.post("/extract_text_from_file", responses={500: {"description": "Internal Server Error"}})
async def extract_text_from_upload(file: UploadFile = File(...)):
    try:
        suffix = "." + file.filename.split(".")[-1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        text = extract_text(tmp_path)
        return {"extracted_text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.post("/generate-audio-from-text", responses={500: {"description": "Internal Server Error"}})
def transcript_generator(request: TranscriptRequest):
    try:
        file_path = synthesized_voice_output.synthesize_speech(request.text)

        # Validate file existence before returning
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Synthesized file not found")

        # Return the file for download
        return FileResponse(
            path=file_path,
            media_type="audio/wav",
            filename=os.path.basename(file_path)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
