import random
from scipy import integrate
import json
from PFR_data import chose_reactor
from split_data import  split_data
from data.data_1 import samples

dict_reactor = {1:"BR",2:"PFR",3:"CSTR",4:"BR、PFR、CSTR"}
data_list=[]

'''
    full_paraments 代表求解问题所提供的参数表 full_paraments = [setting：[reactor_idx,rA_idx,question],
        kinetic_params:[k, c_A0, n1, x_f, c_B0, n2],extra_params:[Q, t_assist, f]]
    reactor 代表所选择的反应器类型 1：BR 2：PFR 3：CSTR 
    rA_idx 代表反应速率表达式编号，代表不同的反应速率表达式
    question 代表所要求解的问题 1：求t 2：求体积V 3 ：求
    kinetic_params 代表所需要的动力学参数列表，[k, c_A0, n1, x_f, c_B0, n2]
    extra_params 代表所需要的额外参数列表，[Q, t_assist, f]
'''
for i in range(1000):

    # setting = [1,1,1]
    # kinetic_params = [1.0,1.0,1,0.9,1.0,1]
    # extra_params = [1.0,0.0,1.0]
    setting = []
    kinetic_params = []
    extra_params = []
    reactor_idx = random.randint(1,3)
    rA_idx = random.randint(1,2)
    question = random.randint(1,2)
    setting.append(reactor_idx)
    setting.append(rA_idx)
    setting.append(question)

    k = round(round(random.uniform(1, 10), 2)*0.001,3)
    c_A0 = round(random.uniform(0.5, 10), 2)
    n1 = random.randint(1, 3)
    x_f = round(random.uniform(0.5, 0.999), 3)
    if rA_idx == 1:
        c_B0 = 1
        n2 = 0
        rA = r"k\\times c_{A}"+f"^{n1}"
        c_text = "The initial concentration of raw material A c_{A0}"+f" is {c_A0} kmol/m3."
    if rA_idx == 2:
        c_B0 = round(random.uniform(0.5, 10), 2)
        n2 = random.randint(1, 3)
        rA = r"k\\times c_{A}"+f"^{n1}"+r"\\times c_{B}"+F"^{n2}"
        c_text = "The initial concentration of raw material A c_{A0}"+f"{c_A0} kmol/m3, "+"and the concentration of raw material B is c_{B0}"+f"{c_B0} kmol/m3."
    kinetic_params.extend([k, c_A0, n1, x_f, c_B0, n2])

    Q = round(random.randint(10, 1000)*0.001,3)
    t_assist = random.randint(0,5)
    f = round(random.uniform(0.4, 0.8), 2)
    extra_params.extend([Q, t_assist, f])

    if reactor_idx == 1 :
        extra_text = f". The feed volumetric flow rate Q is {Q} kmol/m3, the auxiliary production time "+"t_{assist} "+f"is {t_assist} h, and the loading factor f is {f}."
    elif reactor_idx == 2 or 3:
        extra_text = f". The feed volumetric flow rate Q is {Q} kmol/m3."
    full_paraments = [setting, kinetic_params, extra_params]
    reactor = dict_reactor[reactor_idx]
    print(full_paraments)
    result = chose_reactor(full_paraments)
    if result <= 0.0 :
        continue
    if question == 1:
        question_text = f"Please calculate the residence time with following conditions?"
        if reactor_idx == 1 :
            if rA_idx == 1 :
                solution_text = f"For the {reactor} reactor,"+r"-r_{A} "+f"={rA} kmol/(L*min), "+r"c_{A} =c_{A0} \\times (1-x_{A} ) ,the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}."
                answer_text = r"The residence time \\tau of the"+f" {reactor} reactor is {result} h."
            if rA_idx == 2:
                solution_text = f"For the {reactor} reactor,"+r"-r_{A} "+f"={rA} kmol/(L*min), "+r"c_{A} =c_{A0} \\times (1-x_{A} ), c_{B} =c_{B0} - c_{A0} \\times x_{A}, the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}."
                answer_text = r"The residence time \\tau of the"+f" {reactor} reactor is {result} h."
        if reactor_idx == 2 :
            if rA_idx == 1:
                solution_text = f"For the {reactor} reactor," + r"-r_{A} " + f"={rA} kmol/(L*min), " + r"c_{A} =c_{A0} \\times (1-x_{A} ) ,the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}."
                answer_text = r"The residence time \\tau of the"+f" {reactor} reactor is {result} h."
            if rA_idx == 2:
                solution_text = f"For the {reactor} reactor," + r"-r_{A} " + f"={rA} kmol/(L*min), " + r"c_{A} =c_{A0} \\times (1-x_{A} ), c_{B} =c_{B0} - c_{A0} \\times x_{A}, the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}."
                answer_text = r"The residence time \\tau of the"+f" {reactor} reactor is {result} h."
        if reactor_idx == 3:
            if rA_idx == 1:
                solution_text = f"For the {reactor} reactor," + r"-r_{A} " + f"={rA} kmol/(L*min), " + r"c_{A} =c_{A0} \\times (1-x_{A} ) the residence time \\tau is calculated by \\frac{c_{A0} \\times x_{f} }{-r_{A} } ."
                answer_text = r"The residence time \\tau of the"+f" {reactor} reactor is {result} h."
            if rA_idx == 2:
                solution_text = f"For the {reactor} reactor," + r"-r_{A} " + f"={rA} kmol/(L*min), " + r"c_{A} =c_{A0} \\times (1-x_{A} ), c_{B} =c_{B0}- c_{A0} \\times x_{A}, the residence time \\tau is calculated by \\frac{c_{A0} \\times x_{f} }{-r_{A} }."
                answer_text = r"The residence time \\tau of the"+f" {reactor} reactor is {result} h."
        # if reactor_idx == 4 :
        #     solution_text = f"For BR and PFR reactors, the residence time tao is obtained by integrating c_A0/(-rA) from 0 to x_f; for CSTR reactor, the residence time tao is calculated by c_A0*x_f/(-rA)."
        #     answer_text = f"The residence time of the BR reactor is {result[0]} h, that of the PFR reactor is {result[1]} h, and that of the CSTR reactor is {result[2]} h."
    if question == 2:
        question_text = f"Please calculate the reactor volume with following conditions？"
        if reactor_idx == 1 :
            if rA_idx == 1 :
                solution_text = f"For the {reactor} reactor,"+r"-r_{A} "+f"={rA} kmol/(L*min), "+r"c_{A} =c_{A0} \\times (1-x_{A} ) ,the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}. And the reactor volume is \\frac{(\\tau + t_{assist} )\\times Q}{f}"
                answer_text = f"The calculated reactor volume V is {result} Cubic Meters."
            if rA_idx == 2 :
                solution_text = f"For the {reactor} reactor,"+r"-r_{A} "+f"={rA} kmol/(L*min), "+r"c_{A} =c_{A0} \\times (1-x_{A} ), c_{B} =c_{B0}- c_{A0} \\times x_{A}, the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}. And the reactor volume is \\frac{(\\tau + t_{assist} )\\times Q}{f}"
                answer_text = f"The calculated reactor volume V is {result} Cubic Meters."
        if reactor_idx == 2:
            if rA_idx == 1 :
                solution_text = f"For the {reactor} reactor,"+r"-r_{A} "+f"={rA} kmol/(L*min), "+r"c_{A} =c_{A0} \\times (1-x_{A} ) ,the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}. And the reactor volume is \\tau \\times Q"
                answer_text = f"The calculated reactor volume V is {result} Cubic Meters."
            if rA_idx == 2 :
                solution_text = f"For the {reactor} reactor,"+r"-r_{A} "+f"={rA} kmol/(L*min), "+r"c_{A} =c_{A0} \\times (1-x_{A} ), c_{B} =c_{B0}- c_{A0} \\times x_{A}, the residence time \\tau is obtained by c_{A0}\\times\\int_{0}^{x_{f}}\\frac{dx_{A}}{-r_{A}}. And the reactor volume is \\tau \\times Q"
                answer_text = f"The calculated reactor volume V is {result} Cubic Meters."
        if reactor_idx == 3:
            if rA_idx == 1:
                solution_text = f"For the {reactor} reactor," + r"-r_{A} " + f"={rA} kmol/(L*min), " + r"c_{A} =c_{A0} \\times (1-x_{A} ) the residence time \\tau is calculated by \\frac{c_{A0} \\times x_{f} }{-r_{A} }. And the reactor volume is \\tau \\times Q"
                answer_text = f"The calculated reactor volume V is {result} Cubic Meters."
            if rA_idx == 2:
                solution_text = f"For the {reactor} reactor," + r"-r_{A} " + f"={rA} kmol/(L*min), " + r"c_{A} =c_{A0} \\times (1-x_{A} ), c_{B} =c_{B0}- c_{A0} \\times x_{A}, the residence time \\tau is calculated by \\frac{c_{A0} \\times x_{f} }{-r_{A} }. And the reactor volume is \\tau \\times Q"
                answer_text = f"The calculated reactor volume V is {result} Cubic Meters."
        # if reactor_idx == 4:
        #     solution_text = f"For the BR reactor, the residence time tao is obtained by integrating c_A0/(-rA) from 0 to x_f, and the reactor volume is (tao+t_assist)*Q/f; for the PFR reactor, the residence time tao is obtained by integrating c_A0/(-rA) from 0 to x_f, and the reactor volume is tao*Q; for the CSTR reactor, the residence time tao is calculated by c_A0*x_f/(-rA), and the reactor volume is tao*Q."
        #     answer_text = f"The calculated reactor volume of the BR reactor is {result[0]} Cubic Meter, that of the PFR reactor is {result[1]} Cubic Meter, and that of the CSTR reactor is {result[2]} Cubic Meter."

    data_test = {
        'instruction':f"{question_text}",
        'input': f"It is planned to carry out the reaction A+B \longrightarrow C in {reactor}. "+"The experimentally determined reaction kinetic equation is -r_{A}"+f"={rA} kmol/(L*min), the reaction kinetic constant k={k}."
                  f"{c_text}, the conversion rate is {x_f}{extra_text}",
        'output': f"{solution_text} {answer_text}",
    }
    data_list.append(data_test)


