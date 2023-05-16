import requests
from bs4 import BeautifulSoup
import streamlit as st

def pegarDadosLucas():
    progress_text = "Carregando dados, por favor aguarde."
    my_bar = st.progress(0, text=progress_text)

    progress = 1

    url = 'https://www.veneza.com.br/imoveis/alugar'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    buildings = soup.find_all('a', class_='list__link')

    buildings_data = []
    for building in buildings:
        building_url = building['href']
        building_response = requests.get(f'https://www.veneza.com.br{building_url}')
        building_soup = BeautifulSoup(building_response.content, 'html.parser')
        building_type = building_soup.find('h1', class_='card__type').get_text()
        building_address = building_soup.find('p', class_='card__address').get_text()
        building_rent = building_soup.find_all('p', class_='ui__text--green')[2].get_text()
        building_area = building_soup.find_all('div', class_='card__item')[0].get_text()
        building_description = building_soup.find('p', class_='card__text').get_text()

        stripped_elements = [building_type.strip(), building_address.strip().replace(" ", ""), building_rent.strip(), building_area.strip(), building_description.strip()]

        buildings_data.append(stripped_elements)

        progress_percent = (progress / len(buildings))
        my_bar.progress(progress_percent, text=progress_text)     
        progress += 1

    # import openpyxl
    # from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

    # workbook = openpyxl.Workbook()
    # worksheet = workbook.active

    column_names = ['Título', 'Endereço', 'Aluguel', 'Área', 'Descrição']

    # for i in range(len(column_names)):
    #     cell = worksheet.cell(row=1, column=i+1, value=column_names[i])
    #     cell.font = Font(bold=True)
    #     cell.fill = PatternFill(start_color='B7DDE8', end_color='B7DDE8', fill_type='solid')
    #     cell.border = Border(top=Side(border_style='thin', color='000000'),
    #                         bottom=Side(border_style='thin', color='000000'),
    #                         left=Side(border_style='thin', color='000000'),
    #                         right=Side(border_style='thin', color='000000'))
    #     cell.alignment = Alignment(horizontal='center', vertical='center')

    # for row_index, row_data in enumerate(buildings_data):
    #     for col_index, cell_data in enumerate(row_data):
    #         cell = worksheet.cell(row=row_index+2, column=col_index+1, value=cell_data)
    #         cell.border = Border(top=Side(border_style='thin', color='000000'),
    #                             bottom=Side(border_style='thin', color='000000'),
    #                             left=Side(border_style='thin', color='000000'),
    #                             right=Side(border_style='thin', color='000000'))
    #         cell.alignment = Alignment(horizontal='center', vertical='center')
    #         if col_index == 2:
    #             cell.fill = PatternFill(start_color='B7DDE8', end_color='B7DDE8', fill_type='solid')

    # worksheet.column_dimensions['A'].width = 20
    # worksheet.column_dimensions['B'].width = 25
    # worksheet.column_dimensions['C'].width = 12
    # worksheet.column_dimensions['D'].width = 15
    # worksheet.column_dimensions['E'].width = 70

    # for i in range(2, 100):
    #     cell = worksheet.cell(row=i, column=5)
    #     cell.alignment = openpyxl.styles.Alignment(wrapText=True, horizontal='left', vertical='center')

    # from google.colab import drive
    # drive.mount('/content/drive', force_remount=True)

    # workbook.save('/content/drive/MyDrive/Real Estate Data.xlsx')

    # print('Sheet save successfully!')

    # import smtplib
    # from email.mime.text import MIMEText

    # sender_email = 'lucas.voriarocha@gmail.com'
    # sender_password = 'jgcfvlvpobznyumk'
    # receiver_email = 'lucas.voriarocha@gmail.com'
    # subject = 'Veneza Imoveis Dados'

    # text = "\n\n".join([("\n".join(item) + "\n") for item in buildings_data])

    # msg = MIMEText(text)
    # msg['Subject'] = subject
    # msg['From'] = sender_email
    # msg['To'] = receiver_email

    # with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    #     smtp.ehlo()
    #     smtp.starttls()
    #     smtp.ehlo()
    #     smtp.login(sender_email, sender_password)
    #     smtp.sendmail(sender_email, receiver_email, msg.as_string())

    # print('Email sent successfully!')

    # import numpy as np
    # import csv

    # output_path = '/content/drive/My Drive/Real Estate Data.csv'

    # with open(output_path, 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     for row in buildings_data:
    #         writer.writerow(row)

    # print('CSV file saved successfully!')

    import pandas as pd

    df = pd.DataFrame(buildings_data, columns=column_names)
    my_bar.empty()
    return df