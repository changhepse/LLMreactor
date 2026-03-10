import scipy
import random
from scipy import integrate
import json
from PFR_data import chose_reactor
from split_data import  split_data
from data.data_1 import samples

# 预定义反应速率方程的微分表达式
REACTION_RATE_FUNCTIONS = {
    1: lambda x, k, A0, n1, x_f: 1 / (k * A0 ** (n1 - 1) * (1 - x) ** n1),
    2: lambda x, k, A0, n1, x_f, B0, n2: 1 / (k * A0 ** (n1 + n2 - 1) * (1 - x) ** n1 * (B0 / A0 - x) ** n2)
    # 可以继续添加更多预设反应
}
# 预定义反应所需的参数数量
REACTION_PARAM_COUNTS = {
    1: 4,  # k, A0, n1, x
    2: 6,  # k, A0, n1, x, B0, n2
}
# 预定义反应器类型
REACTION_DICT = {
    1:'BR',2:'PFR',3:'CSTR'
}

'''
full_paraments = [setting：[reactor_idx,rA_idx,question],kinetic_params:[k, c_A0, n1, x_f, c_B0, n2],extra_params:[Q, t_assist, f]]
'''

def creat_params_1(i):
    # 用于创建关于使用环氧乙烷水溶液生产乙二醇的反应参数
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
    # CH_{2}ClCH_{2}OH + NaHCO_{3} \longrightarrow CH_{2}OHCH_{2}OH + NaCl + CO_{2}
    # param_list = [reactor_idx, m_product, w_A, w_B, k, mole_ratio, mixraw_density, conservation]
    param_list = []
    k = 5.21 # mol-1h-1
    reactor_idx = 3 # 反应器类型1：BR 2：PFR 3：CSTR

    m_product = 1000 # kg/h
    w_A = 0.5
    w_B = 0.5
    if w_A > w_B:
        w_A, w_B = w_B, w_A
    mole_ratio = 1 # 碳酸氢钠：氯乙醇
    mixraw_density = 1.02 # 比重 kg/l
    conservation = 0.02*i+0.75
    param_list.append(reactor_idx)
    param_list.append(m_product)
    param_list.append(w_A)
    param_list.append(w_B)
    param_list.append(k)
    param_list.append(mole_ratio)
    param_list.append(mixraw_density)
    param_list.append(conservation)
    return param_list

def solver_1(param_list):
    reactor_idx = param_list[0]
    m_product = param_list[1]
    w_A = param_list[2]
    w_B = param_list[3]
    k = param_list[4]
    mole_ratio = param_list[5]
    mixraw_density = param_list[6]
    conservation = param_list[7]
    M_A = 80.5
    M_B = 84
    M_P = 62
    l_P = m_product/M_P # 每小时所需生产的乙二醇的量为 kmol/h
    m_A = l_P*M_A/(conservation*w_A) # 每小时所需的氯乙醇溶液的质量 kg/h
    m_B = l_P*M_B/(conservation*w_B)*mole_ratio # 每小时所需的碳酸氢钠溶液质量 kg/h
    q_raw = (m_A + m_B)/mixraw_density # 原料体积流量 l/h
    c_A0 = l_P*1000/(conservation*q_raw) # 氯乙醇的初始浓度 mol/l
    c_B0 = l_P*1000/(conservation*q_raw)*mole_ratio # 碳酸氢钠的初始浓度 mol/l
    if reactor_idx == 1 or 2:
        def function(x, c_A0, c_B0, k):
            return 1/(k*(1-x)*(c_B0-c_A0*(x)))
        t,_ = scipy.integrate.quad(function,0,conservation,args=(c_A0,c_B0,k))
    if reactor_idx == 3:
        t = conservation/(k*(1-conservation)*(c_B0-c_A0*conservation))
    v = t * q_raw
    result_list = []
    result_list.append(round(l_P,2))
    result_list.append(round(m_A,2))
    result_list.append(round(m_B,2))
    result_list.append(round(q_raw,2))
    result_list.append(round(c_A0,2))
    result_list.append(round(c_B0,2))
    result_list.append(round(t,2))
    result_list.append(round(v,2))
    return result_list

