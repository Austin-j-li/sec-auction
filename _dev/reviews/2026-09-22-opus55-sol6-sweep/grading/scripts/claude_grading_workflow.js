export const meta = {
  name: 'sweep-grading-claude-v2',
  description: 'Blind Claude grading of sweep workbooks in a self-contained grading directory (two independent graders per bundle)',
  phases: [{ title: 'Grade', detail: 'two fresh Claude graders per blinded bundle, each with a private work directory' }],
}
const G = args.gradingDir
const GRADES = {
  type: 'object',
  properties: {
    grades: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, grade: { type: 'string', enum: ['pass', 'partial', 'fail'] },
      rows: { type: 'string' }, reason: { type: 'string' },
    }, required: ['id', 'grade', 'rows', 'reason'] } },
  },
  required: ['grades'],
}
phase('Grade')
const jobs = []
for (const b of args.bundles) {
  for (const g of [1, 2]) {
    const prompt = args.prompt
      .replace('{workdir}', `${G}/work/${b.label}.claude${g}`)
      .replace('{workbook}', `${G}/bundles/${b.label}/workbook.json`)
      .replace('{reference}', `${G}/reference/${b.deal}.json`)
      .replace('{filing}', `${G}/filings/${b.deal}.htm`)
      .replace('{instruction}', `${G}/instruction.md`)
      .replaceAll('{{', '{').replaceAll('}}', '}')
    jobs.push({ b, g, prompt })
  }
}
log(`${args.bundles.length} bundles, ${jobs.length} graders`)
const results = await parallel(jobs.map(j => () =>
  agent(`${j.prompt}\nReturn the grades through the structured output.`,
    { label: `grade:${j.b.label}#${j.g}`, phase: 'Grade', schema: GRADES })
    .then(r => ({ label: j.b.label, grader: `claude${j.g}`, grades: r ? r.grades : null }))))
const done = results.filter(Boolean)
const empty = done.filter(r => !r.grades).map(r => `${r.label}.${r.grader}`)
if (empty.length) log(`no grades returned for: ${empty.join(', ')}`)
return done