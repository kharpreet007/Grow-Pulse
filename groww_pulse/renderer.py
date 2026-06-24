from dataclasses import dataclass
from typing import List
from groww_pulse.summarizer import ThemeSummary
from groww_pulse.config import Config

@dataclass
class EmailPayload:
    subject: str
    html_body: str
    text_body: str
    doc_link: str

def render_google_doc_content(summaries: List[ThemeSummary], iso_week: str, config: Config) -> str:
    """
    Renders the structured payload (as markdown text) to be appended to Google Docs.
    """
    product_name = config.product.name
    
    lines = []
    lines.append(f"{product_name} — Weekly Review Pulse ({iso_week})")
    lines.append("")
    lines.append(f"Period: {iso_week}")
    lines.append("")
    
    lines.append("Top Themes")
    lines.append("")
    
    for i, summary in enumerate(summaries, 1):
        lines.append(f"{i}. {summary.theme_name} ({summary.size} reviews)")
        lines.append(summary.description)
        lines.append("")
        
        if getattr(summary, 'quotes', None):
            lines.append("Real User Quotes:")
            for quote in summary.quotes:
                lines.append(f"- \"{quote}\"")
            lines.append("")
            
        if getattr(summary, 'action_ideas', None):
            lines.append("Action Ideas:")
            for j, idea in enumerate(summary.action_ideas, 1):
                lines.append(f"{j}. [{idea.team}] {idea.idea}")
            lines.append("")
            
    lines.append("--------------------------------------------------")
    lines.append("")
    
    return "\n".join(lines)


def render_email_payload(summaries: List[ThemeSummary], iso_week: str, config: Config, doc_link: str) -> EmailPayload:
    """
    Generates HTML and text email payloads.
    """
    product_name = config.product.name
    subject = f"{product_name} Review Pulse — {iso_week}"
    
    # HTML Body
    html_lines = []
    html_lines.append(f"<h2>{product_name} Review Pulse — {iso_week}</h2>")
    html_lines.append("<p>Here are the top themes from user reviews this week:</p>")
    html_lines.append("<ul>")
    for summary in summaries:
        html_lines.append(f"<li><strong>{summary.theme_name}</strong> ({summary.size} reviews) - {summary.description}</li>")
    html_lines.append("</ul>")
    html_lines.append(f'<p><a href="{doc_link}">Read full report &rarr;</a></p>')
    html_body = "\n".join(html_lines)
    
    # Text Body
    text_lines = []
    text_lines.append(f"{product_name} Review Pulse — {iso_week}")
    text_lines.append("")
    text_lines.append("Here are the top themes from user reviews this week:")
    for summary in summaries:
        text_lines.append(f"- {summary.theme_name} ({summary.size} reviews): {summary.description}")
    text_lines.append("")
    text_lines.append(f"Read full report: {doc_link}")
    text_body = "\n".join(text_lines)
    
    return EmailPayload(
        subject=subject,
        html_body=html_body,
        text_body=text_body,
        doc_link=doc_link
    )
