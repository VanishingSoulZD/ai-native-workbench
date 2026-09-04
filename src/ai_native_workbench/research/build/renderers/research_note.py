def render_research_note_markdown(p):
 lines=['# Research Note']
 for s in p.sections:
  lines += ['',f'## {s.heading}',*s.paragraphs]
  lines += [f'Provenance reference: {r}' for r in s.refs]
 return '\n'.join(lines)+'\n'
