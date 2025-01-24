import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import docx
import re


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        try:
            with open(file_path, "rb") as f:
                return "".join([page.extract_text() for page in PyPDF2.PdfReader(f).pages])
        except Exception as e:
            return f"Error: {e}"
    elif file_path.endswith(".docx"):
        try:
            return "\n".join([p.text for p in docx.Document(file_path).paragraphs])
        except Exception as e:
            return f"Error: {e}"
    return "Invalid file type"


def extract_data(text):
    patterns = {
        "name": r"[A-Z][a-z]+(?: [A-Z][a-z]+)+",
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\b\d{10}\b",
        "skills": r"(?i)\b(python|java|c\+\+|sql|javascript|html|css|aws|azure|machine learning|data science|deep learning)\b",
    }
    return {
        "name": re.search(patterns["name"], text),
        "email": re.search(patterns["email"], text),
        "phone": re.search(patterns["phone"], text),
        "skills": re.findall(patterns["skills"], text),
    }


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF/DOCX files", "*.pdf *.docx")])
    if not file_path:
        return

    text = extract_text(file_path)
    if text.startswith("Error"):
        messagebox.showerror("Error", text)
        return

    data = extract_data(text)
    result_widget.delete("1.0", tk.END)
    result_widget.insert(
        tk.END,
        f"Name: {data['name'].group(0) if data['name'] else 'Not found'}\n"
        f"Email: {data['email'].group(0) if data['email'] else 'Not found'}\n"
        f"Phone: {data['phone'].group(0) if data['phone'] else 'Not found'}\n"
        f"Skills: {', '.join(set(data['skills'])).title() or 'Not found'}\n",
    )


# GUI setup
root = tk.Tk()
root.title("Resume Extractor")

tk.Label(root, text="Select a PDF or DOCX file:").pack(pady=5)
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)
result_widget = tk.Text(root, wrap=tk.WORD, height=10, width=60)
result_widget.pack(pady=10)

root.mainloop()
