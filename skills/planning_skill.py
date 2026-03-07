def generate_plan_prompt(task_description):
    return f"""
You are Claude acting as an autonomous business AI employee.

Task:
{task_description}

Create a detailed execution plan in markdown format.

Include:
- Objective
- Step-by-step execution
- Required tools
- Risks
- Expected outcome

Return clean markdown only.
"""