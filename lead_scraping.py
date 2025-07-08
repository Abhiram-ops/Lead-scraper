import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import re
import csv
import matplotlib.pyplot as plt

SERPAPI_KEY = "f055ec0ebda9fee006ccb40115913787ea357848d03cf976ceb994fd9a349057"

def extract_contacts_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
        phones = set(re.findall(r"\+?\d[\d -]{8,}\d", text))

        return list(emails), list(phones)
    except Exception as e:
        return [], []

def search_leads(query, num_pages, update_progress):
    all_leads = []
    total_steps = num_pages * 10
    step = 0

    for page in range(num_pages):
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY,
            "start": page * 10
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for result in results.get("organic_results", []):
            link = result.get("link")
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            step += 1
            update_progress(step, total_steps)

            if link:
                emails, phones = extract_contacts_from_url(link)
                if emails or phones:
                    all_leads.append({
                        "url": link,
                        "title": title,
                        "snippet": snippet,
                        "emails": emails,
                        "phones": phones
                    })

    return all_leads

def export_to_csv(leads, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["URL", "Title", "Snippet", "Emails", "Phones"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow({
                "URL": lead["url"],
                "Title": lead["title"],
                "Snippet": lead["snippet"],
                "Emails": ", ".join(lead["emails"]),
                "Phones": ", ".join(lead["phones"])
            })

def show_chart(leads):
    only_emails = sum(1 for l in leads if l["emails"] and not l["phones"])
    only_phones = sum(1 for l in leads if l["phones"] and not l["emails"])
    both = sum(1 for l in leads if l["emails"] and l["phones"])

    labels = ['Only Emails', 'Only Phones', 'Both']
    sizes = [only_emails, only_phones, both]
    colors = ['#66b3ff', '#99ff99', '#ffcc99']

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.title('Lead Contact Info Distribution')
    plt.show()

# GUI setup
def run_scraper():
    query = query_entry.get()
    try:
        pages = int(pages_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Pages must be a number.")
        return

    if not query or pages <= 0:
        messagebox.showerror("Invalid Input", "Please provide valid query and pages.")
        return

    progress["value"] = 0
    window.update()

    def update_progress(current, total):
        percent = (current / total) * 100
        progress["value"] = percent
        status_label.config(text=f"Progress: {int(percent)}%")
        window.update_idletasks()

    status_label.config(text="Scraping started...")
    leads = search_leads(query, pages, update_progress)

    if not leads:
        messagebox.showinfo("No Leads", "No contact info found.")
        return

    status_label.config(text=f"Scraped {len(leads)} leads.")
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        export_to_csv(leads, save_path)
        messagebox.showinfo("Saved", f"Leads saved to {save_path}")
        show_chart(leads)

# --- GUI Layout ---
window = tk.Tk()
window.title("Lead Scraper Pro")
window.geometry("550x350")
window.resizable(False, False)

tk.Label(window, text="Search Query:").pack(pady=(10, 0))
query_entry = tk.Entry(window, width=70)
query_entry.insert(0, "AI/ML companies in India which are actively hiring interns contact")
query_entry.pack(pady=5)

tk.Label(window, text="Number of Pages:").pack()
pages_entry = tk.Entry(window, width=10)
pages_entry.insert(0, "3")
pages_entry.pack(pady=5)

tk.Button(window, text="Start Scraping", command=run_scraper, bg="#007BFF", fg="white", width=20).pack(pady=10)

progress = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=5)

status_label = tk.Label(window, text="")
status_label.pack()

tk.Label(window, text="© Lead Scraper by You", fg="gray").pack(side="bottom", pady=10)

window.mainloop()