def dict_maker_1(param_list, result_list):
    reactor_idx = param_list[0]
    reactor_name = REACTION_DICT[reactor_idx]
    m_product = param_list[1]
    w_A = param_list[2]
    w_B = param_list[3]
    k = param_list[4]
    mole_ratio = param_list[5]
    mixraw_density = param_list[6]
    conversion_rate = param_list[7]
    l_p = result_list[0]
    m_a = result_list[1]
    m_b = result_list[2]
    q_raw = result_list[3]
    c_A0 = result_list[4]
    c_B0 = result_list[5]
    t = result_list[6]
    v = result_list[7]
    if reactor_idx == 1 or 2:
        t_solve = r"Reaction time obtained through integral calculation: t=\int_{0}^{x_{f} } \frac{c_{A0}dx_{A} }{r_{A}}=\int_{0}^{x_{f} } \frac{c_{A0}dx_{A} }{k*c_{A}*c_{B}}=\int_{0}^{x_{f} } \frac{dx_{A} }{k*(1-x_{A})*(c_{B0}-c_{A0}*x_{A})}="f"{t} h. "
    if reactor_idx == 3 :
        t_solve = r"Reaction time obtained through integral calculation: t=\frac{c_{A0}*x_{f}}{r_{A}}=\frac{c_{A0}*x_{f}}{k*c_{A}*c_{B}}=\frac{x_{f}}{k*(1-x_{A})*(c_{B0}-c_{A0}*x_{A})}="f"{t} h. "
    data_test={ 'prompt':"Please calculate the residence time and reactor volume based on the following conditions, "
                         "and provide recommendations for material selection.",
                'input':f"It is planned to carry out the saponification reaction of chloroethanol in {reactor_name}. "
                        "Chloroethanol reacts with sodium bicarbonate to produce ethylene glycol, the reaction "
                        "equation is as follows $\ce{CH_{2}ClCH_{2}OH + NaHCO_{3} \longrightarrow CH_{2}OHCH_{2}OH + NaCl + CO_{2}}$"
                        F"The production rate is {m_product}kg/h. "
                        f"{w_A} (weight) aqueous"+r" NaHCO_{3} solution and "+f"{w_B} (weight) "+r"CH_{2}ClCH_{2}OH aqueous solution are used as raw materials. "
                        f"The molar ratio of sodium bicarbonate to chloroethanol in the reactor charge is {mole_ratio}, "
                        f"and the specific gravity of the mixture is {mixraw_density}. "
                        r"The reaction rate of this reaction as follows $r_{A} = k \cdot c_{A} \cdot c_{B}$"
                        f"The rate constant of {k}/mol*h at reaction temperature. "
                        f"The conversion rate is {conversion_rate}. Please calculate the residence time and volume of the reactor.",
               'output':r"The relative molecular weight of NaHCO_{3} is 84 kg/kmol, CH_{2}ClCH_{2}OH is 80.5 kg/kmol, CH_{2}OHCH_{2}OH is 62 kg/kmol. "
                        f"Hourly production of ethylene glycol: {m_product}/62={l_p}kmol/h. "
                        f"Hourly required chloroethanol: {l_p}*80.5/({conversion_rate}*{w_A})={m_a}kg/h. "
                        f"Hourly required sodium bicarbonate: {l_p}*84*{mole_ratio}/({conversion_rate}*{w_B})={m_b}kg/h. "
                        r"Raw material volumetric flow rate: Q_{0}="f"({m_a}+{m_b})/{mixraw_density}={q_raw}L/h. "
                        r"Initial concentration of chloroethanol: c_{A0}="f"{l_p}*1000/({conversion_rate}*{q_raw})={c_A0}mol/L. "
                        r"Initial concentration of sodium bicarbonate: c_{B0}"f"={l_p}*1000*{mole_ratio}/({conversion_rate}*{q_raw})={c_B0}mol/L. "
                        r"The concentration of chloroethanol: c_{A}=c_{A0}*(1-x). "
                        r"The concentration of sodium bicarbonate: c_{B}=c_{B0}-c_{A0}*x. "
                        f"{t_solve}"
                        f"Theoretical volume is v={t}*{q_raw}={v} l."
                        f"After comprehensively considering various factors in the reaction process, "
                        f"the operating temperatures remain moderate with no presence of highly corrosive substances. "
                        f"Given the cost considerations, we recommend using carbon steel as the reactor material."}
    return data_test
