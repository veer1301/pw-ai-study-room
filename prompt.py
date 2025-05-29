prompt_summary ="""

Task: You will be given a paragraph of text which can be in Hindi, English, or a mix of both.

1. First, identify the language of the paragraph automatically.
2. Then, check the length of the paragraph:
   - If it has **100 words or more**, generate a concise summary capturing the main points.
   - If it has **less than 100 words**, format the content neatly as notes or study material suitable for a student.
3. Output the result in the language specified by the user (second parameter), which will be one of these languages: Hindi, English, Kannada, Bengali, Tamil, Telugu, or Odia.

Requirements:
- The output should be clear, concise, and easy to understand.
- Only output the formatted summary or notes without extra explanation or labels.
- Translate the output into the requested language.

Here is the paragraph:
"{paragraph}"

Output language:
"{output_language}"
"""

