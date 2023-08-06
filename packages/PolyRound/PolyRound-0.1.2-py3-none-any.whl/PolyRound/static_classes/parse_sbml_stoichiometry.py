import pandas as pd
from PolyRound.mutable_classes.polytope import Polytope
import cobra


class StoichiometryParser:
    @staticmethod
    def parse_sbml_cobrapy(file, inf_bound=1e5):
        model = StoichiometryParser.read_sbml_model(file)
        p = StoichiometryParser.extract_polytope(model, inf_bound=inf_bound)
        return p

    @staticmethod
    def read_sbml_model(file):
        model = cobra.io.read_sbml_model(file)
        return model

    @staticmethod
    def extract_polytope(model, inf_bound=1e5):
        S = cobra.util.array.create_stoichiometric_matrix(model, array_type="DataFrame")
        # make bounds matrix
        n_react = len(model.reactions)
        A = pd.DataFrame(0.0, index=range(n_react * 2), columns=S.columns)
        b = pd.Series(0.0, index=range(n_react * 2))
        for ind, r in enumerate(list(model.reactions)):
            if r.bounds[1] == float("inf"):
                b[ind] = inf_bound
            else:
                b[ind] = r.bounds[1]
            if r.bounds[0] == float("-inf"):
                b[ind + n_react] = inf_bound
            else:
                b[ind + n_react] = -r.bounds[0]
            A.loc[ind, r.id] += 1
            A.loc[ind + n_react, r.id] -= 1
        p = Polytope(A, b, S=S)
        return p
