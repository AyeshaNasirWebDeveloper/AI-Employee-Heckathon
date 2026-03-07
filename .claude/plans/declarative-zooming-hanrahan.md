## Plan for Processing Files in `Needs_Action`

### Context
This plan outlines the steps to "process" files in the `C:\Users\HP\Desktop\AI_Employee_Vault\Needs_Action` directory, which has been defined as "Analyze and summarize content" by the user. The goal is to systematically read, understand, and summarize the content of various file types that may appear in this directory.

### Implementation Strategy
The processing will involve the following steps for each file found in `Needs_Action`:

1.  **Identify File Type**: Determine the file extension to infer its type (e.g., `.py` for Python, `.md` for Markdown, `.txt` for plain text). If the file extension is not immediately clear or is ambiguous, further inspection might be required (e.g., reading the first few lines to infer content).

2.  **Read File Content**: Utilize the appropriate tool based on the identified file type.
    *   For text-based files (e.g., `.py`, `.md`, `.txt`, `.json`, `.csv`): Use the `Read` tool to retrieve the file's content.
    *   For binary files (e.g., images, PDFs): The current instruction is to "analyze and summarize content." If binary files are encountered, I will need to ask the user for clarification on how to process them, as direct text summarization is not possible.
    *   For URLs or references within a file: If a file contains URLs, I will use `WebFetch` to retrieve and summarize the web content.

3.  **Analyze and Summarize Content**: After reading, the content will be analyzed to extract key information, purpose, and relevant details. The summarization will be concise and informative, focusing on the main points of the file.

    *   **Python (`.py`)**: Summarize the script's functionality, main functions, classes, and their purpose. If it's a test file, summarize what it tests.
    *   **Markdown (`.md`)**: Summarize the document's topic, main sections, and key takeaways.
    *   **Plain Text (`.txt`)**: Summarize the overall message or information contained within.
    *   **JSON/CSV**: Describe the data structure, types of data, and overall purpose of the data.

4.  **Handle Empty/Unknown Files**: If a file is empty or its type cannot be determined for meaningful analysis, a note will be made indicating this.

### Critical Files to be Modified/Accessed
*   `C:\Users\HP\Desktop\AI_Employee_Vault\Needs_Action\*`: All files within this directory will be read and processed according to this plan.
*   `C:\Users\HP\Desktop\AI_Employee_Vault\.claude\plans\declarative-zooming-hanrahan.md`: This plan file itself will be written and updated.

### Verification
After implementing the processing logic, verification will involve:
*   Manually checking the summaries generated for a sample of files to ensure accuracy and completeness.
*   Confirming that all files in `Needs_Action` are attempted to be processed.
*   Ensuring that unknown or empty files are handled gracefully with appropriate notifications.