json_data = "samples = " + json.dumps(data_list, ensure_ascii=False, indent=4)
with open("data/data_1.py", "w", encoding="utf-8") as file:
    file.write("samples = [\n")
    for data in data_list:
        py_data = ("{\n"
                   f'  "prompt": "{data["instruction"]}",\n'
                   f'  "input": "{data["input"]}",\n'
                   f'  "output": "{data["output"]}"\n'
                   "},\n")
        file.write(py_data)
    file.write("]\n")
    print("-----数据集制作完成-----")
#
# # 设置训练集比例 (0.0 - 1.0)
# TRAIN_RATIO = 1.0  # 80% 训练集, 20% 验证集
#
# # 分割数据集
# train_count, val_count = split_data(
#     samples,
#     train_ratio=TRAIN_RATIO,
#     output_train="data/virtual_train.json",
#     output_val="data/virtual_val.json"
# )
# print(f"数据集分割完成!")
# print(f"训练集样本数: {train_count}")
# print(f"验证集样本数: {val_count}")
#
# with open("data_base/data/data_1.jsonl", "w", encoding="utf-8") as f:
#     for s in samples:
#         json_line = json.dumps(s, ensure_ascii=False)
#         f.write(json_line + "\n")
#     else:
#         print("-----数据集制作完成-----")
    #
    # m_main_product=random.randint(10, 50)
    # w_raw_1=round(random.uniform(0.1, 0.6), 2)
    # w_raw_2=round(random.uniform(0.1, 0.6), 2)
    # mole_ratio=1
    # mixraw_density=1.02
    # n1=1
    # n2=1
    # k=5.2
    # conversion_rates=round(random.uniform(0.8, 0.99), 2)
    # t_assist=0.5
    # f=0.75
    #
    # M_CH2ClCH2OH=80.5
    # M_NaHCO3=84
    # M_CH2OHCH2OH=62
    #
    # M_raw_1=M_CH2ClCH2OH
    # M_raw_2=M_NaHCO3
    # M_main_product=M_CH2OHCH2OH
    # n_main_product=m_main_product/M_main_product
    # m_raw_1=n_main_product*M_raw_1/conversion_rates/w_raw_1
    # m_raw_2=n_main_product*M_raw_2/conversion_rates/w_raw_2
    # Q0=(m_raw_1+m_raw_2)/mixraw_density
    # CA0=n_main_product*1000/conversion_rates/Q0
    #
    # result=integrate.quad(func=function,a=0,b=conversion_rates,args=(n1,n2),full_output=True)
    # t=result[0]
    # Vr=Q0*(t+t_assist)
    # V=Vr/f
    #
    # n_main_product = round(n_main_product, 3)
    # m_raw_1 = round(m_raw_1, 3)
    # m_raw_2 = round(m_raw_2, 3)
    # Q0 = round(Q0, 3)
    # CA0 = round(CA0, 3)
    # t = round(t, 3)
    # Vr = round(Vr, 3)
    # V = round(V, 3)

    # 输出公式
    # print(f"拟在等温间歇反应器中进行氯乙醇的皂化反应,使用氯乙醇和碳酸氢钠反应生产乙二醇，产量为{m_main_product}kg/h，\n"
    #       f"使用{w_raw_2}(重量)的NaHC03水溶液及{w_raw_1}(重量)的氯乙醇水溶液作原料，\n"
    #       f"反应器装料中氯乙醇和碳酸氢钠的摩尔比为{mole_ratio}，混合液的比重为{mixraw_density}。\n"
    #       f"该反应对氯乙醇和碳酸氢钠均为一级，在反应温度下反应速率常数等于{k}/mol.h，要求转化率达到 {conversion_rates}。\n"
    #       f"若辅助时间为{t_assist},装填系数取{f}，试计算反应器的理论体积与实际体积")
    # print(f"每小时生产的乙二醇量：{m_main_product}/{M_main_product}={n_main_product}kmol/h")
    # print(f"每小时所需要的氯乙醇量：{n_main_product}*{M_raw_1}/({conversion_rates}*{w_raw_1})={m_raw_1}kg/h")
    # print(f"每小时所需要的碳酸氢钠量：{n_main_product}*{M_raw_1}/({conversion_rates}*{w_raw_1})={m_raw_2}kg/h")
    # print(f"原料体积流量：Q0=({m_raw_1}+{m_raw_2})/{mixraw_density}={Q0}l/h")
    # print(f"氯乙醇的初始浓度：cA0={n_main_product}*1000/({conversion_rates}*{Q0})={CA0}mol/l")
    # print(f"通过积分计算得到反应时间为：t=∫CA0/(k*CA**n1*CB**n2)dXA ={t}")
    # print(f"反应体积为:Vr={Q0}*({t}+{t_assist})l")
    # print(f"反应器实际体积为:V={Vr}/{f}={V}l")
