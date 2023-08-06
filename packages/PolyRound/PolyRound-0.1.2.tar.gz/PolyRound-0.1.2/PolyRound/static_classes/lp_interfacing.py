import numpy as np
import pandas as pd
from scipy import sparse as sp
from optlang.symbolics import Zero
from sympy.core import Add, Mul
from cobra.util.solver import solvers
from swiglpk import glp_adv_basis


class OptlangInterfacer:
    @staticmethod
    def make_sparse_constraint_system(m, A, b, x, backend, equality=False):
        interface = solvers[backend]
        A = sp.csr_matrix(A)
        constr_dict = dict()
        for row_ind, bound in enumerate(b):
            if equality:
                constr_dict[interface.Constraint(Zero, ub=bound, lb=bound)] = {
                    x[var_ind]: A[row_ind, var_ind]
                    for var_ind in A[row_ind, :].nonzero()[1]
                }
            else:
                constr_dict[interface.Constraint(Zero, ub=bound)] = {
                    x[var_ind]: A[row_ind, var_ind]
                    for var_ind in A[row_ind, :].nonzero()[1]
                }
        m.add(constr_dict.keys())
        m.update()
        for constr, terms in constr_dict.items():
            constr.set_linear_coefficients(terms)

    @staticmethod
    def configure_gurobi_model(m, hp_flags, sgp=False, verbose=False):
        if not sgp:
            m.problem.setParam("OutputFlag", 0)
        if verbose:
            print("Using the gurobi flags: " + str(hp_flags))
        for key, val in hp_flags.items():
            m.problem.setParam(key, val)
        # Never let the solver multi thread
        m.problem.setParam("Threads", 1)

    @staticmethod
    def configure_optlang_model(m, hp_flags, verbose=False):
        if "FeasibilityTol" in hp_flags:
            m.configuration.tolerances.feasibility = hp_flags["FeasibilityTol"]
        if "OptimalityTol" in hp_flags:
            m.configuration.tolerances.optimality = hp_flags["OptimalityTol"]

    @staticmethod
    def gurobi_solve(obj, A, b, backend, S=None, h=None, sgp=False, **kwargs):
        interface = solvers[backend]
        m = interface.Model()
        if backend == "gurobi":
            OptlangInterfacer.configure_gurobi_model(m, kwargs, sgp=sgp)
        r_names = [str(r) for r in range(A.shape[1])]
        x = np.array([interface.Variable(name, lb=None) for name in r_names])
        m.add(x)
        m.objective = interface.Objective(obj @ x, direction="min")
        # m.setObjective(obj @ x, gp.GRB.MINIMIZE)
        # sp_ratio = np.sum(np.abs(A) > 1e-12) / A.size
        # if sp_ratio < 0.1:
        # A = sp.csr_matrix(A)
        OptlangInterfacer.make_sparse_constraint_system(m, A, b, x, backend)
        # m.addConstr(A @ x <= np.squeeze(b), name="ineq")
        if S is not None:
            assert h is not None
            # sp_ratio = np.sum(np.abs(S) < 1e-12) / S.size
            # if sp_ratio < 0.1:
            # print("Sparse mode")
            # S = sp.csr_matrix(S)
            # m.addConstr(S @ x == np.squeeze(h), name="eq")
            OptlangInterfacer.make_sparse_constraint_system(
                m, S, h, x, backend, equality=True
            )
        # m.update()
        m.optimize()
        if m.status == "optimal":
            return pd.Series(m.primal_values).values, m
        else:
            x = np.zeros(A.shape[1])
            x[:] = np.nan
            return x, m

    @staticmethod
    def gurobi_solve_model(obj, m, backend):
        interface = solvers[backend]
        # m.reset()
        # m.update()
        x = m.variables
        # m.setObjective(obj @ x, gp.GRB.MINIMIZE)
        m.objective = interface.Objective(obj @ x, direction="min")
        # m.update()
        m.optimize()
        if m.status == "optimal":
            return pd.Series(m.primal_values).values, m
        else:
            x = np.zeros(len(m.variables))
            x[:] = np.nan
            return x, m

    @staticmethod
    def gurobi_regularize_chebyshev_center(obj_val, m, backend):
        interface = solvers[backend]
        x = np.array(m.variables)
        last_var = x[-1]
        m.add(interface.Constraint(last_var, lb=obj_val / 2))
        # m.addConstr(last_var, gp.GRB.GREATER_EQUAL, obj_val / 2)
        expr = x @ x
        m.objective = interface.Objective(expr, direction="min")
        # obj = np.eye(len(x))
        # obj[-1, -1] = 0
        # m.setMObjective(obj, None, 0, sense=gp.GRB.MINIMIZE)
        m.update()
        m.optimize()
        return pd.Series(m.primal_values).values, m

    @staticmethod
    def constraints_as_mat(m, r_names, sense="<"):
        constrs = m.constraints
        if sense == "<":
            constrs = [c for c in constrs if c.ub != c.lb]
        elif sense == "=":
            constrs = [c for c in constrs if c.ub == c.lb]
        else:
            raise ValueError
        b = pd.Series([c.ub for c in constrs], dtype=np.float64)
        c_df = pd.DataFrame(
            index=range(len(constrs)), columns=r_names, dtype=np.float64
        )
        for ind, constr in enumerate(constrs):
            if isinstance(constr.expression, Add):
                for mul in constr.expression.args:
                    assert isinstance(mul, Mul)
                    mul_dict = mul.as_coefficients_dict()
                    for var, coeff in mul_dict.items():
                        c_df.loc[ind, var.name] = float(coeff)
            elif isinstance(constr.expression, Mul):
                mul_dict = constr.expression.as_coefficients_dict()
                for var, coeff in mul_dict.items():
                    c_df.loc[ind, var.name] = float(coeff)
            else:
                raise ValueError(
                    "Invalid constraint expression detected, probably caused by a zero row in a constraint matrix."
                )
        c_df.fillna(0.0, inplace=True)
        return c_df, b

    @staticmethod
    def get_opt(m, backend):
        if m.status == "optimal":
            return m.objective.value
        elif m.status == "infeasible" or m.status == "check_original_solver_status":
            print("model in infeasible state, resetting lp")
            if backend == "gurobi":
                m.problem.reset()
            elif backend == "glpk":
                glp_adv_basis(m.problem, 0)
            else:
                raise ValueError(
                    "PolyRound does currently not support system reset for backend "
                    + backend
                )
            m.optimize()
            # m.setParam("BarHomogeneous", -1)
            if m.status == "optimal":
                return m.objective.value
            else:
                raise ValueError
        else:
            print("Solver status: " + str(m.status))
            raise ValueError
