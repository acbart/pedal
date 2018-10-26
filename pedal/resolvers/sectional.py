from pedal.resolvers import simple
from pedal.report import MAIN_REPORT

def resolve(report=None, priority_key=None):
    '''
    Args:
        report (Report): The report object to resolve down. Defaults to the
                         global MAIN_REPORT
    
    Returns
        str: A string of HTML feedback to be delivered
    '''
    if report is None:
        report = MAIN_REPORT
    if priority_key is None:
        priority_key = simple.by_priority
    # Prepare feedbacks
    feedbacks = report.feedback
    feedbacks.sort(key=lambda f: (f.section or 0, priority_key(f)))
    suppressions = report.suppressions
    # Process
    final_success = False
    final_score = 0
    finals = {0: []}
    for feedback in feedbacks:
        section = feedback.section or 0
        category = feedback.category.lower()
        if category in suppressions:
            if True in suppressions[category]:
                continue
            elif feedback.label.lower() in suppressions[category]:
                continue
        success, partial, message, data = simple.parse_feedback(feedback)
        final_success = success or final_success
        final_score += partial
        if message is not None:
            if section not in finals:
                finals[section] = []
            finals[section].append({
                'label': feedback.label,
                'message': message,
                'category': feedback.category,
                'data': data
            })
    final_hide_correctness = suppressions.get('success', False)
    if not finals:
        finals[0].append({
            'label': 'No errors',
            'category': 'Instructor',
            'data': [],
            'message': "No errors reported."
        })
    return (final_success, final_score, final_hide_correctness, finals)
