
import os
import time
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load keys from env
load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
endpoint = os.getenv("SPEECH_ENDPOINT")


def generate_filename(text: str, extension: str = "wav") -> str:
    safe_snippet = "".join(c for c in text[:20] if c.isalnum() or c in (' ', '_')).strip().replace(" ", "_")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"speech_{safe_snippet}_{timestamp}.{extension}"
    
    # Save all audio files in a specific folder, e.g. "outputs"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)  # folder banayega agar nahi hai
    
    filepath = os.path.join(output_dir, filename)
    return filepath


def synthesize_speech(text: str, voice: str = 'hi-IN-SwaraNeural') -> str:
    """
    Synthesize text to speech and save to a file.
    Returns the output filename.
    """
    if not speech_key or not endpoint:
        raise EnvironmentError("Missing SPEECH_KEY or SPEECH_ENDPOINT in env")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=endpoint)
    speech_config.speech_synthesis_voice_name = voice

    output_file = generate_filename(text)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ Speech synthesized and saved to: {output_file}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"❌ Speech synthesis canceled: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print("Error details:", cancellation.error_details)
        raise RuntimeError("Speech synthesis failed.")

    return output_file

# Main execution
if __name__ == "__main__":
    text = input("🗣️ Enter the text to convert into speech:\n").strip()
    if text:
        fileName = synthesize_speech(text)
        print("Audio saved at:", fileName)
    else:
        print("⚠️ No text provided. Exiting.")
