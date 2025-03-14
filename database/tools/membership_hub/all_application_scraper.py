import applicant_scraper

def process_all_applications():
    applications = {
        # "Spring 2025 New Member Application": (7,9),
        # "Fall 2024 New Member Application": (8,11),
        # "Spring 2024 New Member Application": (8, 10), 
        # "Fall 2023 New Member Application": (9, 11),
        "Spring 2023 SEC New Member Application": (7,9)
    }

    email = "eunsooyeo@tamu.edu"
    password = "qlcthrma0530/Tam"
    
    results = {}
    
    for app, question_ranges in applications.items():
        start_q, end_q = question_ranges
        result = applicant_scraper.scrape_application(app, email, password, start_q, end_q)

        if result:
            results[app] = result
            print(f"Successfully scraped {app}")
        else:
            print(f"Failed to scrape {app}")
    
    return results

if __name__ == "__main__":
    process_all_applications()