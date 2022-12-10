import concurrent.futures as pool
import time
from pathlib import Path

class PrintingStatistic:

    def __init__(self, file_name):

        self.file_name = file_name

    def print_data(self):
        vacancies_objects = statisticsReport.DataSet(self.file_name).vacancies_objects
        return PrintingStatistic.print_analytical_data(vacancies_objects, 'Программист')

    @staticmethod
    def print_analytical_data(vacancies_objects, vacancy_name):

        vacancies_dict = vacancies_objects
        years = set()
        for vacancy in vacancies_dict:
            years.add(int(vacancy.published_at[:4]))
        years = list(range(min(years), max(years) + 1))

        years_salary_dictionary = {year: [] for year in years}
        years_salary_vacancy_dict = {year: [] for year in years}
        years_count_dictionary = {year: 0 for year in years}
        years_count_vacancy_dict = {year: 0 for year in years}

        area_dict = {}

        for vacancy in vacancies_dict:
            year = int(vacancy.published_at[:4])
            years_salary_dictionary[year].append(vacancy.salary.get_salary_in_rub())
            years_count_dictionary[year] += 1
            if vacancy_name in vacancy.name:
                years_salary_vacancy_dict[year].append(vacancy.salary.get_salary_in_rub())
                years_count_vacancy_dict[year] += 1
            if vacancy.area_name in area_dict:
                area_dict[vacancy.area_name].append(vacancy.salary.get_salary_in_rub())
            else:
                area_dict[vacancy.area_name] = [vacancy.salary.get_salary_in_rub()]

        years_salary_dictionary = statisticsReport.InputConect.get_years_salary_dict(years_salary_dictionary)
        years_salary_vacancy_dict = statisticsReport.InputConect.get_years_salary_dict(years_salary_vacancy_dict)

        return [years_salary_dictionary, years_count_dictionary, years_salary_vacancy_dict, years_count_vacancy_dict]

def main(file_name):
    return PrintingStatistic(file_name).print_data()

def get_multiproc():
    fname = [f for f in Path(input('Введите название папки: ')).glob('*.csv')]
    with pool.ThreadPoolExecutor(max_workers=4) as executer:
        result = executer.map(main, fname)
    years_salary_dictionary = {}
    years_count_dictionary = {}
    years_salary_vacancy_dict = {}
    years_count_vacancy_dict = {}
    list_dict = [years_salary_dictionary, years_count_dictionary, years_salary_vacancy_dict, years_count_vacancy_dict]
    for year in result:
        for i in range(len(year)):
            year_items = year[i].items()
            for dic in year_items:
                list_dict[i][dic[0]] = dic[1]
    print(f'Динамика уровня зарплат по годам: {years_salary_dictionary}')
    print(f'Динамика количества вакансий по годам: {years_count_dictionary}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {years_salary_vacancy_dict}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {years_count_vacancy_dict}')

if __name__ == '__main__':
    start_time = time.time()
    get_multiproc()
    print("--- %s seconds ---" % (time.time() - start_time))