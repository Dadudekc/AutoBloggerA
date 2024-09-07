# -------------------------------------------------------------------
# File Path: scripts/entry_parser.py
# Description: Parses raw journal entry data into a structured format for templating.
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# Section 1: Parse journal data into sections
# -------------------------------------------------------------------
# This function takes raw data and formats it into structured sections
def parse_journal_data(raw_data):
    parsed_data = {
        "date": raw_data.get("date", "N/A"),
        "intro": raw_data.get("intro", "No intro available."),
        "summary": raw_data.get("summary", "No summary available."),
        "accomplishments": raw_data.get("accomplishments", []),
        "challenges": raw_data.get("challenges", []),
        "lessons_learned": raw_data.get("lessons_learned", []),
        "next_steps": raw_data.get("next_steps", []),
    }
    return parsed_data

# -------------------------------------------------------------------
# Section 2: Function to handle edge cases and missing data
# -------------------------------------------------------------------
def handle_missing_data(parsed_data):
    for key, value in parsed_data.items():
        if not value:
            parsed_data[key] = f"{key.replace('_', ' ').capitalize()} not available."
    return parsed_data

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    sample_raw_data = {
        "date": "July 3, 2024",
        "summary": "Productive day refactoring the Trading Robot project.",
        "accomplishments": [{"title": "Code Refactoring", "detail": "Removed circular dependencies."}],
        # Other fields can be populated similarly
    }
    
    structured_data = parse_journal_data(sample_raw_data)
    final_data = handle_missing_data(structured_data)
    print(final_data)
