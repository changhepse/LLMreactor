import scipy
import random
import sympy
from sympy import integrate


def reaction1(x, k, A0, n1):
    A=A0*(1-x)
    return A0/(k*A**n1)
def reaction2(x, k, A0, n1, B0, n2):
    A = A0 * (1 - x)
    B = B0 - A0*x/n1*n2
    return A0/(k*A**n1*B**n2)

def BR_t(function,kinetic_params):
    k, C_A0, n1, x_f, C_B0, n2 = kinetic_params
    solution = scipy.integrate.quad(function, 0, x_f, args=(k, C_A0, n1, C_B0, n2))
    t = solution[0]
    return t


def BR_V(function,kinetic_params, extra_params):
    t = BR_t(function,kinetic_params)
    Q, t_assist, f = extra_params
    V = Q* (t + t_assist) / f
    return V


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

'''
full_paraments = [setting：[reactor_idx,rA_idx,question],kinetic_params:[k, c_A0, n1, x_f, c_B0, n2],extra_params:[Q, t_assist, f]]
'''

def process_parameters(full_paraments):
    """
    安全处理参数列表，确保所有变量都有合理的默认值
    参数:
    paraments: 包含 C_A0, C_B0, k, n1, n2, x_f, Q1, Q2 的参数列表
    返回:
    包含所有参数的元组
    """
    # 定义默认值
    kinetic_defaults = {
        'k': 1.0,  # 默认速率常数 (单位取决于反应级数)
        'C_A0': 1.0,  # 默认初始A浓度 (kmol/m3)
        'n1': 1,  # 默认A的反应级数
        'x_f': 0.9,  # 默认目标转化率
        'C_B0': 1.0,  # 默认初始B浓度 (kmol/m3)
        'n2': 1,  # 默认B的反应级数
    }
    extra_defaults = {
        'Q': 1.0,  # 进料体积流量m3/h
        't_assist': 0.0, # 默认的辅助时间，仅理想间歇式反应器,h
        'f':1.0, # 默认的装料系数，仅理想间歇式反应器
    }

    kinetic_params = full_paraments[1]
    extra_params = full_paraments[2] if len(full_paraments) > 2 else []

    # 获取反应类型
    rA_idx = full_paraments[0][1]

    # 获取该反应类型所需的参数数量
    param_count = REACTION_PARAM_COUNTS.get(rA_idx, 6)  # 默认6个参数

    # 处理kinetic_params
    # 确保参数列表长度至少为1
    if not kinetic_params:
        kinetic_params = []
        # 创建完整的动力学参数列表
    kinetic_keys = list(kinetic_defaults.keys())[:param_count]
    full_kinetic = []
    for i, key in enumerate(kinetic_keys):
        if i < len(kinetic_params):
            full_kinetic.append(kinetic_params[i])
        else:
            full_kinetic.append(kinetic_defaults[key])


    # 处理extra_params
    # 确保参数列表长度至少为1
    if not extra_params:
        extra_params = []
    # 创建完整的额外参数列表
    extra_keys = list(extra_defaults.keys())
    full_extra = []
    for i, key in enumerate(extra_keys):
        if i < len(extra_params):
            full_extra.append(extra_params[i])
        else:
            full_extra.append(extra_defaults[key])

    return full_kinetic, full_extra


def BR_solve(full_paraments):
    '''
    full_paraments 代表求解问题所提供的参数表 full_paraments = [setting：[reactor_idx,rA_idx,question],
                 kinetic_params:[k, c_A0, n1, x_f, c_B0, n2],extra_params:[Q, t_assist, f]]
    reactor 代表所选择的反应器类型 1：BR 2：PFR 3：CSTR 4：全选
    rA_idx 代表反应速率表达式编号，代表不同的反应速率表达式
    question 代表所要求解的问题 1：求t 2：求体积V 3 ：求
    kinetic_params 代表所需要的动力学参数列表，[k, c_A0, n1, x_f, c_B0, n2]
    extra_params 代表所需要的额外参数列表，[Q, t_assist, f]
    '''

    rA_idx = full_paraments[0][1]
    question = full_paraments[0][2]
    kinetic_params, extra_params = process_parameters(full_paraments)
    # print(kinetic_params)

    # 获取预设的反应速率函数
    if rA_idx not in REACTION_RATE_FUNCTIONS:
        raise ValueError(f"未知的反应类型: {rA_idx}")

    rate_function = REACTION_RATE_FUNCTIONS[rA_idx]
    t, _ = scipy.integrate.quad(rate_function, 0, kinetic_params[3],args=tuple(kinetic_params))
    t_h = t/60
    if question == 1:
        result = round(t_h,2)
        # print("BR反应器求解得到的结果为：", result, "h")
    elif question == 2:
        Q, t_assist, f = extra_params
        result = round(Q* (t_h + t_assist) / f,2)
        # print("BR反应器求解得到的结果为：", result, "m3")
    return result




