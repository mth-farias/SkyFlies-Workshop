# fly-review-plan — reference

Audits **landed work** after execute. Before execute, use `fly-plan-improve`.

## Example output block

```markdown
**Verdict:** FIXED

| Axis | Result |
|------|--------|
| Landed vs plan | FAIL — README still named the old skill id |
| Better bar | PASS — extra test is correct |
| Verification | PASS — pytest as named in the plan |
| Bounded smoke | PASS — leftover old skill dirs none |
| Regressions | PASS |
| Hygiene | PASS |

1. Patched README skill table to `fly-plan-improve`.
2. No commit (user did not ask).

Suggest `fly-handoff` when the operator is ready to close.
```

## Review axes detail

- **Landed vs plan:** every in-scope touch-list file has the intended change;
  missing work is P0/P1 depending on user-visible breakage.
- **Better bar:** if execute improved on a wrong plan, keep the improvement and
  say so.
- **Verification:** run the commands the plan named (or the repo's real ones if
  the plan was stale).
- **Bounded smoke:** optional Read/Grep/Shell on a named repo path. Not a
  drive-root listing.
- **Regressions:** leftover old names, dual manifests, tests that still assert
  the pre-WP state.
- **Hygiene:** no `.env` / JWKS in the report; no commit unless asked.
