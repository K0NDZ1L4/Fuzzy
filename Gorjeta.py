import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
calorias = ctrl.Antecedent(np.arange(0, 1001, 1), 'calorias')
atividade = ctrl.Antecedent(np.arange(0, 5, 1), 'atividade')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 100, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
calorias.automf(names=['pouco', 'razoavel', 'muita'],)
atividade.automf(names=['baixa', 'medio', 'alta'])




while True:
        func = input("SELECIONE A FUNÇÃO(TRI,GAU,TRA)\n")
        if func=="TRI":
                peso.automf(names=['magro', 'normal', 'pesado'])
                break
        elif func=="GAU":
                peso["magro"] = fuzz.gaussmf(peso.universe,30,10)
                peso["normal"] = fuzz.gaussmf(peso.universe,60,10)
                peso["pesado"] = fuzz.gaussmf(peso.universe,80,20)
                break
        elif func=="TRA":
                peso["magro"] = fuzz.trapmf(peso.universe,[0,10,25,30])
                peso["normal"] = fuzz.trapmf(peso.universe,[30,40,55,60])
                peso["pesado"] = fuzz.trapmf(peso.universe,[60,70,85,100])
                break
        else:
                print("FUNC INVALIDA!!!!!!!!!!")

#Visualizando as variáveis
calorias.view()
atividade.view()
peso.view()



#Criando as regras
regra_1 = ctrl.Rule(calorias['pouco'] & atividade['medio'], peso['magro'])
regra_2 = ctrl.Rule(calorias['muita'] & atividade['medio'], peso['pesado'])
regra_3 = ctrl.Rule(calorias['pouco'] | atividade['alta'], peso['magro'])
regra_4 = ctrl.Rule(calorias['muita'] & atividade['alta'], peso['normal'])
regra_5 = ctrl.Rule(calorias['razoavel'] | atividade['medio'], peso['normal'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3,regra_4])


#Simulando
calculo_peso = ctrl.ControlSystemSimulation(controlador)

notaCalorias = int(input('calorias: '))
notaAtividade = int(input('atividade: '))
calculo_peso.input['calorias'] = notaCalorias
calculo_peso.input['atividade'] = notaAtividade
calculo_peso.compute()

valorPeso = calculo_peso.output['peso']

print("\ncalorias %d \natividade %d \npeso de %5.2f" %(
        notaCalorias,
        notaAtividade,
        valorPeso))


calorias.view(sim=calculo_peso)
atividade.view(sim=calculo_peso)
peso.view(sim=calculo_peso)

plt.show()