import numpy as np

import scipy.sparse as sp
from PolyRound.static_classes.lp_interfacing import OptlangInterfacer
from PolyRound.mutable_classes.polytope import Polytope
from PolyRound.static_classes.lp_utils import ChebyshevFinder
import pandas as pd
from sympy.core import Add, Mul
from cobra.util.solver import solvers
import time


class PolytopeReducer:
    @staticmethod
    def constraint_removal(
        polytope, hp_flags, backend="glpk", thresh=1e-7, verbose=False, sgp=False
    ):
        """
        Removes redundant constraints and removes narrow directions by turning them into equality constraints
        :param polytope: Polytope object to round
        :param hp_flags: Dictionary of gurobi flags for high precision solution
        :param thresh: Float determining how narrow a direction has to be to declare an equality constraint
        :param verbose: Bool regulating output level
        :return: Polytope object with non-empty interior and no redundant constraints, number of removed constraints,
        number of inequality constraints turned to equality constraints.
        """
        interface = solvers[backend]
        m = interface.Model()
        m.configuration.timeout = 60 * 5
        # m = optModel("model")
        if backend == "gurobi":
            OptlangInterfacer.configure_gurobi_model(
                m, hp_flags, sgp=sgp, verbose=verbose
            )
        else:
            OptlangInterfacer.configure_optlang_model(m, hp_flags)
        r_names = [str(r) for r in polytope.A.columns]
        x = np.array([interface.Variable(name, lb=None) for name in r_names])
        m.add(x)

        # make all inequality constraints
        OptlangInterfacer.make_sparse_constraint_system(
            m, polytope.A, polytope.b, x, backend
        )
        # m.addConstr(A @ x <= np.squeeze(polytope.b.values), name="constr")

        if polytope.S is not None:
            # S = sp.csr_matrix(polytope.S)
            # m.addConstr(S @ x == np.squeeze(polytope.h.values), name="eq")
            OptlangInterfacer.make_sparse_constraint_system(
                m, polytope.S, polytope.h, x, backend, equality=True
            )

        m.update()
        # get Chebyshev center for faster solutions
        # cheb_center, dist = ChebyshevFinder.chebyshev_center(
        #     polytope, sgp=sgp, **hp_flags
        # )
        # cheb_center = pd.Series(cheb_center.squeeze(), index=r_names)
        # start = time.time()
        m, removed, refunctioned = PolytopeReducer.constraint_removal_loop(
            m, thresh, backend, verbose=verbose
        )
        # print(time.time() - start)
        A, b = OptlangInterfacer.constraints_as_mat(m, r_names, sense="<")
        if polytope.S is not None:
            S, h = OptlangInterfacer.constraints_as_mat(m, r_names, sense="=")
        if verbose:
            print("Number of removed constraints: " + str(removed))
            print("Number of refunctioned constraints: " + str(refunctioned))
        if polytope.S is not None:
            reduced_polytope = Polytope(A, b, S, h)
            return reduced_polytope, removed, refunctioned
        else:
            reduced_polytope = Polytope(A, b)
            return reduced_polytope, removed, refunctioned

    @staticmethod
    def constraint_removal_loop(m, thresh, backend, start_ind=None, verbose=False):
        interface = solvers[backend]
        constrs = m.constraints
        constr_index = {i: c for i, c in enumerate(constrs) if c.lb != c.ub}
        # in case all constraints are inequalities, we only try remove redundancies
        no_eq_constraints = len(constrs) == len(constr_index)
        if start_ind is not None:
            constr_index = {i: c for i, c in constr_index.items() if i >= start_ind}
        # for each constraint, solve three lps
        removed = 0
        refunctioned = 0
        # avoided_lps = 0
        for i in constr_index:
            if verbose:
                if i % 50 == 0:
                    print("\n Investigating constraint number: " + str(i) + "\n")

                # m.write("output/debug_temp.mps")
            constr_expr = constr_index[i].expression
            m.objective = interface.Objective(constr_expr, direction="max")
            # m.setObjective(constr_expr, gp.GRB.MAXIMIZE)
            # m.update()
            m.optimize()
            max_val = OptlangInterfacer.get_opt(m, backend)

            # now get altered problem
            orig_rhs = constr_index[i].ub
            constr_index[i].ub = orig_rhs + 1
            # m.update()
            m.optimize()
            pert_val = OptlangInterfacer.get_opt(m, backend)
            constr_index[i].ub = orig_rhs
            if np.abs(max_val - pert_val) < thresh:
                removed += 1
                # In this case remove constraint
                m.remove(constr_index[i])
            elif not no_eq_constraints:
                # Check if it might be an equality
                # first, make the "cheap" check
                # chebVal = PolytopeReducer.linExprSeriesProd(cheb_center, constr_expr)
                # if np.abs(max_val - chebVal) > thresh:
                #     avoided_lps += 1
                #     continue

                # m.setObjective(constr_expr, gp.GRB.MINIMIZE)
                m.objective = interface.Objective(constr_expr, direction="min")
                # m.update()
                m.optimize()
                min_val = OptlangInterfacer.get_opt(m, backend)
                if np.abs(max_val - min_val) < thresh:
                    refunctioned += 1
                    constr_index[i].lb = constr_index[i].ub
                    # center = (max_val + min_val) / 2
                    # if center != constr_index[i].RHS:
                    #     constr_index[i].setAttr("rhs", center)

            m.update()
        # if verbose:
        #     print(str(avoided_lps) + " lps were avoided with chebyshev center speed up")
        return m, removed, refunctioned

    @staticmethod
    def null_space(S, eps=1e-10):
        """
        Returns the null space of a matrix
        :param S: Numpy array
        :param eps: Threshold for declaring 0 singular values
        :return: Numpy array of null space
        """
        u, s, vh = np.linalg.svd(S)
        s = np.array(s.tolist())
        vh = np.array(vh.tolist())
        null_mask = s <= eps
        null_mask = np.append(null_mask, True)
        null_ind = np.argmax(null_mask)
        null = vh[null_ind:, :]
        return np.transpose(null)

    @staticmethod
    def linExprSeriesProd(center, lin_expr):
        val = 0.0
        if isinstance(lin_expr, Add):
            for mul in lin_expr.args:
                assert isinstance(mul, Mul)
                val += PolytopeReducer.multiplyMulObject(center, mul)
        else:
            assert isinstance(lin_expr, Mul)
            val += PolytopeReducer.multiplyMulObject(center, lin_expr)
        return val

    @staticmethod
    def multiplyMulObject(center, mul):
        val = 0.0
        mul_dict = mul.as_coefficients_dict()
        for name, coeff in mul_dict.items():
            val += center[name.name] * coeff
        return val
