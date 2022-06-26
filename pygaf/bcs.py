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
        type (int) : Boundary condition type; choices are type=1 (Dirichlet,
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
    def type(self):
        """int : Boundary condition type.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._type
    @type.setter
    def type(self, v):
        if v not in [1, 2, 3]:
            raise Exception('Boundary condition type must be 1, 2 or 3.')
        self._type = v

    @property
    def value(self):
        """dic : Boundary condition value(s)."""
        if self.type == 1:
            return {'head' : self.head}
        elif self.type == 2:
            return {'flow' : self.flow}
        elif self.type == 3:
            return {'head' : self.head, 'cond' : self.cond}

    def info(self):
        """Print the solution information."""
        print('BOUNDARY CONDITION INFORMATION')
        print('------------------------------')
        print('BC type', str(self.type)+',', self.value)
        print()
        return
