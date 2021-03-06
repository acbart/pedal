"""
All of the feedback responses generated by TIFA.
"""
from pedal.utilities.operators import OPERATION_DESCRIPTION
from pedal.core.report import MAIN_REPORT
from pedal.core.feedback import FeedbackResponse


class TifaFeedback(FeedbackResponse):
    """ Base class for all TIFA feedback """
    muted = False
    category = FeedbackResponse.CATEGORIES.ALGORITHMIC
    kind = FeedbackResponse.KINDS.MISTAKE


class action_after_return(TifaFeedback):
    """ Statement after return """
    title = "Action after Return"
    message_template = ("You performed an action after already returning from "
                        "a function, on line {location.line}. You can "
                        "only return on a path once.")
    justification = ("TIFA visited a node not in the top scope when its "
                     "*return variable was definitely set in this scope.")

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class return_outside_function(TifaFeedback):
    """ Return statement outside of function """
    title = "Return outside Function"
    message_template = ("You attempted to return outside of a function on line "
                        "{location.line}. But you can only return from within "
                        "a function.")
    justification = "TIFA visited a return node at the top level."

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class multiple_return_types(TifaFeedback):
    """ Multiple returned types in single function """
    title = "Multiple Return Types"
    message_template = ("Your function returned {actual} on line {location.line}, "
                        "even though you defined it to return {expected}. "
                        "Your function should return values consistently.")
    justification = ("TIFA visited a function definition with multiple returns "
                     "that unequal types.")

    def __init__(self, location, expected, actual, **kwargs):
        super().__init__(location=location, expected=expected,
                         actual=actual, **kwargs)


