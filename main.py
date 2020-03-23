import numpy as np
import csv
import yaml



class Operation4:
    def __init__(self):
        self.num_question = 10 # the number of question
        self.num_digit = 1 # the number of digit
        self.isNegative = False # negative value question is OK?
        self.isDecimal = False # decimal question is OK?


    def pre_calc(self, admd):
        if self.isNegative == True:
            lim_l = -1 * 10**(self.num_digit)+1
            lim_h = 10**(self.num_digit)-1
        else:
            lim_l = 10**(self.num_digit-1)
            lim_h = 10**(self.num_digit)-1

        if self.isDecimal == True:
            np.set_printoptions(precision=2)
            arr = (lim_h - lim_l) * np.random.rand(self.num_question, 2) + lim_h
        else:
            arr = np.random.randint(lim_l, lim_h, (self.num_question, 2))

        if self.isNegative == False and admd is 'diff': # if diff ans is negative
            # diff_positive = np.where(arr[:, 0] >= arr[:, 1])
            diff_negative = np.where(arr[:, 0] < arr[:, 1])

            for i in diff_negative[0]:
                arr_index = arr[i]
                arr[i] = arr_index[1], arr_index[0]

        return arr


    def calc_ope4(self, admd):
        calc_formula = self.pre_calc(admd)

        if admd == 'add':
            calc_result = np.array([np.sum(calc_formula, axis=1)]).T
            calc_info = 'add'
            calc_symbol = '+'
    
        elif admd == 'diff':
            calc_result = np.array(np.diff(calc_formula, axis=1) * (-1))
            calc_info = 'diff'
            calc_symbol = '-'

        elif admd == 'multiply':
            calc_result = np.array([calc_formula[:,0] * calc_formula[:,1]]).T
            calc_info = 'multiply'
            calc_symbol = '*'

        elif admd == 'div':
            calc_result = np.array([calc_formula[:,0] / calc_formula[:,1]]).T
            calc_info = 'div'
            calc_symbol = '/'
        
        else:
            return 'ERROR', 'CHECK ARGUMENT'

        # reshape 
        output_formula = np.array([calc_formula[:, 0], np.repeat(calc_symbol, self.num_question), calc_formula[:, 1], np.repeat('=', self.num_question)], dtype='str').T
        output_calc = np.concatenate([output_formula, calc_result], axis=1)
        return calc_info, output_calc



def export_tsv(read_data):
    f_name = 'export_tsv'
    with open(f_name, mode='w', encoding='utf-8') as fo:
        tsv_writer = csv.writer(fo, delimiter='\t')
        tsv_writer.writerows(read_data)


def export_yaml():
    f_name = 'export_yaml'


def main():
    operation4class = Operation4()
    calc_info, output_calc = operation4class.calc_ope4('div')
    print(calc_info,'\n', output_calc)
    export_tsv(output_calc)


if __name__ == '__main__':
    main()
