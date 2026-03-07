def generate_linkedin_post_prompt(context):
    return f"""
You are a business growth strategist.

Based on this context:
{context}

Write a high-converting LinkedIn post to generate inbound leads.

The post should:
- Be professional
- Create urgency
- Offer value
- Include call to action

Return clean LinkedIn-ready text.
"""