class write_out_of_scope(TifaFeedback):
    """ Write out of Scope """
    title = "Write Out of Scope"
    message_template = ("You attempted to write the variable {name_message} "
                        "from a higher scope (outside the function) on line "
                        "{location.line}. You should only use variables inside "
                        "the function they were declared in.")
    justification = "TIFA stored to an existing variable not in this scope"

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class unconnected_blocks(TifaFeedback):
    """ Unconnected Blocks """
    title = "Unconnected Blocks"
    message_template = ("It looks like you have unconnected blocks on line {location.line}. "
                        "Before you run your program, you must make sure that all "
                        "of your blocks are connected that there are no unfilled "
                        "holes.")
    justification = "TIFA found a name equal to ___"

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class iteration_problem(TifaFeedback):
    """ Iteration Problem """
    title = "Iteration Problem"
    message_template = ("The variable {name_message} was iterated on line "
                        "{location.line} but you used the same variable as the iteration "
                        "variable. You should choose a different variable name "
                        "for the iteration variable. Usually, the iteration variable "
                        "is the singular form of the iteration list (e.g., "
                        "`for a_dog in dogs:`).")
    justification = "TIFA visited a loop where the iteration list and target were the same."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class initialization_problem(TifaFeedback):
    """ Initialization Problem """
    title = "Initialization Problem"
    message_template = ("The variable {name_message} was used on line {location.line}, "
                        "but it was not given a value on a previous line. "
                        "You cannot use a variable until it has been given a value."
                        )
    justification = "TIFA read a variable that did not exist or was not previously set in this branch."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class possible_initialization_problem(TifaFeedback):
    """ Possible Initialization Problem """
    title = "Possible Initialization Problem"
    message_template = ("The variable {name_message} was used on line {location.line}, "
                        "but it was possibly not given a value on a previous "
                        "line. You cannot use a variable until it has been given "
                        "a value. Check to make sure that this variable was "
                        "declared in all of the branches of your decision."
                        )
    justification = "TIFA read a variable that was maybe set but not definitely set in this branch."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class unused_variable(TifaFeedback):
    """ Unused Variable """
    title = "Unused Variable"
    message_template = ("The {kind} {name_message} was given a {initialization} on line "
                        "{location.line}, but was never used after that.")
    justification = ("TIFA stored a variable but it was not read any other time "
                     "in the program.")

    def __init__(self, location, name, variable_type, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        if variable_type.is_equal('function'):
            kind, initialization = 'function', 'definition'
        else:
            kind, initialization = 'variable', 'value'
        fields = {'location': location, 'name': name, 'type': variable_type,
                  'name_message': report.format.name(name),
                  'kind': kind, 'initialization': initialization}
        if 'fields' in kwargs:
            fields.update(kwargs.pop('fields'))
        super().__init__(location=location, fields=fields, **kwargs)


class overwritten_variable(TifaFeedback):
    """ Overwritten Variable """
    title = "Overwritten Variable"
    message_template = ("The variable {name_message} was given a value, but "
                        "{name_message} was changed on line {location.line} "
                        "before it was used. One of the times that you gave "
                        "{name_message} a value was incorrect."
                        )
    justification = ("TIFA attempted to store to a variable that was previously "
                     "stored but not read.")

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class iterating_over_non_list(TifaFeedback):
    """ Iterating over non-list """
    title = "Iterating over Non-list"
    message_template = ("The {iter} is not a list, but you used it in the "
                        "iteration on line {location.line}. You should only "
                        "iterate over sequences like lists.")
    justification = ("TIFA visited a loop's iteration list whose type was"
                     "not indexable.")

    def __init__(self, location, iter_name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        if iter_name is None:
            iter_list = "expression"
        else:

            iter_list = "variable " + report.format.name(iter_name)
        fields = {'location': location, 'name': iter_name, 'iter': iter_list}
        if 'fields' in kwargs:
            fields.update(kwargs.pop('fields'))
        super().__init__(location=location, fields=fields, **kwargs)


class iterating_over_empty_list(TifaFeedback):
    """ Iterating over empty list """
    title = "Iterating over empty list"
    message_template = ("The {iter} was set as an empty list, "
                        "and then you attempted to use it in an iteration on line "
                        "{location.line}. You should only iterate over non-empty lists."
                        )
    justification = "TIFA visited a loop's iteration list that was empty."

    def __init__(self, location, iter_name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        if iter_name is None:
            iter_list = "expression"
        else:
            iter_list = "variable " + report.format.name(iter_name)
        fields = {'location': location, 'name': iter_name, 'iter': iter_list}
        super().__init__(location=location, fields=fields, **kwargs)


class incompatible_types(TifaFeedback):
    """ Incompatible types """
    title = "Incompatible types"
    message_template = ("You used {op_name} operation with {left_name} and {right_name} on line "
                        "{location.line}. But you can't do that with that operator. Make "
                        "sure both sides of the operator are the right type."
                        )
    justification = "TIFA visited an operation with operands of the wrong type."

    def __init__(self, location, operation, left, right, **kwargs):
        op_name = OPERATION_DESCRIPTION.get(operation.__class__,
                                            str(operation))
        left_name = left.singular_name
        right_name = right.singular_name
        fields = {'location': location,
                  'operation': operation, 'op_name': op_name,
                  'left': left, 'right': right,
                  'left_name': left_name, 'right_name': right_name}
        super().__init__(location=location, fields=fields, **kwargs)


class invalid_indexing(TifaFeedback):
    """ Invalid Index """
    title = "Invalid Index"
    message_template = ("You indexed {left_name} with {right_name} on line "
                        "{location.line}. But you can't index {left_name} with "
                        "{right_name}."
                        )
    justification = ("TIFA attempted to call an .index() operation on a type"
                     " with a type that wasn't acceptable.")
    muted = True

    def __init__(self, location, left, right, **kwargs):
        left_name = left.singular_name
        right_name = right.singular_name
        fields = {'location': location,
                  'left': left, 'right': right,
                  'left_name': left_name, 'right_name': right_name}
        super().__init__(location=location, fields=fields, **kwargs)


class parameter_type_mismatch(TifaFeedback):
    """ Parameter type mismatch """
    title = "Parameter Type Mismatch"
    message_template = ("You defined the parameter {parameter_name_message} on line {location.line} "
                        "as {parameter_type_name}. However, the argument passed to that parameter "
                        "was {argument_type_name}. The formal parameter type must match the argument's type."
                        )
    justification = "TIFA visited a function definition where a parameter type and argument type were not equal."

    def __init__(self, location, parameter_name, parameter, argument, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        parameter_type_name = parameter.singular_name
        argument_type_name = argument.singular_name
        fields = {'location': location,
                  'parameter_name': parameter_name,
                  'parameter_name_message': report.format.name(parameter_name),
                  'parameter_type': parameter,
                  'argument_type': argument,
                  'parameter_type_name': parameter_type_name,
                  'argument_type_name': argument_type_name}
        super().__init__(location=location, fields=fields, **kwargs)


class read_out_of_scope(TifaFeedback):
    """ Read out of scope """
    title = "Read out of Scope"
    message_template = ("You attempted to read the variable {name_message} "
                        "from a different scope on line {location.line}. You "
                        "should only use variables inside the function they "
                        "were declared in."
                        )
    justification = "TIFA read a variable that did not exist in this scope but existed in another."

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


# TODO: Complete these
class type_changes(TifaFeedback):
    """ Type changes """
    title = "Type Changes"
    message_template = ("The variable {name_message} changed type from {old} to "
                        "{new} on line {location.line}.")
    justification = ""
    muted = True

    def __init__(self, location, name, old, new, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        fields = {'location': location, 'name': name,
                  'name_message': report.format.name(name),
                  'old': old, 'new': new}
        super().__init__(location=location, fields=fields, **kwargs)


class unnecessary_second_branch(TifaFeedback):
    """ Unnecessary second branch """
    title = "Unnecessary Second Branch"
    message_template = ("You have an `if` statement where one of the two branches"
                       " only has `pass` in its body, on line {location.line}."
                        " You shouldn't need an empty body.")
    justification = "There is an else or if statement who's body is just pass."

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class else_on_loop_body(TifaFeedback):
    """ Else on Loop body """
    title = "Else on Loop Body"
    message_template = "TODO"
    justification = ""

    def __init__(self, location, **kwargs):
        super().__init__(location=location, **kwargs)


class recursive_call(TifaFeedback):
    """ recursive call """
    title = "Recursive Call"
    message_template = "TODO"
    justification = ""
    muted = True

    def __init__(self, location, name, **kwargs):
        super().__init__(location=location, name=name, **kwargs)


class not_a_function(TifaFeedback):
    """ Not a function """
    title = "Not a Function"
    message_template = ("You attempted to call {name} as if it"
                        " was a function on line {location.line}. However,"
                        " that expression was actually a {called_type}.")
    justification = ""
    # TODO: Unmute?
    #muted = True

    def __init__(self, location, name, called_type, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        singular_name = called_type.singular_name
        fields = {'location': location, 'name': name,
                  'called_type': called_type,
                  'singular_name': singular_name}
        super().__init__(fields=fields, **kwargs)


class incorrect_arity(TifaFeedback):
    """ Incorrect arity """
    title = "Incorrect Arity"
    message_template = ("The function {function_name_message} was given the "
                        "wrong number of arguments.")
    justification = ""

    def __init__(self, location, function_name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, function_name=function_name,
                         function_name_message=report.format.name(function_name),
                         **kwargs)


class module_not_found(TifaFeedback):
    """ Module not found """
    title = "Module Not Found"
    message_template = "TODO"
    justification = ""
    muted = True

    def __init__(self, location, name, is_dynamic=False, error=None, **kwargs):
        fields = {"location": location, "name": name,
                  "is_dynamic": is_dynamic, "error": error}
        super().__init__(location=location, fields=fields, **kwargs)


class append_to_non_list(TifaFeedback):
    """ Append to non-list """
    title = "Append to non-list"
    message_template = "TODO"
    justification = ""
    muted = True

    def __init__(self, location, name, actual_type, **kwargs):
        fields = {'location': location, "name": name,
                  "actual_type": actual_type}
        super().__init__(location=location, fields=fields, **kwargs)


class nested_function_definition(TifaFeedback):
    """ Function defined not at top-level """
    message_template = ("The function {name_message} was defined inside of another"
                        "block on line {location.line}. For instance, you may "
                        "have placed it inside another function definition, or "
                        "inside of a loop. Do not nest your function "
                        "definition!")
    title = "Don't Nest Functions"
    justification = "Found a FunctionDef that was not at the top-level."
    muted = True
    unscored = True

    def __init__(self, location, name, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        super().__init__(location=location, name=name,
                         name_message=report.format.name(name), **kwargs)


class unused_returned_value(TifaFeedback):
    """ Expr node had a non-None value """
    title = "Did Not Use Function's Return Value"
    message_template = ("It looks like you called the {call_type} {name_message} on "
                        "{location.line}, but failed to store the result in "
                        "a variable or use it in an expression. You should "
                        "remember to use the result!")
    justification = "Expression node calculated a non-None value."
    muted = True
    unscored = True

    def __init__(self, location, name, call_type, result_type, **kwargs):
        report = kwargs.get("report", MAIN_REPORT)
        fields = {'location': location, 'name': name, 'call_type': call_type,
                  'result_type': result_type,
                  'name_message': report.format.name(name)}
        super().__init__(fields=fields, location=location, **kwargs)


'''
TODO: Finish these checks
"Empty Body": [], # Any use of pass on its own
"Malformed Conditional": [], # An if/else with empty else or if
"Unnecessary Pass": [], # Any use of pass
"Append to non-list": [], # Attempted to use the append method on a non-list
"Used iteration list": [], #
"Unused iteration variable": [], #
"Type changes": [], #
"Unknown functions": [], #
"Not a function": [], # Attempt to call non-function as function
"Recursive Call": [],
"Incorrect Arity": [],
"Aliased built-in": [], #
"Method not in Type": [], # A method was used that didn't exist for that type
"Submodule not found": [],
"Module not found": [],
"Else on loop body": [], # Used an Else on a For or While
'''

# TODO: Equality instead of assignment
