from ..function.hard_code import HardCode

class Case(HardCode):
    def __init__(self):
        super().__init__()




    def table_case(self,url):
        tables = self.tables_2(url)
        print(tables)

    def table_case_hard(self):
        tables = self.tables('https://www.ctdatacollaborative.org/story/gems2022')
        table_1 = tables[0].get('table_1_calculation_of_odds_ratio_from_the_parameters_of_the_logit_model')
        datas = []
        data_table1 = []
        for ii in range(2, 8):
            for i in range(2, len(table_1)):
                item = {}
                item.update({'title':'table_1_calculation_of_odds_ratio_from_the_parameters_of_the_logit_model'})
                for values in table_1[1][ii].values():
                    item.update({'category': values})
                for values in table_1[i][0].values():
                    item.update({'menu': values})
                for values in table_1[i][1].values():
                    item.update({'sub_menu': values})
                for values in table_1[i][ii].values():
                    item.update({'value':values})
                data_table1.append(item)

        # print(data_table1)


        table_2 = tables[1].get('table_2_odds_ratio_computed_for_the_global_estimates')
        data_table2 = []
        for item_2 in table_2:
            it2 = {}
            for itt2 in item_2:
                it2.update({'title':"table_2_odds_ratio_computed_for_the_global_estimates"})
                it2.update(itt2)
            data_table2.append(it2)

        # print(data_table2)

        table_3 = tables[2].get('table_3_global_estimation_of_forced_sexual_exploitation_of_adults_by_sex')
        # print(table_3)
        data_table3 = []
        for item_3 in table_3:
            it3 = {}
            for itt3 in item_3:
                it3.update({'title':"table_3_global_estimation_of_forced_sexual_exploitation_of_adults_by_sex"})
                it3.update(itt3)
            data_table3.append(it3)



        table_4 = tables[3].get('table_4_number_and_prevalence_of_persons_in_modern_slavery,_by_category,_sex,_age,_and_national_income_grouping')
        # print(table_4)
        data_table4 = []
        for iii in range(2, 16):
            for ii in range(1, 10):
                item = {}
                item.update({'title':'table_1_calculation_of_odds_ratio_from_the_parameters_of_the_logit_model'})
                for value in table_4[0][iii].values():
                     item.update({'category':value})
                for value in table_4[ii][1].values():
                    item.update(({'menu':value}))

                for value in table_4[ii][iii].values():
                    item.update({'value': value})
                data_table4.append(item)

        for data_it in data_table1:
            datas.append(data_it)

        for data_it in data_table2:
            datas.append(data_it)

        for data_it in data_table3:
            datas.append(data_it)

        for data_it in data_table4:
            datas.append(data_it)


        return datas

        # print(data_table4)
        # print()

        # for ii in range(2, 8):
        # for i in range(2, len(table_4)):
            # print(table_4[i])
            # item = {}
            # for values in table_4[1][1].values():
                # print(values)
                #     item.update({'category': values})
                # for values in table_4[1][ii].values():
                #     item.update({'sub_category': values})
                # for values in table_4[i][ii].values():
                #     item.update({'value': values})
                # data_table1.append(item)


                # print(item)
