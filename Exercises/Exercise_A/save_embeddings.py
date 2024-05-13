

from openai import OpenAI  # for generating embeddings
import pandas as pd  # for DataFrames to store article sections and embeddings
import re  # for cutting <ref> links out of Wikipedia articles
import tiktoken 
import PyPDF2

client = openai.OpenAI()

SECTIONS_TO_IGNORE = [
    "Contents",
    "List of Tables",
    "List of Figures",
    "References",
]

MAX_TOKENS = 1600
BATCH_SIZE = 1000   

# TODO #1: Create consts for GPT_MODEL and EMBEDDING_MODEL (small)
EMBEDDING_MODEL = "text-embedding-3-small"
GPT_MODEL = "gpt-3.5-turbo"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def split_sections_from_pdf(pdf_text):
    title = []
    text = []
    ignore = True
    current_section = "I.N.I.T.I.A.L-V.A.L.U.E"
    for line in pdf_text.split('\n'):
        line = line.strip()
        
        if not line:
            continue
        if is_new_section(line):
            ignore = ignore_section(line)
            if ignore:
                continue
            title.append(line)
            if current_section != "I.N.I.T.I.A.L-V.A.L.U.E":
                text.append(current_section)
            current_section = ""
        else:
            if not ignore:
                current_section += " " + line
    if current_section:
        text.append(current_section)
        
    
    sections = [(title),(text)]
    return sections

def ignore_section(line):
    if any(section in line for section in SECTIONS_TO_IGNORE):
        return True
    return False

def is_new_section(line):
    pattern = r"\d+\.\d+(?:\.\d+)? [A-Z].*?"
    
    if line.strip().count('.') > 7:
        return False
    if re.match(pattern, line.strip()):
        return True 
    if any(section in line for section in SECTIONS_TO_IGNORE):
        return True

    return False

def clean_section(section):

    titles = section[0]
    text = section[1]
    
    for line in text:
        line = re.sub(r"\[\d+\]", "", line)
        line = re.sub(r"\[\d\d+\]", "", line)
        line = line.strip()

    return (titles, text)


def num_tokens(text, model = GPT_MODEL):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def halved_by_delimiter(string, delimiter = "\n"):
    chunks = string.split(delimiter)
    if len(chunks) == 1:
        return [string, ""]  
    elif len(chunks) == 2:
        return chunks 
    else:
        total_tokens = num_tokens(string)
        halfway = total_tokens // 2
        best_diff = halfway
        for i, chunk in enumerate(chunks):
            left = delimiter.join(chunks[: i + 1])
            left_tokens = num_tokens(left)
            diff = abs(halfway - left_tokens)
            if diff >= best_diff:
                break
            else:
                best_diff = diff
        left = delimiter.join(chunks[:i])
        right = delimiter.join(chunks[i:])
        return [left, right]
    
    
def truncated_string(string, model, max_tokens, print_warning = True,):
    encoding = tiktoken.encoding_for_model(model)
    encoded_string = encoding.encode(string)
    truncated_string = encoding.decode(encoded_string[:max_tokens])
    if print_warning and len(encoded_string) > max_tokens:
        print(f"Warning: Truncated string from {len(encoded_string)} tokens to {max_tokens} tokens.")
    return truncated_string


def split_strings_from_subsection(title, text, max_tokens = 1000, model = GPT_MODEL, max_recursion = 5):

    string = "\n\n".join(title + text)
    num_tokens_in_string = num_tokens(string, model)

    if num_tokens_in_string <= max_tokens:
        return [string]

    elif max_recursion == 0:
        return [truncated_string(string, model, max_tokens)]

    else:
        for delimiter in ["\n\n", "\n", ". "]:
            left, right = halved_by_delimiter(text, delimiter=delimiter)
            if left == "" or right == "":

                continue
            else:

                results = []
                for half in [left, right]:
                    half_strings = split_strings_from_subsection(title, half,max_tokens,model,max_recursion - 1)
                    results.extend(half_strings)
                return results
            
    return [truncated_string(string, model, max_tokens)]


# TODO #2: Call the previous created functions
pdf_text = extract_text_from_pdf("LETI_SISTCA_2023_24_Team2_OpenAI.pdf")

pdf_sections = split_sections_from_pdf(pdf_text)

cleaned_sections = clean_section(pdf_sections)

MAX_TOKENS = 1600
strings = []
titles = cleaned_sections[0]
texts = cleaned_sections[1]
for i in range(len(titles)):
    strings.extend(split_strings_from_subsection(titles[i], texts[i], max_tokens=MAX_TOKENS))
    
    

embeddings = []
for batch_start in range(0, len(strings), BATCH_SIZE):
    batch_end = batch_start + BATCH_SIZE
    batch = strings[batch_start:batch_end]
    # TODO #3: Make a request to the embeddings API with the batch as input
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
    for i, be in enumerate(response.data):
        assert i == be.index  
    batch_embeddings = [e.embedding for e in response.data]
    embeddings.extend(batch_embeddings)
    
    
df = pd.DataFrame({"text": strings, "embedding": embeddings})


SAVE_PATH = "SISTCA_TEAM2.csv"
df.to_csv(SAVE_PATH, index=False)