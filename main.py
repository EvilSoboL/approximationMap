from handlers.excel import ExcelHandler
from config import PATH_TO_EXCEL

if __name__ == '__main__':
    eh = ExcelHandler(PATH_TO_EXCEL)
    #print(eh.cleaned_sheets['Мазут_пар_2']['Q_пар, кг/ч'])