#
# def creat_params_2():
#     # 用于创建关于使用乙酸乙酯皂化反应的反应参数
#     # 输出公式
#     # 在CSTR反应器中进行乙酸乙酯皂化反应，反应方程式为CH_{3}COOC_{2}H_{5}+NaOH\longrightarrow CH_{3}COONa+C_{2}H_{5}OH，
#     # 该反应对乙酸乙酯和氢氧化钠都是以及反应，其反应速率方程为r_{A}=k*c_{A}*c_{B},反应速率常数为5.61/mol*min,乙酸乙酯和氢氧化钠的进料量均为100kg/h
#     # 混合液比重为1.02 kg/l，要求最终转化率达到0.95。求反应器的停留时间和体积。
#     # print(f"原料体积流量：Q0=({m_raw_1}+{m_raw_2})/{mixraw_density}={Q0}l/h")
#     # print(f"氯乙醇的初始浓度：cA0={n_main_product}*1000/({conversion_rates}*{Q0})={CA0}mol/l")
#     # print(f"通过积分计算得到反应时间为：t=∫CA0/(k*CA**n1*CB**n2)dXA ={t}")
#     # print(f"反应体积为:Vr={Q0}*({t}+{t_assist})l")
#     # print(f"反应器实际体积为:V={Vr}/{f}={V}l")
#     # CH_{2}ClCH_{2}OH + NaHCO_{3} \longrightarrow CH_{2}OHCH_{2}OH + NaCl + CO_{2}
#     # param_list = [reactor_idx, m_product, w_A, w_B, k, mole_ratio, mixraw_density, conservation]
#     param_list = []
#     k = 5.63 # mol-1min-1
#     reactor_idx = random.randint(1,3) # 反应器类型1：BR 2：PFR 3：CSTR
#     m_A = random.randint(100,1000) # kg/h
#     m_B = m_A
#     mole_ratio = 1 # 碳酸氢钠：氯乙醇
#     mixraw_density = round(random.uniform(1.0,2.0),2) # 比重 kg/l
#     conservation = round(random.uniform(0.7,0.99),2)
#     param_list.append(reactor_idx)
#     param_list.append(m_A)
#     param_list.append(m_B)
#     param_list.append(k)
#     param_list.append(mole_ratio)
#     param_list.append(mixraw_density)
#     param_list.append(conservation)
#     return param_list
#
# def solver_2(param_list):
#     reactor_idx = param_list[0]
#     m_A = param_list[1]
#     m_B = param_list[2]
#     k = param_list[3]
#     mole_ratio = param_list[4]
#     mixraw_density = param_list[5]
#     conservation = param_list[6]
#     M_A = 76
#     M_B = 40
#     q_raw = (m_A + m_B)/mixraw_density # 原料总体积流量 l/h
#     c_A0 = m_A*1000/M_A/q_raw # 氯乙醇的初始浓度 mol/l
#     c_B0 = m_B*1000/M_B/q_raw*mole_ratio # 碳酸氢钠的初始浓度 mol/l
#     if reactor_idx == 1 or 2:
#         def function(x, c_A0, c_B0, k):
#             return 1/(k*(1-x)*(c_B0-c_A0*(x)))
#         t,_ = scipy.integrate.quad(function,0,conservation,args=(c_A0,c_B0,k))
#     if reactor_idx == 3:
#         t = conservation/(k*(1-conservation)*(c_B0-c_A0*conservation))
#     v = t * q_raw
#     result_list = []
#     result_list.append(round(q_raw,2))
#     result_list.append(round(c_A0,2))
#     result_list.append(round(c_B0,2))
#     result_list.append(round(t,2))
#     result_list.append(round(v,2))
#     return result_list
#
# def dict_maker_2(param_list, result_list):
#     reactor_idx = param_list[0]
#     reactor_name = REACTION_DICT[reactor_idx]
#     m_A = param_list[1]
#     m_B = param_list[2]
#     k = param_list[3]
#     mole_ratio = param_list[4]
#     mixraw_density = param_list[5]
#     conversion_rate = param_list[6]
#     q_raw = result_list[0]
#     c_A0 = result_list[1]
#     c_B0 = result_list[2]
#     t = result_list[3]
#     v = result_list[4]
#     if reactor_idx == 1 or 2:
#         t_solve = r"Reaction time obtained through integral calculation: t=\int_{0}^{x_{f} } \frac{c_{A0}dx_{A} }{r_{A}}=\int_{0}^{x_{f} } \frac{c_{A0}dx_{A} }{k*c_{A}*c_{B}}=\int_{0}^{x_{f} } \frac{dx_{A} }{k*(1-x_{A})*(c_{B0}-c_{A0}*x_{A})}="f"{t} h. "
#     if reactor_idx == 3 :
#         t_solve = r"Reaction time obtained through integral calculation: t=\frac{c_{A0} \cdot x_{f}}{r_{A}}=\frac{c_{A0} \cdot x_{f}}{k \cdot c_{A} \cdot c_{B}}=\frac{x_{f}}{k \cdot (1-x_{A}) \cdot (c_{B0}-c_{A0} \cdot x_{A})}="f"{t} h. "
#     data_test={ 'prompt':"Please calculate the residence time and reactor volume based on the following conditions, "
#                          "and provide recommendations for material selection.",
#                 'input':f"The saponification reaction of ethyl acetate is carried out in {reactor_name} reactor. "
#                         "The reaction equation is $\ce{CH_{3}COOC_{2}H_{5} + NaOH \longrightarrow CH_{3}COONa + C_{2}H_{5}OH}$, "
#                         "which is first-order with respect to both ethyl acetate and sodium hydroxide. "
#                         "The reaction rate equation is $r_{A} = k \cdot c_{A} \cdot c_{B}$, with a rate constant of 5.6 L/(mol·min)."
#                         f"The molar ratio of sodium bicarbonate to chloroethanol in the reactor charge is {mole_ratio}, "
#                         f"and the specific gravity of the mixture is {mixraw_density}. "
#                         r"The reaction rate of this reaction as follows r_{A}=k*c_{A}*c_{B}"
#                         f"The rate constant of {k}/mol*h at reaction temperature. "
#                         f"The conversion rate is {conversion_rate}. Please calculate the residence time and volume of the reactor.",
#                'output':r"The relative molecular weight of CH_{3}COOC_{2}H_{5} is 76 kg/kmol, NaOH is 40 kg/kmol. "
#                         r"Raw material volumetric flow rate: Q_{0}="f"({m_A}+{m_B})/{mixraw_density}={q_raw} m^{3}/h. "
#                         r"Initial concentration of ethyl acetate: c_{A0}="f"{m_A}*1000/(76*{q_raw})={c_A0} mol/L. "
#                         r"Initial concentration of sodium hydroxide: c_{B0}"f"={m_B}*1000*{mole_ratio}/(40*{q_raw})={c_B0} mol/L. "
#                         r"The concentration of chloroethanol: c_{A}=c_{A0}*(1-x). "
#                         r"The concentration of sodium bicarbonate: c_{B}=c_{B0}-c_{A0}*x. "
#                         f"{t_solve}"
#                         f"Theoretical volume is v={t}*{q_raw}={v} l."
#                         f"After comprehensively evaluating all factors in the reaction process, "
#                         f"the presence of a strongly alkaline substance (sodium hydroxide) requires careful material selection. "
#                         f"Considering cost-effectiveness requirements, we recommend using stainless steel as the reactor material."}
#     return data_test
#
# def creat_params_3():
#     # 用于创建关于使用乙酸乙酯制备反应的反应参数（可逆反应）
#     # 输出公式
#     # 在CSTR反应器中用乙醇和乙酸合成乙酸乙酯，反应方程式为CH_{3}COOH+C_{2}H_{5}OH \rightleftharpoons CH_{3}COOC_{2}H_{5}+H_{2}O，
#     # 该反应是可逆反应，采用浓硫酸作为催化剂，用A、B、C、D依次代表四种物质，反应速率方程为r_{A}=k_{1}*(c_{A}*c_{B} -\frac{1}{k_{c}}*c_{C}*c_{D}) ,在78摄氏度的条件下
#     # k_{1}=3.56*10E-5 dm^{6}/(min\cdot g\cdot mol)   k_{c}= 2.67，M_A=60 M_B=46 A与B同摩尔流量进料，要求乙酸乙酯(C)产量为1000kg/h 混合液比重为1.02 kg/l，假设进料均为纯料
#     # 要求乙酸A的转化率达到0.95.求反应器的停留时间和体积。
#     '''
#     r"The relative molecular weight of NaHCO_{3} is 84 kg/kmol, CH_{2}ClCH_{2}OH is 80.5 kg/kmol, CH_{2}OHCH_{2}OH is 62 kg/kmol. "
#                         f"Hourly production of ethylene glycol: {m_product}/62={l_p}kmol/h. "
#                         f"Hourly required chloroethanol: {l_p}*80.5/({conversion_rate}*{w_A})={m_a}kg/h. "
#                         f"Hourly required sodium bicarbonate: {l_p}*84*{mole_ratio}/({conversion_rate}*{w_B})={m_b}kg/h. "
#                         r"Raw material volumetric flow rate: Q_{0}="f"({m_a}+{m_b})/{mixraw_density}={q_raw}L/h. "
#                         r"Initial concentration of chloroethanol: c_{A0}="f"{l_p}*1000/({conversion_rate}*{q_raw})={c_A0}mol/L. "
#                         r"Initial concentration of sodium bicarbonate: c_{B0}"f"={l_p}*1000*{mole_ratio}/({conversion_rate}*{q_raw})={c_B0}mol/L. "
#                         r"The concentration of chloroethanol: c_{A}=c_{A0}*(1-x). "
#                         r"The concentration of sodium bicarbonate: c_{B}=c_{B0}-c_{A0}*(1-x). "
#                         f"{t_solve}"
#                         f"Theoretical volume is v={t}*{q_raw}={v} l."
#                         f"After comprehensively considering various factors in the reaction process, "
#                         f"the operating temperatures remain moderate with no presence of highly corrosive substances. "
#                         f"Given the cost considerations, we recommend using carbon steel as the reactor material."
#     '''
#     param_list = []
#     k1 = 3.56*10E-5 # dm^{6}/(min\cdot g\cdot mol)
#     kc = 2.67
#     reactor_idx = random.randint(1,3) # 反应器类型1：BR 2：PFR 3：CSTR
#     m_product = random.randint(100,1000) # kg/h
#     mole_ratio = 1 # 乙酸：乙醇
#     mixraw_density = round(random.uniform(0.79,1.2),2) # 比重 kg/l
#     conservation = round(random.uniform(0.4,0.65),2)
#     param_list.append(reactor_idx)
#     param_list.append(m_product)
#     param_list.append(k1)
#     param_list.append(kc)
#     param_list.append(mole_ratio)
#     param_list.append(mixraw_density)
#     param_list.append(conservation)
#
#     return param_list
#
# def solver_3(param_list):
#     reactor_idx = param_list[0]
#     m_product = param_list[1]
#     k1 = param_list[2]
#     kc = param_list[3]
#     mole_ratio = param_list[4]
#     mixraw_density = param_list[5]
#     conservation = param_list[6]
#     M_A = 60
#     M_B = 46
#     M_C = 88
#     n_product = m_product/M_C
#     m_A = n_product*M_A
#     m_B = n_product*M_B
#     q_raw = (m_A + m_B)/mixraw_density # 原料总体积流量 l/h
#     c_A0 = m_A*1000/M_A/q_raw # 乙酸的初始浓度 mol/l
#     c_B0 = m_B*1000/M_B/q_raw*mole_ratio # 乙醇的初始浓度 mol/l
#     if reactor_idx == 1 or 2:
#         def function(x, c_A0, c_B0, k1, kc):
#             return 1/k1*((1-x)*(c_B0-c_A0*x)-c_A0*x*x/kc)
#         t,_ = scipy.integrate.quad(function,0,conservation,args=(c_A0,c_B0,k1,kc))
#     if reactor_idx == 3:
#         t = conservation/k1*((1-conservation)*(c_B0-c_A0*conservation)-c_A0*conservation*conservation/kc)
#     v = t/60 * q_raw
#     result_list = []
#     result_list.append(round(n_product,2))
#     result_list.append(round(m_A,2))
#     result_list.append(round(m_B,2))
#     result_list.append(round(q_raw,2))
#     result_list.append(round(c_A0,2))
#     result_list.append(round(c_B0,2))
#     result_list.append(round(t/60,2))
#     result_list.append(round(v,2))
#     return result_list
#
# def dict_maker_3(param_list, result_list):
#     reactor_idx = param_list[0]
#     reactor_name = REACTION_DICT[reactor_idx]
#     m_product = param_list[1]
#     k1 = param_list[2]
#     kc = param_list[3]
#     mole_ratio = param_list[4]
#     mixraw_density = param_list[5]
#     conversion_rate = param_list[6]
#     n_product = result_list[0]
#     m_A = result_list[1]
#     m_B = result_list[2]
#     q_raw = result_list[3]
#     c_A0 = result_list[4]
#     c_B0 = result_list[5]
#     t = result_list[6]
#     v = result_list[7]
#     # 已知乙酸的相对摩尔质量为60 kg/kmol，乙醇的相对摩尔质量为46 kg/kmol，乙酸乙酯的相对摩尔质量为88 kg/kmol。
#     # 每小时需要生产的乙酸乙酯的摩尔流率为 n_product = {m_product}/88 = {n_product} kmol/h.
#     # 根据化学反应方程式可知，每小时所需的乙酸的质量流率为 m_A = {n_product}*60 = {m_A} kg/h.
#     # 每小时所需的乙醇的质量流率为 m_B = {n_product}*46 = {m_B} kg/h.
#     # 进料的总体积流率为 q_raw = ({m_A}+{m_B})*1000/{mixraw_density} = {q_raw} l/h.
#     # 乙酸的初始浓度为 c_{A0} = {m_A}*1000/(60*{q_raw}) = {c_A0} mol/l.
#     # 乙醇的初始浓度为 c_{B0} = {m_B}*1000/(46*{q_raw}) = {c_B0} mol/l.
#     # 转化率为x时，A的浓度为 c_{A} = c_{A0}*(1-x).
#     # B的浓度为 c_{B} = c_{B0}-c_{A0}*(1-x).
#     # C的浓度为 c_{C} = c_{A0}*x.
#     # D的浓度为 c_{D} = c_{A0}*x.
#     if reactor_idx == 1 or 2:
#         t_solve = r"Reaction time obtained through integral calculation: t=\int_{0}^{x_{f} } \frac{c_{A0}dx_{A} }{r_{A}}=\int_{0}^{x_{f} } \frac{c_{A0}dx_{A} }{k1*(c_{A}*c_{B}- \frac{c_{C}*c_{D}}{kc}}=\int_{0}^{x_{f} } \frac{dx_{A} }{k1*(1-x_{A})*(c_{B0}-c_{A0}*x_{A})-\frac{c_{A0}*x_{A}*x_{A}}{kc}}="f"{t} h. "
#     if reactor_idx == 3 :
#         t_solve = r"Reaction time obtained through integral calculation: t=\frac{c_{A0} \cdot x_{f}}{r_{A}}=\frac{c_{A0} \cdot x_{f}}{k \cdot c_{A} \cdot c_{B}}=\frac{x_{f}}{k \cdot (1-x_{A}) \cdot (c_{B0}-c_{A0} \cdot x)}="f"{t} h. "
#     data_test={ 'prompt':"Please calculate the residence time and reactor volume based on the following conditions, "
#                          "and provide recommendations for material selection.",
#                 'input':f"In a {reactor_name} reactor, "
#                         f"Ethyl acetate is synthesized from ethanol and acetic acid. "
#                         r"The reaction equation is $\ce{CH_{3}COOH + C_{2}H_{5}OH \rightleftharpoons CH_{3}COOC_{2}H_{5} + H_{2}O}$. "
#                         r"This reversible reaction uses concentrated sulfuric acid as a catalyst. "
#                         r"Assigning A, B, C, D to represent the four compounds respectively, "
#                         r"the reaction rate equation is $r_{A} = k_{1} \left( c_{A} \cdot c_{B} - \frac{1}{k_{c}} \cdot c_{C} \cdot c_{D} \right)$. "
#                         r"At 78°C, $k_{1} = 3.56 \times 10^{-5}  \text{dm}^{6}/(\text{min} \cdot \text{g} \cdot \text{mol})$, "
#                         r"$k_{c} = 2.67$, $M_A = 60 kg/kmol $, $M_B = 46 kg/kmol $. "
#                         f"A and B are fed at equal molar flow rates. The target ethyl acetate (C) production rate is {m_product} kg/h. "
#                         f"The mixture density is {mixraw_density} kg/L. "
#                         f"Assuming pure feed streams, the required conversion of acetic acid (A) is {conversion_rate}. "
#                         f"Please calculate the reactor residence time and volume.",
#                'output':r"The molar mass of acetic acid is 60 kg/kmol, ethanol is 46 kg/kmol, and ethyl acetate is 88 kg/kmol. "
#                         r"The molar flow rate of ethyl acetate required per hour is n_product = "f"{m_product}/88 = {n_product} kmol/h. "
#                         f"According to the chemical reaction equation, the mass flow rate of acetic acid required per hour is m_A = {n_product}*60 = {m_A} kg/h. "
#                         f"The mass flow rate of ethanol required per hour is m_B = {n_product}*46 = {m_B} kg/h. "
#                         f"The total volumetric feed flow rate is q_raw = ({m_A}+{m_B})*1000/{mixraw_density} = {q_raw} L/h. "
#                         r"The initial concentration of acetic acid is c_{A0} = "f"{m_A}*1000/(60*{q_raw}) = {c_A0} mol/L. "
#                         r"The initial concentration of ethanol is c_{B0} = "f"{m_B}*1000/(46*{q_raw}) = {c_B0} mol/L. "
#                         r"At conversion x, the concentration of A is c_{A} = c_{A0}*(1-x). "
#                         r"The concentration of B is c_{B} = c_{B0} - c_{A0}*x. "
#                         r"The concentration of C is c_{C} = c_{A0}*x. "
#                         r"The concentration of D is c_{D} = c_{A0}*x. "
#                         f"{t_solve}"
#                         f"Theoretical volume is v={t}*{q_raw}={v} l."
#                         f"After comprehensively evaluating various factors in the reaction process, "
#                         f"the emergence of highly corrosive substances (sulfuric acid) necessitates material considerations. "
#                         f"Given cost-effectiveness requirements, we recommend using stainless steel as the reactor material."}
#     return data_test