#     data_test={'prompt':f"It is planned to carry out the saponification reaction of chloroethanol in an isothermal batch reactor. Chloroethanol reacts with sodium bicarbonate to produce ethylene glycol, with a production rate of {m_main_product}kg/h. "
#                          f"{w_raw_2} (weight) aqueous NaHCO3 solution and {w_raw_1} (weight) chloroethanol aqueous solution are used as raw materials. "
#                          f"The molar ratio of chloroethanol to sodium bicarbonate in the reactor charge is {mole_ratio}, and the specific gravity of the mixture is {mixraw_density}. "
#                          f"The reaction is first-order with respect to both chloroethanol and sodium bicarbonate, with a rate constant of {k}/mol.h at reaction temperature. The required conversion rate is {conversion_rates}. "
#                          f"If the auxiliary time is {t_assist} and the filling factor is {f}, calculate the theoretical and actual volumes of the reactor.",
#                'completion':f"Hourly production of ethylene glycol: {m_main_product}/{M_main_product}={n_main_product}kmol/h"
#                           f"Hourly required chloroethanol: {n_main_product}*{M_raw_1}/({conversion_rates}*{w_raw_1})={m_raw_1}kg/h"
#                           f"Hourly required sodium bicarbonate: {n_main_product}*{M_raw_1}/({conversion_rates}*{w_raw_1})={m_raw_2}kg/h"
#                           f"Raw material volumetric flow rate: Q0=({m_raw_1}+{m_raw_2})/{mixraw_density}={Q0}L/h"
#                           f"Initial concentration of chloroethanol: cA0={n_main_product}*1000/({conversion_rates}*{Q0})={CA0}mol/L"
#                           f"Reaction time obtained through integral calculation: t=∫CA0/(k*CA**n1*CB**n2)dXA ={t}"
#                           f"Reaction volume: Vr={Q0}*({t}+{t_assist})L"
#                           f"Actual reactor volume: V={Vr}/{f}={V}L"}
#     data_list.append(data_test)
# json_data = "samples = " + json.dumps(data_list, ensure_ascii=False, indent=4)
# with open("data/data_1.py", "w", encoding="utf-8") as file:
#     file.write("samples = [\n")
#     for data in data_list:
#         py_data = ("{\n"
#                     f'  "prompt": "{data["prompt"]}",\n'
#                     f'  "completion": "{data["completion"]}"\n'
#                    "},\n")
#         file.write(py_data)
#     file.write("]\n")
# with open("data/data_1.jsonl", "w", encoding="utf-8") as f:
#     f.write(json_data)
#     for s in samples:
#         json_line = json.dumps(s, ensure_ascii=False)
#         f.write(json_line + "\n")
#     else:
#         print("-----数据集制作完成-----")