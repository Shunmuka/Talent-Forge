import { rest } from 'msw';
export const handlers = [
  rest.post('/api/analyze', (req, res, ctx) =>
    res(
      ctx.status(200),
      ctx.json({
        score: 72,
        gaps: [{ skill: 'GraphQL', reason: 'TODO: replace stub' }],
        evidence: [{ resumeText: 'Sample resume', jdText: 'Sample JD' }],
        bullets: ['TODO: add tailored bullet']
      })
    )
  ),
  rest.post('/api/rewrite', (req, res, ctx) =>
    res(
      ctx.status(200),
      ctx.json({
        original: 'Original bullet placeholder.',
        revised: 'Rewritten bullet placeholder.',
        rationale: 'TODO: describe rewrite reasoning.'
      })
    )
  )
];
// TODO: swap MSW handlers with live API once ready.