def main():
    data_list_1 = []
    n = 10 # 每种数据的个数

    for i in range(n):
        params_list = creat_params_1(i)
        print("循环次数:",i, params_list)
        result_list = solver_1(params_list)
        if result_list[6] <= 0 :
            continue
        data_test = dict_maker_1(params_list, result_list)
        data_list_1.append(data_test)
    # json_data = json.dumps(data_list_1)
    # for i in range(n):
    #     params_list = creat_params_2()
    #     print("循环次数:",i, params_list)
    #     result_list = solver_2(params_list)
    #     if result_list[3] <= 0 :
    #         continue
    #     data_test = dict_maker_2(params_list, result_list)
    #     data_list_1.append(data_test)
    # for i in range(n):
    #     params_list = creat_params_3()
    #     print("循环次数:",i, params_list)
    #     result_list = solver_3(params_list)
    #     if result_list[6] <= 0 :
    #         continue
    #     data_test = dict_maker_3(params_list, result_list)
    #     data_list_1.append(data_test)

    print(len(data_list_1))
    # with open("data/real_train.jsonl","w",encoding="utf-8") as file:
    #     for data in data_list_1:
    #         json_line = json.dumps(data)
    #         file.write(json_line+"\n")
    with open("data/real_val_conversion_PFR.jsonl","w",encoding="utf-8") as file:
        for data in data_list_1:
            json_line = json.dumps(data)
            file.write(json_line+"\n")


if __name__ == '__main__':
    main()


# data_list.append(data_test)
# json_data = json.dumps(data_list, ensure_ascii=False, indent=4)
# with open("data/data_1.jsonl", "w", encoding="utf-8") as file:
#     file.write(json_data)
#
# with open("data/data_1.py", "w", encoding="utf-8") as file:
#     file.write("samples = [\n")
#     for data in data_list:
#         # 将字典转换为Python格式的字符串（确保引号正确转义）
#         py_data = (
#             "    {\n"
#             f'        "prompt": "{data["prompt"]}",\n'
#             f'        "answer": "{data["answer"]}"\n'
#             "    },\n"
#         )
#         file.write(py_data)
#     file.write("]\n")
#
# param_list = creat_params_1()
# print(param_list)
# result_list = solver_1(param_list)
# print(result_list)