def PFR_solve(full_paraments):
    '''
    full_paraments 代表求解问题所提供的参数表 full_paraments = [setting：[reactor_idx,rA_idx,question],
             kinetic_params:[k, c_A0, n1, x_f, c_B0, n2],extra_params:[Q, t_assist, f]]
    reactor 代表所选择的反应器类型 1：BR 2：PFR 3：CSTR 4：全选
    rA_idx 代表反应速率表达式编号，代表不同的反应速率表达式
    question 代表所要求解的问题 1：求t 2：求体积V 3 ：求
    kinetic_params 代表所需要的动力学参数列表，[k, c_A0, n1, x_f, c_B0, n2]
    extra_params 代表所需要的额外参数列表，[v0]
    '''
    rA_idx = full_paraments[0][1]
    question = full_paraments[0][2]
    kinetic_params, extra_params = process_parameters(full_paraments)


    # 获取预设的反应速率函数
    if rA_idx not in REACTION_RATE_FUNCTIONS:
        raise ValueError(f"未知的反应类型: {rA_idx}")

    rate_function = REACTION_RATE_FUNCTIONS[rA_idx]

    t, _ = scipy.integrate.quad(rate_function, 0, kinetic_params[3],args=tuple(kinetic_params))
    t_h = t/60
    if question == 1:
        result = round(t_h,2)
        # print("PFR反应器求解得到的结果为：", result, "h")
    elif question == 2:
        v0 = extra_params[0]
        result = round(v0*t_h,2)
        # print("PFR反应器解得到的结果为：", result, "m3")
    return result

def CSTR_solve(full_paraments):
    '''
    full_paraments 代表求解问题所提供的参数表 full_paraments = [setting：[reactor_idx,rA_idx,question],
        kinetic_params:[k, c_A0, n1, x_f, c_B0, n2],extra_params:[Q, t_assist, f]]
    reactor 代表所选择的反应器类型 1：BR 2：PFR 3：CSTR 4：全选
    rA_idx 代表反应速率表达式编号，代表不同的反应速率表达式
    question 代表所要求解的问题 1：求t 2：求体积V 3 ：求
    kinetic_params 代表所需要的动力学参数列表，[k, c_A0, n1, x_f, c_B0, n2]
    extra_params 代表所需要的额外参数列表，[v0]
    '''
    rA_idx = full_paraments[0][1]
    question = full_paraments[0][2]
    kinetic_params, extra_params = process_parameters(full_paraments)

    # 获取预设的反应速率函数
    if rA_idx not in REACTION_RATE_FUNCTIONS:
        raise ValueError(f"未知的反应类型: {rA_idx}")

    rate_function = REACTION_RATE_FUNCTIONS[rA_idx]
    kinetic_params.insert(0,kinetic_params[3])
    t = kinetic_params[0]*rate_function(*kinetic_params)
    t_h = t/60
    if question == 1:
        result = round(t_h,2)
        # print("CSTR反应器求解得到的结果为：", result, "h")
    elif question == 2:
        v0 = extra_params[0]
        result = round(v0*t_h,2)
        # print("CSTR反应器求解得到的结果为：", result, "m3")
    return result

def chose_reactor(full_paraments):
    reactor_idx = full_paraments[0][0]
    if reactor_idx == 1:
        result = BR_solve(full_paraments)
    elif reactor_idx == 2:
        result = PFR_solve(full_paraments)
    elif reactor_idx == 3:
        result = CSTR_solve(full_paraments)
    elif reactor_idx == 4:
        result = [0,0,0]
        result[0] = BR_solve(full_paraments)
        result[1] = PFR_solve(full_paraments)
        result[2] = CSTR_solve(full_paraments)
    return result
# test_full_parameters = [[4,1,1],[0.00197,4,2,0.80],[0.171,1,0.75]]
# result = chose_reactor(test_full_parameters)
# print(result)
# test_full_parameters = [[1, 2, 2], [0.002, 9.23, 1, 0.735, 2.58, 1], [0.315, 4, 0.46]]
# result = chose_reactor(test_full_parameters)
# print(result)