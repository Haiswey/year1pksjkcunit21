# QA, GitHub, artifact, Vercel

## Before publishing

1. `scripts/test_lesson.js` passes (no errors, no sideways scroll at 390 px, pictures load, every story reaches the end,
   no device-voice fallback when clips exist).
2. Look at screenshots yourself at 390 px in light and dark themes: quiz page, a story page, the story end buttons.
3. Look at every picture at full size and check expressions (see `illustrations.md`).
4. Report the final file size. The example with 17 pictures, 41 clips and 68 icons is about 3 MB.
5. State what you did not test (real phones, real ears, the teacher's devices).

## Files in the repo

- `index.html`: complete page. `source/index.readable.html`: same code with base64 replaced by `<EMBEDDED-DATA-OMITTED>`
  (make it with a regex on `data:...;base64,<200+ chars>`), so the teacher can read the code.
- `tools/`: voice scripts and notebooks. `CLAUDE.md`: general rules (optional).

## Publish steps

1. Preview as a Claude artifact (`Artifact` tool with the built file path; republish the same path to keep the URL).
   Artifacts are private until the teacher shares them. Tell her.
2. Commit with the attribution trailer the session requires and push only to the branch she names
   (`git push -u origin <branch>`; retry network errors up to 4 times with backoff). No pull request unless asked.
3. Deploy to Vercel from the branch: `create_deployment` with `gitSource` `{type:"github", org, repo, ref}`,
   `target:"production"`, `name`. The first time also pass `projectSettings` with framework/build/output null and later
   deployments pass `project` id. Vercel redeploys only when asked (call it again after each push).
4. New Vercel projects have login protection on, so pupils see a login page. The teacher asked for a public lesson,
   so `update_project` with `ssoProtection: null` was applied. Confirm with the teacher first when public use was not stated.
5. Extra address: `add_project_domain` with e.g. `name.vercel.app`; it needs the teacher's approval prompt.
6. Verify what you can: deployment state, and ask the teacher to open the link on a phone. From the cloud environment the
   site may be unreachable (network policy) and the Vercel fetch tool may be denied: say so instead of claiming success.

## Page weight

3 MB is fine on home Wi-Fi but heavier on mobile data. Tell her. Options: fewer or smaller pictures, WebP at lower quality,
or split voice clips out (loses offline use).

## Licensing and credits

Credit OpenMoji (CC BY-SA 4.0) and say scene pictures are AI generated with Canva.
