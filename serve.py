import argparse, datetime, gspread, yaml
from oauth2client.service_account import ServiceAccountCredentials
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI

def log_to_sheets(sheet_name, creds_file, user, query, intent, confidence, reply):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([user, timestamp, query, intent, confidence, reply])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--persist", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--service_json")
    args = parser.parse_args()

    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=args.persist, embedding_function=embeddings)
    llm = ChatOpenAI()

    while True:
        query = input("Farmer: ")
        if query.lower() in ["exit", "quit"]: break

        docs = db.similarity_search(query, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        reply = llm.predict(f"Context: {context}\n\nQuestion: {query}\nAnswer:")

        print("Bot:", reply)

        if args.sheet and args.service_json:
            log_to_sheets(args.sheet, args.service_json, "User1", query, "N/A", "N/A", reply)

if __name__ == "__main__":
    main()
