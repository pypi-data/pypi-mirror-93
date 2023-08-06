class ReqCheckException(Exception): pass
class PipMissing(ReqCheckException): pass
class PipFailed(ReqCheckException): pass
class ConstraintFailure(ReqCheckException): pass
