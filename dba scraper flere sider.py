import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_dba():
    liste = []
    for i in range(1, 5):
        try:
            if i == 1:
                url = 'https://www.dba.dk/computer-og-spillekonsoller/mac/mac/type-macbook-air/?fra=privat'
            else:
                url = f'https://www.dba.dk/computer-og-spillekonsoller/mac/mac/type-macbook-air/side-{i}/?fra=privat'
            print('virker')
            response = requests.get(url)
            response = response.content
            soup = BeautifulSoup(response, 'html.parser')

            genstands_liste_1 = soup.find('tbody')
            genstande_1 = genstands_liste_1.find_all('a', class_='listingLink')
            genstands_liste_2 = soup.find('tbody')
            genstande_2 = genstands_liste_2.find_all('ul', class_='details')
            for span1, span2 in zip(genstande_1, genstande_2):
                pris = span1.find('span', class_='price')
                pris_værdi = pris.text.strip()
                beskrivelse = span1.find('span', class_='text')
                beskrivelse_text = beskrivelse.text.strip()
                link = span2.find('a', class_='visitedLink')
                location_element = span2.select_one('ul.details > li:nth-of-type(2) > span')
                location = location_element.text.strip()
                tidspunkt_element = span2.parent.find('span', class_='date')
                date_text = tidspunkt_element.text.strip() if tidspunkt_element else ''
                liste.append([pris_værdi, date_text, location, link['href'], beskrivelse_text])

            messagebox.showinfo("Done")
        except requests.exceptions.RequestException:
            messagebox.showerror("Fejl")

    excel_ark = pd.DataFrame(liste, columns=['Pris', 'Dato', 'Lokation', 'Link', 'Beksrivelse'])
    excel_ark.to_excel('DBA_Output.xlsx')

# Create the GUI window
window = tk.Tk()
window.title("DBA Scraper")
window.geometry('250x150')
window.config(bg='white')

# URL entry field
url_label = tk.Label(window, text="URL:")
url_label.pack()

url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Scraping button
scrape_button = tk.Button(window, text="Scrap DBA", command=scrape_dba)
scrape_button.pack()

# Configure widget colors for dark mode appearance
window.configure(bg="#1f1f1f")
url_label.configure(foreground="#00BFFF", background="#1f1f1f")
url_entry.configure(foreground="#00BFFF", background="#333333")
scrape_button.configure(foreground="#00BFFF", background="#333333")

# Run the GUI event loop
window.mainloop()
