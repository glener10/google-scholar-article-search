import pandas as pd

def save_articles_csv(articles, OUTPUT_FILE_NAME):
  if articles:
    df = pd.DataFrame(articles)
    try:
      existing_df = pd.read_csv(OUTPUT_FILE_NAME)
      df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
      pass
    df.to_csv(OUTPUT_FILE_NAME, index=False)
    print(f"💾 articles sheet created - {len(articles)} articles")

def get_articles_in_csv(OUTPUT_FILE_NAME):
  try:
    df = pd.read_csv(OUTPUT_FILE_NAME)
    return len(df)
  except FileNotFoundError:
    return "⚠️ not found file to read the number of articles"