import streamlit as st
import pandas as pd
import math


@st.cache
def load_data_xmail():
    df = pd.read_excel('Тарифы Иксмейл.xlsx')
    return df
xmail = load_data_xmail()

@st.cache
def load_data_new_partner():
    df = pd.read_excel('Тарифы Новый Партнер.xlsx', skiprows=3, names=['Направление','Населенный пункт','Сроки','t','до 0,5кг','1кг','доп 1 кг','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17','Unnamed: 18','Unnamed: 19','Unnamed: 20'])
    return df

new_partner = load_data_new_partner()

@st.cache
def load_data_flippost():
    df = pd.read_excel('Тарифы ФлипПост.xlsx', names=['Направление','Населенный пункт','kod','Сроки','до 0,5кг','доп 1 кг'])
    return df
flippost = load_data_flippost()

xmail = xmail[['Направление','Населенный пункт', 'РП тариф, 0,25', 'РП тариф, 0,5','РП тариф, 0,5-1,0кг','РП тариф + 1кг', 'Сроки']]
new_partner = new_partner[['Направление','Населенный пункт','Сроки','до 0,5кг','1кг','доп 1 кг']]






col1, col2, col3 = st.columns(3)

with col1:
    oblast = st.selectbox('Введите субъект РФ : ', '' + flippost['Направление'].unique())
with col2:
    town = st.selectbox('Введите субъект РФ : ', flippost['Населенный пункт'].unique(), format_func=lambda x: 'Выберите город' if x == '' else x)
with col3:
    weight = st.number_input('Введите вес', min_value=0.00, help='Вес указывается в кг')

def sum_flippost(oblast,town,weight):
    comp_name = 'Флиппост'
    if (len(flippost[(flippost.Направление == oblast) & (flippost['Населенный пункт'] == town)]) != 0)&(weight != 0.0):
        deliver_time = flippost[(flippost.Направление == oblast) & (flippost['Населенный пункт'] == town)]['Сроки'].tolist()[0]
        if weight < 0.5:
            sum_f_p = flippost[(flippost.Направление == oblast) & (flippost['Населенный пункт'] == town)]['до 0,5кг']
        else:
            coef = ((weight-0.5) // 1) + 1
            sum_f_p = flippost[(flippost.Направление == oblast) & (flippost['Населенный пункт'] == town)]['до 0,5кг']+(flippost[(flippost.Направление == oblast) & (flippost['Населенный пункт'] == town)]['доп 1 кг']*coef)
    else:

        sum_f_p = float('inf')
        town = 'нет города'
        deliver_time = 'нет данных'
        st.write("Компания : Флиппост\nТарифа по Флиппосту нет")
    return comp_name, town, round(float(sum_f_p),2), deliver_time


s_flippost = sum_flippost(oblast,town,weight)
# st.write("Компания: {c} \nГород доставки: {t} \nСумма доставки: {s} руб. \nСрок доставки в днях: {d} \n".format(c = sum_flippost(oblast,town,weight)[0],t=sum_flippost(oblast,town,weight)[1],s=sum_flippost(oblast,town,weight)[2], d=sum_flippost(oblast,town,weight)[3]))


def sum_new_partner(oblast,town,weight):
    comp_name = 'Новый партнер'
    if len(new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]) != 0:
        deliver_time = new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['Сроки'].tolist()[0]
        if weight < 0.5:
            sum_n_p = new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['до 0,5кг']
        elif weight < 1:
            sum_n_p = new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['1кг']
            if math.isnan(sum_n_p):
                coef = ((weight-0.5) // 1) + 1
                sum_n_p = new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['до 0,5кг']+(new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['доп 1 кг']*coef)
        else:
            coef = ((weight-1) // 1) + 1
            sum_n_p = new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['1кг']+(new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['доп 1 кг']*coef)
            if math.isnan(new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['1кг']):
                coef = ((weight-0.5) // 1) + 1
                sum_n_p = new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['до 0,5кг']+(new_partner[(new_partner.Направление == oblast) & (new_partner['Населенный пункт'] == town)]['доп 1 кг']*coef)
    else:
        sum_n_p = float('inf')
        town = 'нет города'
        deliver_time = 'нет данных'
        st.write("Компания : Новый партнер\nТарифа по Новому партнеру нет")

    return comp_name, town, round(float(sum_n_p),2), deliver_time


s_new_partner = sum_new_partner(oblast,town,weight)
# st.write("Компания: {c} \nГород доставки: {t} \nСумма доставки: {s} руб. \nСрок доставки в днях: {d} \n".format(c = sum_new_partner(oblast,town,weight)[0],t=sum_new_partner(oblast,town,weight)[1],s=sum_new_partner(oblast,town,weight)[2], d=sum_new_partner(oblast,town,weight)[3]))


def sum_xmail(oblast,town,weight):
    comp_name = 'Иксмейл'
    coef = ((weight-1) // 1) + 1
    if len(xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]) != 0:
        deliver_time = xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]['Сроки'].tolist()[0]
        if len(str(deliver_time)) == 0:
            deliver_time = 'не указано'
        if weight < 0.25:
            sum_x_m = xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]['РП тариф, 0,25']
        elif weight < 0.5:
            sum_x_m = xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]['РП тариф, 0,5']
        elif weight < 1:
            sum_x_m = xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]['РП тариф, 0,5-1,0кг']
        else:
            sum_x_m = xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]['РП тариф, 0,5-1,0кг']+(xmail[(xmail.Направление == oblast) & (xmail['Населенный пункт'] == town)]['РП тариф + 1кг']*coef)
    else:
        sum_x_m = float('inf')
        town = 'нет города'
        deliver_time = 'нет данных'
        st.write("Компания : Иксмейл\nТарифа по Иксмейлу нет")
    return comp_name, town, round(float(sum_x_m),2), deliver_time


s_xmail = sum_xmail(oblast,town,weight)


def choose_best(s_flippost,s_new_partner,s_xmail):

    min_sum = min(s_flippost[2],s_new_partner[2],s_xmail[2])
    if s_flippost[2] == min_sum:
        best_company = s_flippost[0]
        del_date = s_flippost[3]
    elif s_new_partner[2] == min_sum:
        best_company = s_new_partner[0]
        del_date = s_new_partner[3]
    else:
        best_company = s_xmail[0]
        del_date = s_xmail[3]
    return best_company,min_sum, del_date
# st.write("Компания: {c}"
#       "\nГород доставки: {t}"
#       "\nСумма доставки: {s} руб. "
#       "\nСрок доставки в днях: {d}"
#       "\n".format(c = sum_xmail(oblast,town,weight)[0],
#                                               t=sum_xmail(oblast,town,weight)[1],
#                                               s=sum_xmail(oblast,town,weight)[2],
#                                               d=sum_xmail(oblast,town,weight)[3]
#                                               )
#       )
if choose_best(s_flippost, s_new_partner, s_xmail)[1] == float('inf'):
    st.write("Ни в одной базе нет данных по тарифам")
else:
    st.write("Лучшая компания: {best_comp}\n".format(best_comp=choose_best(s_flippost,s_new_partner,s_xmail)[0]))
    #st.write("Самая выгодная сумма доставки: {min_sum} руб.\n".format(min_sum =choose_best(s_flippost,s_new_partner,s_xmail)[1]))
    st.write("Срок доставки: {del_date} дн.\n".format(del_date = choose_best(s_flippost,s_new_partner,s_xmail)[2]))
