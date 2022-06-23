class SteadyBC:
    """Boundary condition for steady state groundwater flow.

    The boundary condition can be type 1, 2 or 3 (see the 'type' attribute). An
    exception occurs if any other value is specified for type. The default
    SteadyBC object is a type 2 boundary condition with flow=0.0, which is
    equivalent to a no-flow boundary. The default type 1 Boundary has head=10.0
    (same as the default head of all Aquifer classes). The default type 3
    boundary condition has head=10.0 and cond=0.0, which is equivalent to
    a no-flow condition.

    Note a utilities function is available to calculate conductance values

    Attributes:
        type (str) : Boundary condition type; choices are type=1 (Dirichlet,
            first-type or constant head), type=2 (Neumann, second-type or
            constant flow) or type=3 (Cauchy or general head).
        head (float) : Value of head at the boundary for type 1 and value of
        external head for type 2 (units L, default 10.0).
        flow (float) : value of normal flow at boundary for type 2 (units L/T,
            default 0.0).
        cond (float) : Value of conductance for type 3 (units L2/T, default 0.0).

    """
    def __init__(self, type=2, head=10.0, flow=0.0, cond=0.0):
        self.type = type
        self.head = head
        self.flow = flow
        self.cond = cond

    @property
    def value(self):
        """dic : Boundary condition value(s)."""
        if self.type == 1:
            return {'head' : self.head}
        elif self.type == 2:
            return {'flow' : self.flow}
        elif self.type == 3:
            return {'head' : self.head, 'cond' : self.cond}
        else:
            raise Exception('Boundary condition type must be 1, 2 or 3.')
            return
